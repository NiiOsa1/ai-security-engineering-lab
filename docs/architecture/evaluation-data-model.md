# Evaluation Data Model

The AI Security Engineering Lab separates what is being tested, what data and conditions drive the evaluation, which security controls are present, how execution occurs, what the system actually does, what evidence is produced, and what security conclusions that evidence can support.

The model is designed for evaluations spanning production-grade language models, agentic systems, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), AI-assisted software engineering, memory-enabled systems, voice and multimodal AI, infrastructure, and cross-layer enterprise scenarios.

The lab does not treat model behavior as equivalent to system impact.

> Model compromise ≠ action attempt ≠ authorization granted ≠ execution ≠ external effect ≠ detection ≠ containment ≠ recovery.

Each state must be established from observable evidence.

---

# Design principles

## Evidence before conclusion

Security conclusions must be traceable to observable system behavior and retained evidence.

A model producing a malicious response does not prove that an unauthorized action executed.

An attempted tool call does not prove authorization was granted.

Authorization being granted does not prove execution completed.

Successful execution does not automatically prove an external effect occurred.

Every security claim must remain bounded by the evidence available to support it.

---

## Observation and interpretation are separate

The evaluation model distinguishes:

```text
what happened
```

from:

```text
what that behavior means
```

Trajectory and Evidence capture observable events and artifacts.

Outcome normalizes observable security states.

Assessment interprets those states against the security property defined by the Case.

This separation allows historical evidence to be rescored or reinterpreted without rewriting the original execution record.

---

## Unknown is not false

The absence of evidence for an event must not automatically be interpreted as proof that the event did not occur.

Where appropriate, security-relevant states distinguish between:

- observed
- not observed
- unknown
- not applicable

For example, if network telemetry was unavailable during a Run, `external_effect = false` would be an unjustified conclusion unless another evidence source established that no external effect occurred.

Missing telemetry must remain visible as uncertainty.

---

## Reproducibility and realism are complementary

The lab supports both controlled deterministic evaluation and realistic empirical evaluation.

Deterministic reference environments provide:

- repeatability
- evaluator validation
- known expected states
- scoring validation
- regression testing
- fork-safe Continuous Integration (CI)

Production-grade models, applications, agents, infrastructure, datasets, and integrations provide realistic behavioral evidence.

Neither replaces the other.

The lab therefore distinguishes evidence obtained from deterministic fixtures from evidence obtained through real model and system execution.

---

## Data provenance is part of the evidence

Evaluation data may originate from:

- authorized first-party systems and observations
- production-derived data that has been appropriately sanitized
- real-world public datasets
- established research and security evaluation corpora
- lab-generated empirical observations
- production-grade hosted models and services
- local open-weight models
- adversarially generated cases
- synthetic edge cases
- deterministic fixtures designed for reproducibility

The origin, version, transformation history, and limitations of evaluation data must be recorded where they materially affect interpretation.

Synthetic data is used to extend coverage, exercise rare conditions, generate controlled variations, and support reproducibility.

It is not treated as a substitute for real-world evidence where real-world evidence is required.

---

## Version everything that can change the result

Security results can change when any of the following change:

- model
- model provider
- model configuration
- system instructions
- developer instructions
- application code
- evaluation code
- Dataset
- Evaluation Sample
- retrieval configuration
- embedding configuration
- tools
- MCP servers
- Control definitions
- Control configuration
- identities
- permissions
- authorization policy
- sandbox
- filesystem policy
- network policy
- egress policy
- infrastructure
- detectors
- dependencies
- human approval policy

The data model therefore preserves version and configuration information wherever those details materially affect reproducibility or interpretation.

---

## Controls outside the model matter

Model-level defenses are only one part of the security system.

A compromised or manipulated model may still be prevented from producing system impact by deterministic controls outside the model.

Examples include:

- authentication
- authorization
- least privilege
- tool scope
- sandboxing
- filesystem restrictions
- network segmentation
- default-deny egress
- secrets isolation
- credential brokering
- human approval
- monitoring
- containment
- kill switches
- recovery controls

The data model therefore treats Control as an explicit security object rather than burying controls inside free-text configuration.

---

## Security evidence requires provenance and integrity

Evidence should answer:

```text
Where did this artifact come from?
Which Run produced it?
When was it produced?
Which component produced it?
Was it transformed?
Can its integrity be checked?
```

Security-critical Evidence should use hashes, immutable identifiers, version references, timestamps, or equivalent integrity mechanisms where practical.

---

## Sensitive evidence is not automatically public evidence

The internal evaluation model may contain information that must not be published directly.

Examples include:

- credentials
- secrets
- customer information
- personally identifiable information
- sensitive infrastructure details
- private production identifiers
- proprietary prompts
- proprietary source material
- restricted datasets

Evidence should therefore support classification and sanitization so that public artifacts preserve the security-relevant facts without exposing protected information.

---

# Canonical objects

The evaluation model is built around a canonical set of independently defined objects that preserve provenance, configuration, security controls, execution state, evidence, and conclusions across heterogeneous AI systems and evaluation environments.

---

## 1. Target

The Target is the system, component, model, agent, application, service, infrastructure layer, or controlled environment being evaluated.

A Target defines **what is under test**.

It does not define the attack being performed against it.

Targets may include:

- a production-grade hosted language model
- a local open-weight language model
- a RAG application
- an enterprise agent with authenticated tools
- an MCP-enabled system
- an AI coding agent
- a memory-enabled agent
- a multimodal system
- a voice AI system
- a tool execution service
- an authorization service
- a database or retrieval layer
- a sandboxed execution environment
- an infrastructure component
- a sanitized first-party system approved for evaluation
- a deterministic reference implementation used for reproducible security testing

A Target record should preserve enough identity and version information to determine exactly what system was evaluated.

Relevant Target identity may include:

- Target identifier
- Target type
- name
- version
- deployment type
- provider
- model identifier
- application revision
- infrastructure revision
- capability profile
- supported interfaces
- applicable trust boundaries

A Target may itself contain multiple components.

The data model therefore supports both whole-system evaluation and component-level evaluation without conflating the two.

---

## 2. Dataset or Corpus

