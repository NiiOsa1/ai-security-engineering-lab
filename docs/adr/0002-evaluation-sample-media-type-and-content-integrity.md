ADR-0002: Evaluation Sample Media Type and Content Integrity

Status

Accepted

Date

2026-09-07

Context

The AI Security Evaluation Harness must eventually execute multiple forms of evaluation material, including:

plain text

structured data

documents

audio

images

multimodal artifacts

The existing EvaluationSample contract identifies the exact intended evaluation material through:

sample ID

sample version

SHA-256 content hash

The execution layer now also has a ResolvedEvaluationSample contract that contains the exact bytes prepared for Target execution and independently verifies those bytes against the declared SHA-256 content hash.

A content hash identifies exact bytes.

A content hash does not identify how those bytes should be interpreted.

For example, the same byte sequence could be interpreted as:

text/plain
application/json
application/pdf
audio/wav
image/png

That interpretation can change evaluation behavior and therefore can change the result of a Run.

The project has a global requirement to version information that can materially change evaluation results.

The interpretation of an Evaluation Sample must therefore be part of its versioned definition rather than an undocumented assumption inside a Target adapter.

This decision must also preserve the distinction between:

sample identity
↓
expected content
↓
resolved content
↓
verified execution content

The execution system must not treat a syntactically valid recorded hash as proof that resolved bytes are correct.

The actual bytes must be independently hashed and compared with the expected digest before they are considered execution-ready.

Production Reference Floor

OCI Content Descriptors

OCI means Open Container Initiative.

The OCI descriptor model separates:

media type

content digest

content size

optional retrieval and annotation metadata

Its descriptor model treats content type and content identity as separate properties.

It also expects retrieved content to be verified against the expected digest when integrity matters.

The Lab adopts the relevant architectural lesson:

expected content identity
+
content interpretation
+
independent verification of consumed bytes

The Lab does not copy the complete OCI descriptor because fields must be justified by Lab requirements rather than copied for structural similarity.

Internet Media Types

RFC means Request for Comments.

RFC 6838 defines the registration and naming model used for Internet media types across HTTP, MIME, and other Internet protocols.

MIME means Multipurpose Internet Mail Extensions.

Although MIME originated in electronic mail, the media-type system is now broadly used to identify content formats.

Media types use the general form:

type/subtype

Examples include:

text/plain
application/json
application/pdf
audio/wav
image/png

RFC 6838 permits a type name and subtype name of up to 127 characters each.

The Lab therefore uses 255 characters as the outer length bound for the bare media-type value:

255

The Lab does not yet implement the complete RFC 6838 grammar.

A partial homemade parser could incorrectly reject valid media types or accept malformed ones while appearing standards-compliant.

Full standards validation will be added only if an interoperability or security requirement justifies it.

Decision

EvaluationSample will own the authoritative media type for each versioned evaluation sample.

The contract will evolve from:

EvaluationSample
├── sample_id
├── version
└── content_hash

to:

EvaluationSample
├── sample_id
├── version
├── content_hash
└── media_type

The media type is part of the versioned EvaluationSample definition because changing how the same bytes are interpreted may change evaluation behavior.

ResolvedEvaluationSample will carry the same media type alongside the exact resolved bytes:

ResolvedEvaluationSample
├── sample_id
├── sample_version
├── content_hash
├── media_type
└── content

The resolved content remains:

strict bytes

immutable after successful construction

excluded from default representation

excluded from default model serialization

independently verified against content_hash

The integrity invariant is:

SHA-256(resolved content bytes)

EvaluationSample content_hash

If the calculated digest differs from the declared digest, creation of the execution-ready sample must fail.

Unverified bytes must not be passed to a Target adapter.

Media Type Validation

At this stage, media_type will use deliberately minimal validation.

It must:

be present

be supplied as an actual string rather than coerced from another Python type

become nonblank after shared whitespace stripping

contain at least 3 characters

contain no more than 255 characters

The current contract will not claim full RFC 6838 validation.

The minimum length of 3 permits the smallest conceptual:

a/b

shape.

The maximum length of 255 reflects the RFC 6838 outer bound for a bare type/subtype pair.

This validation establishes a bounded required semantic field without creating a partial standards parser.

Adapter-specific support is a separate concern.

For example, an adapter may support:

text/plain
application/json

while rejecting:

audio/wav

because that adapter has no audio capability.

A syntactically acceptable media type does not imply that every Target adapter must support it.

RunSample Decision

RunSample will remain:

RunSample
├── sample_id
└── sample_version

It will not duplicate media_type.

RunSample is a historical reference to an exact EvaluationSample version.

The resolution path remains:

Run
↓
sample_id + sample_version
↓
exact EvaluationSample
↓
content_hash + media_type

Duplicating media_type inside RunSample would create two possible authoritative locations for the same fact.

Those values could eventually disagree.

The versioned EvaluationSample remains authoritative.

Storage and Resolver Boundary

EvaluationSample will not contain:

raw content bytes

filesystem paths

URLs

object-storage locations

provider-specific identifiers

cloud bucket names

Those are resolution and storage concerns.

The intended separation is:

EvaluationSample
= identity + expected digest + interpretation

resolver
= obtains the actual material

ResolvedEvaluationSample
= immutable integrity-verified execution snapshot

Target adapter
= consumes verified execution material

This prevents storage implementation details from leaking into the canonical evaluation domain contract.

Raw Content Handling

Raw resolved sample content may contain:

adversarial payloads

sensitive evaluation material

production-derived sanitized fixtures

documents

audio

other data that should not automatically enter logs

ResolvedEvaluationSample therefore excludes raw content from:

its default representation

normal model serialization

This is a safe-default behavior.

It is not encryption, access control, or complete data-loss prevention.

Code that possesses the object can still explicitly access its content.

Sensitive-data handling, evidence storage, retention, and telemetry sanitization remain separate security responsibilities.

Immutability

ResolvedEvaluationSample represents a verified execution snapshot.

After integrity verification succeeds, its identifying fields and content must not be reassigned through normal model mutation.

This reduces the risk that content or identifying metadata changes between verification and execution.

The content field uses Python bytes, which are immutable.

The resolved model is frozen through Pydantic configuration.

This reduces, but does not claim to eliminate every possible Time Of Check To Time Of Use risk.

The important invariant is:

verify exact immutable snapshot
↓
execute that same snapshot

Alternatives Considered

Alternative 1: Keep EvaluationSample without media_type

Rejected.

The content hash identifies bytes but does not define their intended interpretation.

Different adapters could silently interpret the same sample differently, weakening reproducibility.

Alternative 2: Store media_type only inside Target adapters

Rejected.

This would make sample meaning dependent on adapter-specific assumptions.

The same EvaluationSample could then mean different things depending on which adapter executes it.

Alternative 3: Store media_type only in ResolvedEvaluationSample

Rejected.

The interpretation would exist only after resolution and would not be part of the authoritative versioned sample definition.

Historical reconstruction could therefore lose the intended interpretation.

Alternative 4: Duplicate media_type inside RunSample

Rejected.

RunSample already identifies the exact EvaluationSample version.

Duplicating media_type would introduce redundant authoritative state and the possibility of disagreement.

Alternative 5: Implement a complete RFC 6838 media-type parser now

Deferred.

Correct Internet media-type validation has more syntax and interoperability detail than a simple regular expression suggests.

A partial parser could create false confidence.

The current requirement is to preserve authoritative content interpretation, not to build an Internet media-type validation library.

Full RFC-compliant validation should be introduced only when the requirement is concrete and should use a well-supported implementation or a deliberately tested standards implementation.

Alternative 6: Copy the full OCI descriptor model

Rejected for the current phase.

OCI descriptors also include fields such as:

content size

URLs

annotations

embedded data

artifact type

Those fields solve OCI-specific transport and artifact requirements.

The Lab will add comparable fields only when its own resolver, resource-control, provenance, or interoperability requirements justify them.

Consequences

Positive

This decision provides:

authoritative content interpretation

deterministic association between sample version and media type

cleaner multimodal extensibility

less adapter-specific ambiguity

improved reproducibility

independent content-integrity verification

immutable execution snapshots

safer default serialization of raw execution content

separation between domain identity and storage mechanics

a clean future boundary for Target adapter capability negotiation

Costs

Every EvaluationSample must now declare a media type.

Existing fixtures and tests constructing EvaluationSample objects must be updated.

ResolvedEvaluationSample must also carry the media type.

Future resolvers must preserve the media type from the authoritative EvaluationSample definition.

Adapters will eventually need explicit policies for which media types they support.

These costs are accepted because content interpretation can materially affect evaluation behavior.

Security Implications

This decision prevents several failure classes.

Wrong artifact execution

The resolver may return different bytes from those identified by the EvaluationSample.

Mitigation:

independent SHA-256 verification

Ambiguous interpretation

Two adapters may interpret identical bytes differently.

Mitigation:

authoritative versioned media_type

Silent type coercion

Evaluation metadata or resolved content may be silently coerced from an unintended Python type into the declared type, hiding an upstream producer error and weakening contract fidelity.

Mitigation:

strict string validation for media_type
+
strict bytes at the resolved execution boundary

Post-verification mutation

Verified execution state may change after validation.

Mitigation:

frozen resolved model
+
immutable bytes

Accidental raw-content logging

Raw evaluation material may leak through ordinary object representation or serialization.

Mitigation:

repr disabled for content
+
default serialization exclusion

These controls reduce risk but do not replace sandboxing, authorization, secrets handling, storage security, telemetry sanitization, or access control.

Proof Requirements

This decision is not complete merely because the models compile.

Executable tests must prove:

valid EvaluationSample media type
→ accepted

missing media type
→ rejected

blank media type
→ rejected

non-string media type
→ rejected

media type below minimum length
→ rejected

media type above maximum length
→ rejected

resolved sample
→ preserves media type

matching resolved bytes
→ accepted

valid but incorrect SHA-256
→ rejected

non-bytes resolved content
→ rejected

post-validation mutation
→ rejected

default representation
→ does not expose raw content

default model serialization
→ does not expose raw content

full regression suite
→ remains passing

Non-Goals of This Decision

This ADR does not decide:

final sample resolver architecture

final sample storage backend

filesystem versus database versus object-storage resolution

media-type capability negotiation protocol

full RFC 6838 parser implementation

charset handling

content encoding handling

media sniffing

maximum execution artifact size

decompression limits

streaming large sample content

sandbox architecture

final Target adapter protocol

Those decisions require their own requirements and evidence.

Follow-Up Decisions

The next relevant architecture work should define:

Evaluation Sample resolution boundary

Target execution port

Target adapter contract

supported execution request and response contracts

timeout and cancellation behavior

resource limits where justified

adapter media-type capability handling

deterministic reference Target

A separate Architecture Decision Record should be created for the Target adapter contract when that interface is ready to be frozen.

Public-Safe Scope

This ADR contains only public architectural decisions.

It does not contain customer information, production payloads, credentials, production infrastructure details, confidential artifacts, or private business strategy.

Decision Principle

An evaluation must not merely know:

which sample record was selected?

It must be able to prove:

which exact bytes were intended?
↓
how were those bytes intended to be interpreted?
↓
which bytes were actually resolved?
↓
did those bytes match the expected digest?
↓
was that verified snapshot the material supplied for execution?

Evaluation identity, content interpretation, and content integrity are separate concerns.

The Harness must preserve all three.