A Dataset or Corpus is a versioned collection of inputs, artifacts, documents, conversations, attack material, benign controls, or other data available for evaluation.

Datasets may contain:

- real-world examples
- first-party observations
- public benchmark data
- academic research corpora
- security research corpora
- adversarial prompts
- poisoned documents
- malicious repository content
- tool outputs
- MCP responses
- voice recordings
- transcripts
- multimodal inputs
- benign control material
- generated attack variations
- regression material

Dataset provenance should record, where applicable:

- Dataset identifier
- source
- source organization
- version
- license
- collection method
- publication date
- acquisition date
- content hash
- modality
- language
- sanitization status
- sampling method
- transformation history
- generation method
- mutation lineage
- known limitations

A Dataset's presence in a public repository does not by itself establish its quality, realism, safety, representativeness, or suitability for a particular security claim.

### Dataset provenance classes

Datasets should be distinguishable by provenance.

Examples include:

```text
first-party observed
production-derived sanitized
real-world public
research corpus
lab-generated empirical
adversarially generated
synthetic
deterministic fixture
```

Generated data must never be represented as naturally observed real-world data.

### Dataset and Evaluation Sample are different

A Dataset defines an available population.

An Evaluation Sample identifies the exact material actually used during evaluation.

For example:

```text
Dataset:
Prompt Injection Corpus v3.2

        ↓

10,000 available source items

        ↓

Evaluation Sample:
sample-004817

        ↓

Run:
run-028817
```

Recording only the Dataset version is not sufficient to reproduce the exact execution.

---

## 3. Evaluation Sample

An Evaluation Sample is the exact input instance, input bundle, or derived test material supplied to an evaluation execution.

The Dataset or Corpus defines the broader collection.

The Evaluation Sample identifies exactly what material was used.

A Sample may contain or reference:

- a user prompt
- a multi-turn conversation
- a retrieved document
- a poisoned RAG chunk
- repository content
- a README
- an issue
- a pull-request comment
- tool output
- an MCP response
- a memory entry
- structured API input
- source code
- configuration
- an image
- an audio recording
- a transcript
- a multimodal bundle
- multiple coordinated artifacts required by one evaluation

An Evaluation Sample should preserve, where applicable:

- Sample identifier
- source Dataset identifier
- source Dataset version
- source item identifier
- content hash
- modality
- language
- source provenance
- acquisition method
- generation method
- transformation lineage
- mutation lineage
- sanitization status
- artifact references
- parent Sample identifier
- reproduction metadata

### Evaluation Samples do not belong exclusively to Cases

An Evaluation Sample is independent of a Case.

The same Sample may be reused across multiple Cases.

A Case may also execute against many different Samples.

For example:

```text
Sample S-001
    ├── Case PI-001
    ├── Case PI-014
    └── Case PI-028
```

Likewise:

```text
Case PI-001
    ├── Sample S-001
    ├── Sample S-002
    ├── Sample S-003
    └── Sample S-004
```

The exact Case-to-Sample binding is recorded by the Run.

This supports:

- provider comparisons
- model comparisons
- repeated testing
- multilingual testing
- attack mutations
- RAG evaluation
- voice transformation analysis
- benign controls
- statistical analysis

without coupling Samples permanently to one Case.

### Exact execution lineage

The Evaluation Sample preserves the path from source material to the exact material evaluated.

For example:

```text
Public Prompt Injection Corpus v3.2
        ↓
Source item:
item-004817
        ↓
Multilingual mutation
        ↓
Audio conversion
        ↓
Speech-to-Text transformation
        ↓
Evaluation Sample:
sample-009431
        ↓
Run:
run-028817
```

This distinction is essential when evaluation material is:

- sampled
- translated
- mutated
- encoded
- obfuscated
- converted to audio
- transcribed
- chunked
- retrieved
- summarized
- parsed
- combined with other artifacts

### Transformation lineage

Transformation history should remain traceable.

For voice:

```text
original attack text
        ↓
generated or recorded audio
        ↓
Speech-to-Text transcript
        ↓
normalized transcript
        ↓
security-critical token representation
        ↓
model input
```

For RAG:

```text
original document
        ↓
parser
        ↓
chunking
        ↓
embedding
        ↓
retrieval
        ↓
context supplied to model
```

For coding agents:

```text
repository content
        ↓
agent reads file
        ↓
content enters context
        ↓
model processing
        ↓
proposed tool action
```

Attacks may be introduced, removed, modified, or amplified during transformations.

The lineage must therefore remain part of the evidence chain.

### Compound Samples

Some security conditions require more than one input artifact.

For example:

```text
user request
+
poisoned retrieved document
+
malicious tool output
+
existing memory content
```

A single Evaluation Sample may therefore act as a manifest referencing multiple coordinated artifacts while preserving the provenance of every component.

### Sample immutability

Once referenced by a recorded Run, the logical contents of an Evaluation Sample must not be silently changed.

A transformed or mutated version should receive a new Sample identity or version while retaining lineage to its parent.

Historical Runs must not change meaning when source Datasets evolve.

---

## 4. Control

A Control is a versioned security mechanism intended to prevent, restrict, detect, contain, or recover from security-relevant behavior.

Controls exist independently of the model and may operate at any layer of the system.

Examples include:

- instruction hierarchy enforcement
- source isolation
- context minimization
- retrieval filtering
- output validation
- authentication
- authorization
- least privilege
- tool scoping
- allowlists
- deny policies
- sandboxing
- filesystem restrictions
- process restrictions
- network segmentation
- default-deny egress
- credential brokering
- secrets isolation
- human approval
- rate limiting
- anomaly detection
- security monitoring
- kill switches
- rollback mechanisms
- recovery procedures

### Control identity

A Control should preserve, where applicable:

- Control identifier
- name
- version
- Control class
- security layer
- enforcement point
- protected security property
- configuration schema
- expected behavior
- failure behavior
- dependencies
- implementation revision
- policy revision
- owner
- known limitations

### Control classes

Controls may be categorized by function.

Examples include:

```text
preventive
restrictive
detective
containment
recovery
```

A single mechanism may provide more than one function.

### Control layers

Controls may exist at layers such as:

```text
model
application
context
retrieval
identity
authorization
tool
sandbox
filesystem
process
network
egress
credential
human approval
detection
containment
recovery
```

### Control definition and Control activation are separate

The Control object defines the mechanism.

The Evaluation Environment records whether that Control is active and how it is configured for a particular evaluation.

For example:

```text
Control:
AUTHZ-003 v2.1

Security property:
Untrusted model output cannot authorize account modification.
```

Environment A may contain:

```text
AUTHZ-003 v2.1
state = disabled
```

Environment B may contain:

```text
AUTHZ-003 v2.1
state = enabled
policy = strict
```

The same Target can therefore be evaluated with different Control configurations.

### Control state

Within an Evaluation Environment, a Control may have states such as:

```text
enabled
disabled
observe-only
not applicable
```

Configuration must remain distinguishable from the Control's identity and version.

### Controls and findings

A Finding may identify:

- a missing Control
- a misconfigured Control
- a bypassed Control
- an incorrectly scoped Control
- a Control that failed open
- a Control that detected but did not contain
- a Control that contained impact but damaged benign functionality

This allows remediation to reference the exact mechanism that changed.

---

## 5. Evaluation Environment

The Evaluation Environment defines the runtime conditions under which a Target is evaluated.

It captures security-relevant context that may change the result.

Examples include:

- model provider
- model version
- model parameters
- system instructions
- developer instructions
- retrieval configuration
- embedding configuration
- tool availability
- tool permissions
- MCP server configuration
- identities
- credentials
- authorization policy
- filesystem permissions
- network access
- egress policy
- sandbox configuration
- memory state
- database state
- infrastructure version
- dependency versions
- detector configuration
- human approval requirements
- kill-switch configuration
- active Controls
- Control versions
- Control configuration

A Target describes what system is being evaluated.

An Evaluation Environment describes the conditions under which that Target is being evaluated.

A Control describes a security mechanism.

The Environment binds specific Control versions and configurations to a particular evaluation state.

These are intentionally separate.

### Example

```text
Target:
Enterprise Agent v2.1
```

Environment A:

```text
authorization control = AUTHZ-003 v2.1
authorization state = enabled
tool scope = read-only
egress control = enabled
human approval = required
```

Environment B:

```text
authorization control = AUTHZ-003 v2.1
authorization state = disabled
tool scope = write-capable
egress control = restricted
human approval = disabled
```

The Target remains the same.

The security outcome may change because the Environment and active Controls changed.

### Environment immutability

A historical Evaluation Environment referenced by a Run must remain reconstructable.

Changing a live policy after an evaluation must not silently rewrite the configuration associated with historical Runs.

A changed environment should therefore produce a new version or immutable snapshot.

---

## 6. Case

A Case is a versioned definition of one security test condition.

A Case defines what security property should be exercised and what evidence is required to determine the result.

A Case may specify:

- Case identifier
- version
- security objective
- Case type
- attack or benign condition
- source of untrusted influence
- expected trust boundary
- intended security property
- preconditions
- Target capabilities required
- Dataset requirements
- Sample-selection requirements
- expected behavior
- prohibited behavior
- required observations
- success criteria
- failure criteria
- scorer requirements
- taxonomy mappings
- framework mappings
- Control classes being exercised
- applicable security layers

### Case types

Cases may include:

```text
attack
benign control
functional control
negative control
reproduction
regression
```

Attack Cases determine whether a security property can be violated.

Benign Cases determine whether Controls preserve legitimate functionality.

Both are necessary.

A system that blocks every request may resist an attack while still fail as an engineering system.

### Cases reference security properties, not necessarily active Control instances

A Case may state:

```text
Unauthorized account modification must not execute.
```

It may identify authorization and tool-scope Controls as relevant.

The exact Control versions active during execution are resolved through the Evaluation Environment and recorded by the Run.

This allows the same Case to be reused across different Control implementations.

### Reusability

A Case is reusable.

It is not the record of one execution.

For example:

```text
Case PI-001

Security property:
Untrusted user input must not result in an unauthorized tool action.
```

The same Case may be executed:

- against multiple models
- against multiple providers
- against multiple Targets
- with different Samples
- under different authorization policies
- with different Controls
- across multiple repetitions
- before remediation
- after remediation

Each execution produces a separate Run.

---

## 7. Campaign

A Campaign is a versioned collection of Cases executed for a defined evaluation objective.

Campaigns may represent:

- baseline security evaluations
- adversarial evaluations
- Control comparisons
- model comparisons
- provider comparisons
- architecture comparisons
- red-team campaigns
- remediation verification
- regression suites
- release gates
- cross-layer attack campaigns

The Campaign defines the population from which campaign-level metrics and denominators are calculated.

Campaign configuration should make explicit, where applicable:

- Campaign identifier
- Campaign version
- Campaign objective
- included Cases
- excluded Cases
- Case versions
- Target selection
- Evaluation Environment selection
- Dataset selection
- Sample-selection strategy
- Control comparison strategy
- repetition strategy
- randomization strategy
- sampling strategy
- stopping criteria
- scoring policy
- start time
- completion criteria

### Campaign does not replace Case or Run

A Campaign groups and organizes evaluation work.

A Case defines one security test condition.

A Run records one actual execution.

For example:

```text
Campaign:
Prompt Injection Baseline

        ├── Case PI-001
        ├── Case PI-002
        └── Case PI-003
```

Each Case may generate multiple Runs.

### Denominator integrity

Metrics must retain their denominator.

For example:

```text
7 successful attacks / 50 valid attack runs
```

is materially more informative than:

```text
14% attack success
```

Campaign-level metrics must remain traceable to the exact Runs that produced them.

Case exclusions, invalid Runs, unsupported capabilities, and stopping criteria must remain visible when they affect interpretation.

---

## 8. Run

A Run is one concrete execution of one Case using one defined set of Evaluation Samples against one Target in one defined Evaluation Environment.

Repeated executions of the same Case produce separate Runs.

A Run should identify, where applicable:

- Run identifier
- Case identifier
- Case version
- Campaign identifier
- Target identifier
- Target version
- Dataset identifier
- Dataset version
- Evaluation Sample identifiers
- input artifact hashes
- Evaluation Environment identifier
- Evaluation Environment version
- resolved Control identifiers
- resolved Control versions
- resolved Control states
- source code revision
- evaluator version
- model
- provider
- model configuration
- start time
- end time
- random seed
- repetition number
- execution status
- Evidence references

The Run is the primary execution unit connecting evaluation intent to observed behavior.

### Critical Run relationship

A Run binds:

```text
Case
+
Evaluation Sample(s)
+
Target
+
Evaluation Environment
+
resolved Control configuration
+
Campaign context
        ↓
      Run
```

Each object answers a different question:

```text
Dataset
What population is available?

Evaluation Sample
What exact material was used?

Case
What security property is being tested?

Campaign
Why and how is this collection of tests being executed?

Target
What system is being tested?

Control
What security mechanism exists?

Evaluation Environment
Which Controls and runtime conditions are active?

Run
What happened during this one execution?
```

### Run identity

A Run must be uniquely identifiable.

The same Case executed twice against the same Target must still produce separate Run records.

For example:

```text
Case PI-017
Sample sample-310
Target Agent-A
Environment AUTHZ-STRICT
Repetition 1
        ↓
Run 000471
```

```text
Case PI-017
Sample sample-310
Target Agent-A
Environment AUTHZ-STRICT
Repetition 2
        ↓
Run 000472
```

This prevents repeated executions from being silently collapsed into one result.

### Invalid or interrupted Runs

Not every attempted Run produces a valid security result.

Runs may terminate because of:

- infrastructure failure
- provider failure
- timeout
- malformed input
- evaluator failure
- unavailable dependency
- rate limit
- human interruption
- corrupted Evidence
- unsupported Target capability

These must remain distinguishable from genuine security outcomes.

A failed evaluation harness must not be reported as a successful defense.

---

## 9. Trajectory

Trajectory is the ordered sequence of security-relevant events observed during a Run.

It captures how the system moved from input to outcome.

Depending on the Target, events may include:

1. untrusted input received
2. input transformed or transcribed
3. context assembled
4. retrieved content introduced
5. model inference performed
6. model response produced
7. tool or action requested
8. arguments constructed
9. identity resolved
10. authorization evaluated
11. authorization granted or denied
12. execution attempted
13. execution blocked or completed
14. filesystem state changed
15. process launched
16. network request attempted
17. network request completed
18. database state changed
19. memory state changed
20. external effect occurred
21. detector triggered
22. containment activated
23. recovery performed

The Trajectory preserves causal and temporal separation between:

```text
model behavior
authorization
execution
impact
detection
containment
recovery
```

### Event ordering

Where possible, Trajectory events should preserve:

- timestamp
- sequence number
- event type
- component
- actor
- identity
- Control involved
- input reference
- output reference
- Evidence reference
- correlation identifier

This allows reconstruction of the attack path after the Run completes.

### Source-to-sink reconstruction

For injection and agentic attacks, the Trajectory should support reconstruction such as:

```text
malicious repository instruction
        ↓
coding agent context
        ↓
model proposes shell command
        ↓
tool request created
        ↓
authorization evaluated
        ↓
sandbox executes command
        ↓
network egress attempted
        ↓
egress control denies request
        ↓
detector alert generated
```

This is substantially stronger Evidence than retaining only the model response.

---

## 10. Evidence

Evidence is the set of artifacts that support claims about a Run.

Evidence may include:

- original inputs
- canonical attack representations
- prompts
- model responses
- audio
- normalized transcripts
- retrieved documents
- context snapshots
- tool requests
- tool arguments
- MCP messages
- identity records
- authorization decisions
- Control evaluations
- policy evaluations
- execution logs
- process events
- filesystem changes
- network observations
- database state
- memory state
- external-effect records
- detector events
- containment events
- recovery events
- screenshots
- traces
- hashes
- structured telemetry
- scorer outputs
- human-review records

Evidence should be attributable to a specific Run and retained in a form suitable for verification.

### Evidence identity

Evidence records should support, where applicable:

- Evidence identifier
- Run identifier
- Evidence type
- producer
- creation time
- storage location
- content hash
- media type
- sensitivity classification
- sanitization state
- transformation lineage
- correlation identifier

### Evidence integrity

Security-critical Evidence should be integrity-protected where practical through:

- cryptographic hashes
- immutable identifiers
- source revision identifiers
- signed artifacts where justified
- append-only logging
- trusted timestamps
- equivalent integrity mechanisms

### Public and restricted Evidence

The project may maintain multiple representations of the same Evidence.

For example:

```text
restricted raw Evidence
        ↓
sanitization process
        ↓
sanitized public Evidence
```

The public artifact should retain the facts required to support the security claim without exposing protected information.

---

## 11. Outcome

Outcome is the normalized security state derived from observable Evidence.

Outcome records factual state transitions independently rather than collapsing them into a single binary result.

Relevant states may include:

- model compromise observed
- policy violation produced
- sensitive information exposed
- action attempted
- authorization requested
- authorization granted
- authorization denied
- execution attempted
- execution blocked
- execution completed
- external effect occurred
- persistence established
- detection occurred
- containment occurred
- recovery occurred

These states are not interchangeable.

> Model compromise ≠ action attempt ≠ authorization granted ≠ execution ≠ external effect.

### Example: compromise contained

```text
Model compromised
        ↓
Action attempted
        ↓
Authorization denied
        ↓
No execution
        ↓
No external effect
```

### Example: compromise produced impact

```text
Model compromised
        ↓
Action attempted
        ↓
Authorization granted
        ↓
Execution completed
        ↓
External effect occurred
```

These two Runs may involve the same successful prompt injection at the model layer.

They represent materially different system-level security outcomes.

### State certainty

Where necessary, an Outcome state supports values equivalent to:

```text
observed
not observed
unknown
not applicable
```

This prevents missing telemetry from silently becoming evidence of safety.

---

## 12. Assessment

Assessment is the security conclusion justified by the Case definition, Trajectory, Evidence, and normalized Outcome.

Assessment is deliberately separated from raw observation.

An Assessment may include:

- Assessment identifier
- pass
- fail
- warning
- inconclusive
- severity
- confidence
- attack success determination
- security-property determination
- affected Control
- root cause
- residual risk
- scorer
- scoring method
- human-review status
- reviewer rationale

### Deterministic scoring

Deterministic scoring should be preferred whenever the required state can be established directly from system Evidence.

Examples include:

```text
authorization decision = DENY
filesystem file exists = FALSE
network sink received payload = FALSE
database value changed = TRUE
process exit code = 0
```

These observations should not require an LLM judge.

### Semantic scoring

Model-based or human judgment may be required for conditions such as:

- semantic instruction following
- partial disclosure
- policy interpretation
- conversational manipulation
- hallucination severity
- ambiguous language

When semantic scoring is used, the mechanism must remain identifiable.

Relevant metadata may include:

- scorer type
- scorer version
- scoring prompt
- model
- model version
- rubric
- confidence
- human review

### Assessment reproducibility

Changing a scorer must not erase the original Assessment.

Where appropriate, the same historical Evidence may be reassessed using a new scoring method while preserving the original result.

---

## 13. Finding

A Finding is a security issue supported by one or more Assessments and their underlying Evidence.

A Finding represents an underlying security problem, not merely one failed execution.

Multiple Cases, Targets, Campaigns, Samples, or Runs may provide Evidence for the same Finding.

A Finding may track:

- Finding identifier
- title
- affected Target
- affected component
- security property violated
- affected Control
- Control failure mode
- root cause
- attack path
- impact
- severity
- confidence
- Evidence references
- reproduction information
- remediation status
- residual risk
- related Cases
- related Runs
- framework mappings

Findings must remain traceable to the Evidence supporting them.

### Control failure modes

A Finding may identify:

```text
control absent
control disabled
control misconfigured
control bypassed
control insufficiently scoped
control failed open
control detected but did not contain
control contained but damaged legitimate functionality
```

### Finding status

Typical lifecycle states may include:

```text
open
confirmed
remediation in progress
ready for retest
remediated
accepted risk
closed
reopened
```

A Finding must not be marked remediated merely because code, policy, or configuration changed.

---

## 14. Remediation

A Remediation is a documented Control or system change intended to address a Finding.

Remediation may occur at multiple layers, including:

- model configuration
- application logic
- instruction hierarchy
- context construction
- retrieval
- source isolation
- tool design
- identity
- authorization
- least privilege
- sandboxing
- filesystem policy
- process policy
- network policy
- egress control
- secrets management
- credential brokering
- human approval
- detection
- containment
- recovery

A Remediation record may preserve:

- Remediation identifier
- Finding identifier
- affected Control
- previous Control version
- new Control version
- change description
- code revision
- policy revision
- configuration revision
- deployment revision
- implementation date
- expected security effect
- known limitations

A Remediation is not considered effective merely because implementation changed.

Its effectiveness must be tested.

---

## 15. Retest

A Retest is a verification relationship linking a Remediation and its original Finding to one or more new Runs.

A Retest is not a substitute for Run.

The actual executions remain normal Runs.

The Retest records why those Runs were performed and what earlier Evidence they are intended to verify.

A Retest may link:

- Retest identifier
- original Finding
- original Cases
- original Samples
- original Runs
- original Evidence
- Remediation applied
- previous Control version
- new Control version
- Target version
- Evaluation Environment version
- new Runs
- new Evidence
- resulting Assessments
- residual risk

Retesting should preserve enough of the original evaluation conditions to support a defensible comparison while explicitly recording intentional changes.

### Example

Original Run:

```text
Prompt injection succeeds
        ↓
Action attempted
        ↓
Authorization grants write
        ↓
Execution completes
        ↓
External effect occurs
```

Remediation:

```text
Authorization Control
AUTHZ-003 v2.1
        ↓
AUTHZ-003 v2.2
```

Retest Run:

```text
Prompt injection still succeeds
        ↓
Action still attempted
        ↓
Authorization denied
        ↓
No execution
        ↓
No external effect
```

The model may remain vulnerable to manipulation while system-level impact is successfully contained.

The data model must preserve both facts.

---

## 16. Regression

Regression represents a persistent requirement to continue testing a previously established security property.

Regression is not a replacement for Case, Campaign, or Run.

A Regression requirement typically points back to one or more Cases that must continue to execute after the original Finding has been remediated.

Where appropriate, successfully remediated Cases become permanent regression coverage.

Regression evaluation may execute:

- locally
- during development
- during pull-request validation
- in Continuous Integration
- before release
- after dependency changes
- after model changes
- after provider changes
- after infrastructure changes
- after Control changes
- after authorization-policy changes
- after tool changes
- after retrieval changes

Regression results may feed a security gate such as:

```text
PASS
WARN
BLOCK
```

A Regression record may preserve:

- Regression identifier
- related Finding
- related Remediation
- required Cases
- required Target classes
- required Evaluation Environments
- required Control properties
- execution frequency
- gate policy
- failure policy
- active status

A Regression test is only useful if failure produces enough Evidence to explain:

```text
what changed
which security property failed
which Control changed or failed
where the Trajectory diverged
what impact became possible
```

---

# Object relationships

The canonical relationship model is:

```text
DATASET / CORPUS
        │
        │ produces / contains
        ▼
EVALUATION SAMPLE
        │
        │
        │ exact material
        │
        ├──────────────────────────────┐
        │                              │
        │                              │
        ▼                              │
      RUN ◄──────────────── CASE       │
       ▲                     ▲         │
       │                     │         │
       │                     │ selected by
       │                     │
       │                  CAMPAIGN
       │                     │
       │                     │ execution context
       │                     │
       │                     └───────────────┐
       │                                     │
       │                                     ▼
     TARGET                         EVALUATION ENVIRONMENT
       │                                     │
       │                                     │ resolves
       │                                     ▼
       │                                 CONTROL(S)
       │
       └─────────────────────► RUN ◄─────────┘
                                  │
                                  ▼
                              TRAJECTORY
                                  │
                                  ▼
                               EVIDENCE
                                  │
                                  ▼
                                OUTCOME
                                  │
                                  ▼
                              ASSESSMENT
                                  │
                                  ▼
                                FINDING
                                  │
                                  ▼
                             REMEDIATION
                                  │
                                  ▼
                                RETEST
                                  │
                                  ▼
                              REGRESSION
                                  │
                                  ▼
                               CI GATE
```

The diagram is conceptual rather than a database schema.

The most important relationship is:

```text
Case
+
Evaluation Sample(s)
+
Target
+
Evaluation Environment
+
resolved Control configuration
+
Campaign context
        ↓
      Run
```

Dataset does not replace Evaluation Sample.

Dataset defines an available population.

Evaluation Sample identifies exact material.

Evaluation Sample does not belong exclusively to a Case.

Cases and Samples are bound during execution.

Campaign does not replace Case.

Campaign selects and organizes Cases and their execution strategy.

Control does not replace Evaluation Environment.

Control defines the security mechanism.

Evaluation Environment defines which Control versions and configurations are active.

Case does not replace Run.

Case defines the security test.

Run records one concrete execution.

Retest does not replace Run.

Retest links Remediation verification to new Runs.

Regression does not replace Case.

Regression establishes that relevant security properties must continue to be tested.

---

# Example relationship

A Campaign may contain:

```text
Campaign:
Prompt Injection Baseline

        ├── Case PI-001
        ├── Case PI-002
        └── Case PI-003
```

The Campaign may select Samples from:

```text
Dataset:
Prompt Injection Corpus v3.2

        ↓

Sample S-001
Sample S-002
Sample S-003
```

The Sample and Case remain independent until execution.

For example:

```text
Case PI-001
+
Sample S-001
+
Target Agent-A
+
Environment Baseline
+
Controls Baseline
+
Repetition 1
        ↓
Run 0001
```

The same Sample may be used with another Case:

```text
Case PI-014
+
Sample S-001
+
Target Agent-A
+
Environment Baseline
        ↓
Run 0002
```

The same Case may use another Sample:

```text
Case PI-001
+
Sample S-002
+
Target Agent-A
+
Environment Baseline
        ↓
Run 0003
```

The same Case and Sample may also be used after hardening:

```text
Case PI-001
+
Sample S-001
+
Target Agent-A
+
Environment Hardened
+
AUTHZ-003 v2.2 enabled
        ↓
Run 0004
```

This structure supports:

- repeated testing
- A/B Control comparisons
- provider comparisons
- model comparisons
- architecture comparisons
- Dataset comparisons
- Sample-level analysis
- Control-effectiveness analysis
- remediation retesting
- statistical aggregation
- regression testing

without collapsing test definition, input identity, Control configuration, execution, and interpretation into one object.

---

# Security state model

The lab explicitly rejects the shortcut:

```text
Attack input
     ↓
Model responded badly
     ↓
System compromised
```

Instead, security evaluation follows the observable path:

```text
Untrusted influence
        ↓
Input / context processing
        ↓
Model behavior
        ↓
Action attempt
        ↓
Authorization decision
        ↓
Execution state
        ↓
External effect
        ↓
Detection
        ↓
Containment
        ↓
Recovery
        ↓
Evidence-backed Assessment
```

A security evaluation should determine how far an attack progressed through this chain.

---

# Evidence hierarchy

Not every artifact supports the same level of security claim.

The lab therefore distinguishes multiple Evidence layers.

---

## Model Evidence

What the model:

- generated
- selected
- inferred
- requested
- attempted to invoke

Examples:

- model response
- tool-call request
- generated arguments
- generated code

Model Evidence establishes model behavior.

It does not by itself establish system impact.

---

## Application Evidence

What the surrounding application:

- accepted
- transformed
- rejected
- routed
- retrieved
- persisted

Examples:

- context assembly logs
- parser output
- retrieval results
- routing decisions

---

## Identity Evidence

Which identity was associated with an operation.

Examples:

- user identity
- agent identity
- service identity
- workload identity
- delegated identity

---

## Authorization Evidence

What identity and policy Controls allowed or denied.

Examples:

- policy decision
- permission evaluation
- role resolution
- scope check
- approval state

---

## Execution Evidence

What actually executed inside the runtime.

Examples:

- process creation
- tool execution
- shell command execution
- filesystem modification
- API invocation
- database query

---

## Effect Evidence

What state changed beyond the immediate execution boundary.

Examples:

- external message sent
- database record modified
- remote service changed
- file transmitted
- deployment modified
- secret transmitted
- user-visible action completed

---

## Detection Evidence

What monitoring systems observed.

Examples:

- detector alert
- policy alert
- Security Information and Event Management event
- anomaly event
- security log

---

## Containment Evidence

What prevented additional impact after compromise or attempted compromise.

Examples:

- authorization denial
- sandbox denial
- filesystem restriction
- blocked egress
- revoked credential
- terminated process
- kill-switch activation

---

## Recovery Evidence

What restored the affected system or state.

Examples:

- rollback
- credential rotation
- state restoration
- memory reset
- environment rebuild
- configuration recovery

This hierarchy prevents model-level observations from being presented as system-level impact without supporting Evidence.

---

# Evaluation data strategy

The lab intentionally combines multiple evidence and data sources.

No single Dataset class is expected to represent the full attack surface.

---

## First-party empirical Evidence

Authorized observations generated from systems built, operated, or evaluated by the project.

This may include Evidence from production-grade systems where testing and publication are authorized.

Where required for public release, sensitive information is sanitized while preserving the security-relevant properties of the Evidence.

Examples may include:

- interaction traces
- transcripts
- model outputs
- security events
- application behavior
- authorization decisions
- Control decisions
- infrastructure observations

First-party Evidence must preserve its provenance.

---

## Production-derived sanitized Evidence

Production-derived Evidence may provide security realism that is difficult to reproduce artificially.

Before public use, such Evidence must be reviewed for:

- customer data
- personally identifiable information
- credentials
- secrets
- private network information
- proprietary identifiers
- sensitive infrastructure details
- contractual restrictions

Sanitization should preserve the technical property required to support the security claim.

---

## Real-world public data

Datasets, corpora, benchmarks, and research artifacts may be obtained from reputable public sources and research repositories.

Potential sources may include:

- academic repositories
- security research projects
- Hugging Face datasets
- Kaggle datasets
- vendor evaluation datasets
- government repositories
- standards-related repositories
- open-source security benchmarks

Before use, they should be evaluated for:

- provenance
- licensing
- quality
- relevance
- age
- representativeness
- duplication
- contamination
- collection methodology
- known limitations

Public availability is not equivalent to validation.

---

## Lab-generated empirical Evidence

The lab generates Evidence through controlled execution of real systems.

These may include:

- production-grade hosted LLMs
- local open-weight LLMs
- RAG applications
- enterprise agents
- MCP-enabled agents
- memory-enabled agents
- AI coding agents
- voice AI systems
- multimodal systems
- authentication systems
- authorization systems
- tool services
- databases
- sandboxes
- network environments
- cloud infrastructure

This Evidence captures actual system behavior under security evaluation conditions created specifically for the lab.

Lab-generated does not mean synthetic.

If a real model, real agent, real tool, real database, real authorization layer, and real execution environment participate in the experiment, the resulting telemetry is empirical Evidence generated by the lab.

---

## Adversarially generated and synthetic data

Generated data is used where it improves:

- attack variation
- mutation coverage
- multilingual coverage
- code-switching coverage
- edge-case coverage
- rare-event testing
- long-context testing
- obfuscation testing
- transformation testing
- privacy-safe reproduction
- deterministic regression
- coverage of conditions not readily available in public Datasets

Generated data retains provenance and generation metadata so it cannot be mistaken for naturally observed real-world data.

Where generated attacks are derived from an existing Case or Evaluation Sample, their lineage should be preserved.

For example:

```text
Original Sample
PI-S-017
        ↓
multilingual mutation
        ↓
encoding mutation
        ↓
long-context mutation
        ↓
New Evaluation Sample
PI-S-017-M03
```

---

## Deterministic reference fixtures

Deterministic fixtures provide known system states against which the evaluation framework itself can be tested.

Their purpose is not to imitate the full complexity of production AI systems.

Their purpose is to establish:

- evaluator correctness
- repeatability
- expected state transitions
- scoring correctness
- Evidence integrity
- regression behavior
- fork-safe CI execution

For example, a deterministic authorization target may guarantee:

```text
request A → ALLOW
request B → DENY
```

If the evaluator reports otherwise, the evaluator itself is defective.

Results from deterministic fixtures and results from production-grade AI systems must remain distinguishable.

---

# Evaluation modes

The same evaluation framework may operate across multiple modes.

## Deterministic validation

Used to validate:

- framework correctness
- state tracking
- Evidence capture
- scoring
- Control instrumentation
- regression logic

## Controlled model evaluation

Used to evaluate:

- local open-weight models
- hosted production-grade models
- model behavior under controlled configurations

## System evaluation

Used to evaluate:

- complete RAG systems
- agents
- MCP systems
- memory systems
- coding agents
- voice systems
- multimodal systems

## Control evaluation

Used to determine whether a security Control:

- prevents attack progression
- restricts privileges
- blocks execution
- prevents external effect
- detects compromise
- contains compromise
- supports recovery
- preserves legitimate functionality

## Cross-layer evaluation

Used to evaluate attacks that move through multiple system layers.

For example:

```text
malicious retrieved document
        ↓
prompt injection
        ↓
agent manipulation
        ↓
tool request
        ↓
authorization
        ↓
execution
        ↓
network effect
```

## Remediation evaluation

Used to compare behavior before and after security Controls or system architecture change.

## Regression evaluation

Used to determine whether previously fixed security properties remain protected.

---

# Scoring principles

Metrics must be derived from clearly defined states and explicit denominators.

Possible metrics include:

- Model Compromise Rate
- Policy Violation Rate
- Attack Success Rate
- Action Attempt Rate
- Unauthorized Authorization Rate
- Unauthorized Execution Rate
- External Effect Rate
- Detection Rate
- Containment Rate
- Recovery Rate
- Benign Task Success Rate
- False Refusal Rate

Where applicable, operational metrics may also include:

- latency
- token usage
- cost
- resource consumption

A metric must define its numerator and denominator.

For example:

```text
Unauthorized Execution Rate
=
Runs with unauthorized execution observed
/
valid attack Runs in which unauthorized execution was possible
```

The denominator must not silently include:

- invalid Runs
- unsupported Cases
- infrastructure failures
- unavailable telemetry

unless the metric definition explicitly requires them.

---

# Control effectiveness

Control effectiveness must not be reduced to a simple statement such as:

```text
attack blocked
```

The evaluation should identify **where** progression stopped.

For example:

```text
Model compromised
        ↓
Action attempted
        ↓
Authorization Control denied
        ↓
No execution
```

differs from:

```text
Model compromised
        ↓
Authorization granted
        ↓
Execution attempted
        ↓
Sandbox Control blocked execution
```

which also differs from:

```text
Model compromised
        ↓
Execution completed
        ↓
Egress Control blocked transmission
```

All three may result in:

```text
No external effect
```

but the security architecture behaved differently.

The Trajectory and Evidence must preserve the exact enforcement point.

---

# Benign controls

Adversarial security evaluation must not ignore legitimate functionality.

Security Controls may reduce attack success while also damaging normal system operation.

The lab therefore tracks benign behavior where appropriate.

For example:

```text
Before Control:

Attack Success Rate = 40%
Benign Task Success Rate = 98%
```

```text
After Control:

Attack Success Rate = 2%
Benign Task Success Rate = 51%
```

The Control reduced attack success but introduced substantial functionality loss.

That is not equivalent to a clean security improvement.

Security evaluation should therefore measure both:

```text
security effectiveness
```

and:

```text
utility preservation
```

where the tested system requires both.

---

# Reproducibility contract

A defensible evaluation should preserve enough information for another qualified engineer to understand:

```text
what was tested
which data was available
which exact Samples were used
which Target was used
which Environment was used
which Controls were active
which Control versions were active
which Control configurations were active
which code version executed
which model/provider executed
what happened
which Evidence supports the result
how the result was scored
```

Perfect reproduction may not always be possible for external hosted models whose behavior changes over time.

When perfect reproduction is impossible, the evaluation should preserve enough metadata to reconstruct the original conditions as closely as possible and clearly document the limitation.

---

# Evidence retention and public release

Evidence should be retained according to its sensitivity and value.

Possible classifications include:

```text
public
sanitized-public
restricted
private
ephemeral
```

Public release must never depend on exposing:

- customer identity
- private production addresses
- phone numbers
- credentials
- tokens
- API keys
- proprietary prompts
- proprietary source code
- sensitive topology
- private logs
- personal data

A sanitized public engineering twin may reproduce the security property without reproducing the sensitive production artifact.

---

# Core invariants

The Evaluation Data Model is governed by the following invariants.

## Invariant 1

> Security claims must not exceed the Evidence available to support them.

## Invariant 2

> Model compromise does not automatically imply system compromise.

## Invariant 3

> Action attempt does not imply authorization.

## Invariant 4

> Authorization does not imply execution.

## Invariant 5

> Execution does not automatically imply external effect.

## Invariant 6

> Absence of telemetry does not prove absence of impact.

## Invariant 7

> Generated Evidence must remain distinguishable from observed real-world Evidence.

## Invariant 8

> Dataset identity does not replace exact Evaluation Sample identity.

## Invariant 9

> Evaluation Samples and Cases are independently reusable and are bound during execution.

## Invariant 10

> Control identity, Control configuration, and Control activation state must remain distinguishable.

## Invariant 11

> A Remediation is not complete until its security effect has been retested.

## Invariant 12

> Fixed security properties should become Regression coverage where appropriate.

## Invariant 13

> Historical Evidence must remain attributable to the exact Run that produced it.

## Invariant 14

> Invalid or interrupted Runs must not be interpreted as successful security Controls.

## Invariant 15

> A security Control should be evaluated at its actual enforcement point, not inferred solely from final model output.

---

# Relationship to the Three Failure Domains

The Evaluation Data Model supports the lab's Three Failure Domains without collapsing them into a single score.

---

## Boundary

Boundary asks:

```text
Where can untrusted influence enter?
```

Relevant Evidence may include:

- user input
- retrieved content
- repository content
- tool output
- MCP output
- memory
- APIs
- voice
- multimodal input
- network-originated content

Boundary evaluation records the source, transformation path, and trust relationship of untrusted influence.

---

## Grounding

Grounding asks:

```text
Can untrusted influence redirect model or system reasoning away from intended behavior?
```

Relevant Evidence may include:

- instruction override
- context poisoning
- model compromise
- sensitive disclosure
- unsafe reasoning
- malicious tool selection
- malicious argument construction

A Grounding failure describes manipulation of model or system decision behavior.

It does not automatically establish external impact.

---

## Containment

Containment asks:

```text
What can a compromised or manipulated model actually reach and change?
```

Relevant Evidence may include:

- identity
- permissions
- authorization
- tool scope
- filesystem access
- sandbox policy
- process restrictions
- network egress
- credential access
- human approval
- kill switches

A Grounding failure can occur without a Containment failure.

For example:

```text
Prompt injection succeeds
        ↓
Model attempts unauthorized action
        ↓
Authorization Control denies request
        ↓
No execution
        ↓
No external effect
```

The model was compromised.

The system contained the compromise.

Both facts belong in the final result.

---

# Final evaluation path

The assurance path is:

```text
DATASET / CORPUS
        ↓
EVALUATION SAMPLE
        │
        │
CASE ───┼───────────────┐
        │               │
        │               │
TARGET ─┼──────────────► RUN
        │               ▲
        │               │
EVALUATION ENVIRONMENT ─┤
        │               │
        ▼               │
   CONTROL(S) ──────────┘
                        │
                        ▼
                   TRAJECTORY
                        ↓
                     EVIDENCE
                        ↓
                      OUTCOME
                        ↓
                    ASSESSMENT
                        ↓
                      FINDING
                        ↓
                   REMEDIATION
                        ↓
                      RETEST
                        ↓
                    REGRESSION
                        ↓
                     CI GATE
```

At runtime, the critical security path is:

```text
UNTRUSTED INFLUENCE
        ↓
INPUT / CONTEXT BOUNDARY
        ↓
MODEL / AGENT
        ↓
ACTION ATTEMPT
        ↓
AUTHORIZATION
     ↙         ↘
   DENY       ALLOW
    ↓           ↓
CONTAINED    EXECUTION
                 ↓
          EXTERNAL EFFECT
```

Deterministic Controls may intervene at multiple points:

```text
untrusted input
      ↓
context Control
      ↓
model / agent
      ↓
tool-scope Control
      ↓
authorization Control
      ↓
sandbox Control
      ↓
filesystem / process Control
      ↓
network / egress Control
      ↓
external effect
      ↓
detection / containment / recovery Controls
```

The assurance process then asks:

```text
What happened?
        ↓
Can we prove it?
        ↓
Where did attack progression reach?
        ↓
Which security property failed?
        ↓
Which Control failed, succeeded, or was absent?
        ↓
What was the root cause?
        ↓
What changed during Remediation?
        ↓
Did the Retest change the security Outcome?
        ↓
Can Regression prevent recurrence?
```

---

# Core invariant

The central invariant of the Evaluation Data Model is:

> Security claims must not exceed the Evidence available to support them.

A model compromise may demonstrate a Grounding failure.

An unauthorized action attempt may demonstrate that model behavior crossed into a consequential system path.

An authorization denial may demonstrate successful Containment by an authorization Control.

A sandbox denial may demonstrate successful execution containment after authorization.

An egress denial may demonstrate containment after local execution.

Unauthorized authorization may demonstrate a Control failure.

Execution Evidence may demonstrate successful privilege use.

External-effect Evidence may demonstrate realized impact.

Detection Evidence may demonstrate that monitoring identified the event.

Containment Evidence may demonstrate that compromise occurred without allowing unrestricted system impact.

Recovery Evidence may demonstrate that affected state was restored after the incident.

The Evaluation Data Model exists to preserve these distinctions from Dataset provenance and exact Evaluation Samples through Case definition, Campaign execution, Target and Environment configuration, Control state, Run execution, Trajectory reconstruction, Evidence collection, Outcome normalization, Assessment, Finding, Remediation, Retest, Regression, and release gating.