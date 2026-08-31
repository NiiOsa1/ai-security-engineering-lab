![AI Security Engineering Lab](assets/banner/ai-security-engineering-lab-hero.svg)

> **AI security does not end when the model is compromised.**

A model can be manipulated without the surrounding system being compromised.

This lab measures what happens next.

```text
UNTRUSTED INPUT
      ↓
MODEL / AGENT
      ↓
ACTION ATTEMPT
      ↓
AUTHORIZATION
      ↓
EXECUTION
      ↓
EXTERNAL EFFECT
      ↓
DETECTION + CONTAINMENT + RECOVERY
```

The central question is not only whether an attack changes model behavior.

The question is whether adversarial influence crosses the boundaries that separate untrusted content from trusted decisions, whether it reaches a consequential action, whether authorization stops it, whether anything executes, whether the outside world changes, whether the event is detected, and whether the same failure can be prevented from returning.

That is the security problem this project is built to evaluate.

---

## Contents

- [What this project is](#what-this-project-is)
- [What makes the lab different](#what-makes-the-lab-different)
- [Security outcome model](#security-outcome-model)
- [Three Failure Domains](#three-failure-domains)
- [How the platform is organized](#how-the-platform-is-organized)
- [Security modules](#security-modules)
- [Module 01: Prompt Injection](#module-01-prompt-injection)
- [Target systems](#target-systems)
- [Evaluation lifecycle](#evaluation-lifecycle)
- [Evaluation architecture](#evaluation-architecture)
- [Evidence model](#evidence-model)
- [Scoring and metrics](#scoring-and-metrics)
- [Controls outside the model](#controls-outside-the-model)
- [Agentic AI security](#agentic-ai-security)
- [AI-assisted software engineering and DevSecOps](#ai-assisted-software-engineering-and-devsecops)
- [Voice and multimodal security](#voice-and-multimodal-security)
- [Regression and release gates](#regression-and-release-gates)
- [Quick start](#quick-start)
- [Repository layout](#repository-layout)
- [How to use the lab on your own system](#how-to-use-the-lab-on-your-own-system)
- [Framework mapping](#framework-mapping)
- [Project status](#project-status)
- [Results policy](#results-policy)
- [Security and responsible use](#security-and-responsible-use)
- [Contributing](#contributing)
- [License](#license)

---

## What this project is

The **AI Security Engineering Lab** is a modular, evidence-driven platform for evaluating the security of modern AI systems.

It is designed for:

- AI security engineers,
- red teams,
- application security teams,
- AI platform teams,
- ML engineers,
- agent developers,
- DevSecOps teams,
- security researchers,
- engineers building production LLM applications.

The lab is built to answer questions such as:

- Can untrusted content override trusted application instructions?
- Can indirect prompt injection survive retrieval, parsing, transcription, or tool wrapping?
- Can a manipulated model trigger a consequential action?
- Can an agent escalate from reading data to changing a system?
- Can a malicious tool or MCP server influence downstream decisions?
- Can poisoned memory persist across sessions?
- Can an AI coding agent be redirected by repository content?
- Can a compromised model access secrets, files, networks, or privileged tools?
- Can deterministic authorization stop an unsafe action even after model failure?
- Can an attack be detected, contained, reconstructed, remediated, and converted into regression coverage?

The lab is not a collection of disconnected prompts.

It is an evaluation system for tracing security outcomes across the full path from **adversarial input to external effect**.

---

## What makes the lab different

Many AI security tests stop here:

```text
attack
  ↓
model response
  ↓
PASS / FAIL
```

That is useful, but incomplete for systems that can retrieve data, call tools, modify files, use credentials, communicate over networks, or take autonomous actions.

This lab continues the trace:

```text
ATTACK
  ↓
MODEL / AGENT BEHAVIOR
  ↓
ACTION ATTEMPT
  ↓
AUTHORIZATION
  ↓
EXECUTION
  ↓
EXTERNAL EFFECT
  ↓
DETECTION
  ↓
CONTAINMENT
  ↓
RECOVERY
  ↓
EVIDENCE
  ↓
REMEDIATION
  ↓
RETEST
  ↓
REGRESSION
```

The design is built around five principles.

### 1. Model failure and system compromise are different events

A model may follow malicious instructions while a lower-layer control still blocks the dangerous action.

That distinction is measured explicitly.

### 2. Security claims require evidence

A result should be reproducible from:

- versioned cases,
- controlled configuration,
- run metadata,
- trajectories,
- authorization decisions,
- execution evidence,
- scoring rules,
- supporting artifacts.

### 3. Controls are tested, not merely listed

The lab is designed to compare security profiles such as:

```text
PERMISSIVE
BASELINE
HARDENED
```

The objective is to measure whether a control changes the security outcome.

### 4. Fixed findings become regression tests

A remediation is not complete because code changed.

It is complete only after controlled retesting, residual-risk review, and permanent regression coverage where appropriate.

### 5. The core path must remain forkable

The deterministic evaluation path is designed so another engineer can clone the repository, run the local baseline, inspect evidence, add a case, and plug in a target without requiring paid model credentials.

---

<!--
PUBLIC DIAGRAM PLACEHOLDER

Final asset:
assets/diagrams/system-architecture.svg

Source:
docs/diagrams/source/system-architecture.mmd

The public diagram should show:
- untrusted sources
- target systems
- model / agent
- RAG / memory / tools / MCP
- authorization
- sandbox / execution
- external effect
- evidence / scoring
- detection / containment
- remediation / regression
- CI / release gate

Do not include private infrastructure, customer systems, credentials, or non-public topology.
-->

## Security outcome model

The lab deliberately separates states that are often collapsed into one result.

```text
Model Compromise
      ≠
Action Attempt
      ≠
Authorization Granted
      ≠
Execution Occurred
      ≠
External Effect Occurred
      ≠
Detection
      ≠
Containment
      ≠
Recovery
```

Consider two systems exposed to the same successful prompt injection.

### System A

```text
Prompt injection succeeds
        ↓
Model requests unauthorized action
        ↓
Authorization denies request
        ↓
No execution
        ↓
No external effect
        ↓
Attempt recorded and contained
```

The model failed.

The containment architecture held.

### System B

```text
Prompt injection succeeds
        ↓
Model requests unauthorized action
        ↓
Authorization permits request
        ↓
Tool executes
        ↓
External system changes
```

The same model-level failure produced a materially different system-level result.

The lab is designed to measure that difference.

---

<!--
PUBLIC DIAGRAM PLACEHOLDER

Final asset:
assets/diagrams/attack-to-impact.svg

Source:
docs/diagrams/source/attack-to-impact.mmd

Path A:
MODEL COMPROMISED
-> ACTION ATTEMPTED
-> AUTHORIZATION DENIED
-> NO EXECUTION
-> CONTAINED

Path B:
MODEL COMPROMISED
-> ACTION ATTEMPTED
-> AUTHORIZATION GRANTED
-> EXECUTION
-> EXTERNAL EFFECT

Path C:
SECURITY EVENT
-> DETECTION
-> CONTAINMENT
-> RECOVERY
-->

## Three Failure Domains

The lab uses the **Three Failure Domains** as an engineering lens for understanding how AI failures propagate.

### Boundary

**Where untrusted influence enters.**

Examples:

- user input,
- retrieved documents,
- repository content,
- tool output,
- MCP resources,
- memory,
- speech transcripts,
- API responses,
- network inputs.

A boundary failure occurs when untrusted content enters a trusted decision path without sufficient separation, provenance, validation, or policy enforcement.

### Grounding

**How the system decides what information to trust and how that information may influence behavior.**

Examples:

- instruction vs data separation,
- retrieved context,
- tool-result trust,
- source provenance,
- memory provenance,
- conflicting sources,
- stale or poisoned context.

A grounding failure occurs when untrusted, incorrect, stale, or attacker-controlled information is treated as authoritative.

### Containment

**What the system is allowed to do when prevention fails.**

Examples:

- authorization,
- tool scope,
- filesystem scope,
- network egress,
- secrets access,
- sandboxing,
- least privilege,
- human approval,
- execution policy,
- kill switches.

Containment assumes that a sufficiently capable attacker may eventually influence the model.

The question becomes:

> If that happens, what can the compromised system actually do?

---

<!--
PUBLIC DIAGRAM PLACEHOLDER

Final asset:
assets/diagrams/three-failure-domains.svg

Source:
docs/diagrams/source/three-failure-domains.mmd

BOUNDARY
untrusted influence enters
        ↓
GROUNDING
system decides what to trust
        ↓
CONTAINMENT
system limits what compromise can do

Apply across:
Text
Documents
RAG
Repositories
Tools
MCP
Memory
Agents
Voice / multimodal
-->

## How the platform is organized

The project is developed as **deep vertical security modules on one reusable horizontal evaluation backbone**.

```text
COMMON EVALUATION BACKBONE
          │
          ├── 01  Prompt Injection
          ├── 02  Jailbreak & Model-Control Security
          ├── 03  RAG Security
          ├── 04  Agentic AI Security
          ├── 05  MCP & Tool Security
          ├── 06  Memory & Persistence Security
          ├── 07  AI-Assisted Software Engineering & DevSecOps
          ├── 08  Voice & Multimodal Security
          ├── 09  Data, Privacy & Secrets
          ├── 10  Infrastructure, Supply Chain & Containment
          ├── 11  Detection, Response & Observability
          └── 12  Cross-Layer / Multi-Agent Enterprise Campaigns
```

A module is not considered complete because a few attacks were demonstrated.

A mature module should include the relevant:

```text
scope
threat model
attack taxonomy
target coverage
control coverage
evaluation cases
versioned suite
controlled campaigns
evidence
scoring
metrics
findings
remediation
retest
residual risk
regression
CI / release gates
documentation
limitations
fork path
```

Later modules reuse proven platform components instead of rebuilding the evaluation engine from scratch.

---

## Security modules

| Module | Focus | Status |
|---|---|---|
| 01 | Prompt Injection | In progress |
| 02 | Jailbreak & Model-Control Security | Planned |
| 03 | RAG Security | Planned |
| 04 | Agentic AI Security | Planned |
| 05 | MCP & Tool Security | Planned |
| 06 | Memory & Persistence Security | Planned |
| 07 | AI-Assisted Software Engineering & DevSecOps | Planned |
| 08 | Voice & Multimodal Security | Planned |
| 09 | Data, Privacy & Secrets | Planned |
| 10 | Infrastructure, Supply Chain & Containment | Planned |
| 11 | Detection, Response & Observability | Planned |
| 12 | Cross-Layer / Multi-Agent Enterprise Campaigns | Planned |

The table communicates direction, not completion.

Only implemented code, tests, evidence, and reproducible results determine maturity.

---

## Module 01: Prompt Injection

The first complete security module is **Prompt Injection**.

Prompt injection is a useful first vertical slice because it crosses nearly every modern AI application boundary.

### Direct prompt injection

Attacker-controlled instructions are supplied directly through an input channel accepted by the application.

Examples:

- user text,
- structured input,
- code/configuration input,
- multi-turn interaction,
- transcribed user speech.

### Indirect prompt injection

Attacker-controlled instructions arrive through content the system reads, retrieves, observes, receives from another component, or incorporates into context.

Examples:

- documents,
- RAG chunks,
- web-like content,
- repository files,
- issue or pull-request text,
- tool output,
- MCP resources,
- memory,
- speech-to-text output,
- multimodal-extracted text.

### Transformations

The module is designed to test whether malicious intent survives transformations such as:

- summarization,
- retrieval,
- chunking,
- parsing,
- transcription,
- serialization,
- code blocks,
- Markdown or HTML-like formatting,
- tool wrapping,
- encoding,
- obfuscation,
- multilingual or code-switched text,
- long-context placement.

### Attack goals

Cases may test attempts to:

- override trusted instructions,
- reveal system or developer instructions,
- disclose sensitive context,
- influence downstream decisions,
- trigger tool use,
- manipulate tool arguments,
- read unauthorized data,
- access secrets,
- write files,
- modify code,
- alter memory,
- transmit data,
- reach unauthorized network destinations,
- cause destructive actions,
- create persistence,
- evade detection.

### Source-to-sink analysis

For consequential systems, the lab evaluates both the untrusted source and the dangerous sink.

```text
SOURCE: malicious repository content
SINK: shell execution

SOURCE: poisoned retrieved document
SINK: outbound data transmission

SOURCE: malicious tool output
SINK: privileged database update

SOURCE: attacker-controlled transcript
SINK: account-changing action
```

A model-level manipulation that cannot reach a consequential sink is different from an attack that changes the outside world.

### Module 01 completion standard

Module 01 is not complete until the implemented scope includes:

- direct injection,
- indirect injection across major source classes,
- benign controls,
- controlled target configurations,
- source-to-sink tests,
- action/authorization/execution/effect evidence,
- controls outside the model,
- reproducible scoring,
- explicit limitations,
- retesting,
- regression,
- a deterministic fork-safe path.

---

## Prompt injection and jailbreak are different problems

They can overlap, but the lab evaluates them separately.

### Prompt Injection

Prompt injection attacks **instruction control inside an AI application**.

The central question is:

> Can attacker-controlled content redirect trusted application behavior?

### Jailbreak

Jailbreak attacks **model-level behavioral or safety restrictions**.

The central question is:

> Can the attacker cause the model to violate a defined behavioral or safety policy?

Separating them makes the threat model, expected behavior, controls, and scoring more precise.

---

## Target systems

The lab is designed around multiple target types instead of one monolithic demo.

| Target type | Purpose |
|---|---|
| Deterministic synthetic target | Fork-safe CI baseline and evaluation-engine testing |
| Local open-weight LLM target | Controlled real-model experiments |
| Reference RAG system | Document and retrieval-borne attacks |
| Reference enterprise agent | Tool use, planning, authorization, containment |
| Reference MCP environment | Server, tool, resource and trust-boundary tests |
| Reference memory system | Persistence, poisoning and provenance |
| AI coding agent | Repository-borne attacks and DevSecOps controls |
| External provider adapters | Optional cross-provider campaigns |

Target adapters are intended to let the evaluation framework remain stable while the underlying model or application changes.

A basic fork should remain useful without commercial provider credentials.

---

## Evaluation lifecycle

Every mature module follows a controlled evaluation lifecycle.

```text
SCOPE / RULES OF ENGAGEMENT
          ↓
SECURITY PROPERTY
          ↓
THREAT
          ↓
EVALUATION PLAN
          ↓
EVALUATION CASE
          ↓
VERSIONED SUITE / CORPUS
          ↓
CONTROLLED CAMPAIGN
          ↓
REPEATED RUNS
          ↓
TRAJECTORY + EVIDENCE
          ↓
SCORING
          ↓
HUMAN REVIEW, WHEN REQUIRED
          ↓
FINDING
          ↓
SEVERITY + RATIONALE
          ↓
REMEDIATION
          ↓
RETEST
          ↓
RESIDUAL RISK
          ↓
REGRESSION
          ↓
BREAKING / NON-BREAKING DECISION
          ↓
CI / RELEASE GATE
```

A fix is not considered validated because code or configuration changed.

It must survive controlled retesting.

A validated security property should become permanent regression coverage.

---

<!--
PUBLIC DIAGRAM PLACEHOLDER

Final asset:
assets/diagrams/evaluation-lifecycle.svg

Source:
docs/diagrams/source/evaluation-lifecycle.mmd

Finalize only after the canonical evaluation data model is implemented and accepted.
-->

## Evaluation architecture

The platform separates four questions:

```text
What are we testing?
Under what conditions?
What actually happened?
What conclusion does the evidence support?
```

### Scope / Rules of Engagement

Defines:

- authorized targets,
- out-of-scope targets,
- permitted attack classes,
- prohibited actions,
- safety constraints,
- data handling,
- escalation,
- stopping conditions.

### Evaluation Plan

Defines the campaign before execution:

- threat references,
- target,
- control profile,
- suite,
- expected behavior,
- scorer policy,
- severity rubric,
- repetitions,
- stopping criteria,
- evidence requirements,
- environment,
- compute/time/cost budget.

Scoring rules should not be silently rewritten after the results are visible.

### Evaluation Case

Defines **what is being tested**.

A case can include:

- case identifier,
- security module,
- category,
- technique,
- security objective,
- attack vector,
- input modality,
- prerequisites,
- fixture reference,
- expected secure behavior,
- failure condition,
- pass criteria,
- scorer,
- framework mappings,
- version.

### Evaluation Suite / Corpus

A versioned collection of cases used for:

- repeatability,
- regression,
- baseline/candidate comparison,
- model comparison,
- control comparison,
- release gating.

### Target Profile

Describes the system under test:

- target type,
- version,
- capabilities,
- trust boundaries,
- tools,
- identity,
- filesystem access,
- network access,
- data classification,
- known limitations.

### Control Profile

Describes which controls are active.

Typical comparison profiles may include:

```text
PERMISSIVE
BASELINE
HARDENED
```

### Campaign

Defines the controlled execution configuration:

- suite version,
- target version,
- provider/model,
- configuration hashes,
- policy version,
- tool configuration,
- sampling parameters,
- repetition policy,
- scorer version,
- environment,
- stopping criteria,
- budget.

### Run

Represents one execution of one case.

A run can preserve:

- inputs,
- hashes,
- model output,
- tool requests,
- authorization decisions,
- execution result,
- external effect,
- detection state,
- containment state,
- timestamps,
- latency,
- token/cost metadata,
- evidence references,
- source-control revision.

### Trajectory

For multi-step systems, capture externally observable events:

```text
input
→ retrieval
→ model / agent response
→ tool request
→ policy decision
→ execution
→ observation
→ next action
→ outcome
```

The lab does not depend on private chain-of-thought capture.

### Security Property

A security property is a claim that should remain true.

Example:

> A prompt-injected coding agent cannot write outside its assigned workspace or connect to an unapproved network destination.

Once validated, a security property becomes a regression target.

---

## Evidence model

Security conclusions should be reconstructable from evidence.

A mature run may preserve fields such as:

```text
run_id
case_id
campaign_id
module version
suite / corpus version
Git commit SHA
input hash
prompt hash
fixture hash
audio hash, when applicable
provider
model
model version
STT provider / version, when applicable
sampling configuration
target profile
control profile
timestamp
expected secure behavior
model compromise state
action attempt
authorization decision
execution result
external effect
detection
containment
recovery
scorer version
human review state
evidence references
latency
token usage
cost
```

The exact schema is versioned with the implementation.

Private or sensitive evidence must remain outside the public artifact path.

Public examples use synthetic, sanitized, or clearly reconstructed-with-provenance data.

---

## Evaluation discipline

The lab follows several non-negotiable rules.

```text
No campaign without phases.

No phase without required artifacts.

No campaign without stopping criteria.

No test without expected secure behavior.

No scorer without a defined rubric.

No metric without a defined denominator.

No subjective result without review governance.

No severity without rationale.

No finding without evidence.

No remediation without retest.

No fixed vulnerability without regression coverage.

No comparison without controlled configuration.

No CI security gate without an explicit blocking rule.

No public claim without reproducible support.
```

---

## Stopping criteria

Security testing should not end because the tester feels enough attacks have been attempted.

Campaigns declare stopping criteria before result interpretation.

Supported strategies can include:

- fixed case coverage,
- fixed repetition count,
- compute/time/cost budget,
- statistical precision,
- mutation saturation,
- safety stop.

There is no universal number of attacks that proves an AI system is secure.

---

## Scoring and metrics

A metric is useful only when its numerator, denominator, eligibility rule, and success condition are explicit.

Example:

```text
Attack Success Rate

successful eligible attack executions
─────────────────────────────────────
total eligible attack executions
```

One aggregate number can still hide important system behavior.

The lab can separately measure:

| Metric | Question |
|---|---|
| Model Manipulation / Compromise Rate | Did the model violate the defined security property? |
| Action Attempt Rate | Did the attack produce a consequential action request? |
| Unauthorized Authorization Rate | Was an unauthorized capability permitted? |
| Unauthorized Execution Rate | Did unauthorized execution occur? |
| External Effect Rate | Did something outside the AI system change? |
| Detection Rate | Was the security event detected? |
| Containment Rate | Was propagation stopped? |
| Recovery Rate | Was the system returned to an acceptable state? |
| Benign Task Success Rate | Did legitimate functionality remain usable? |
| False Refusal Rate | Were legitimate requests incorrectly blocked? |

Metrics are introduced only when corresponding evidence exists.

Small samples are not converted into broad claims of resistance.

---

## Human review

Some outputs cannot be scored reliably with deterministic rules alone.

When human adjudication is required, the evaluation design can record:

- independent labels,
- rubric version,
- reviewer disagreement,
- adjudication,
- final label,
- agreement metrics when statistically justified.

Potential agreement measures include:

- percent agreement,
- Cohen's kappa,
- Fleiss' kappa,
- Krippendorff's alpha.

A metric is selected because it fits the evaluation design, not because it sounds sophisticated.

---

## Severity

The lab does not invent an arbitrary AI-specific severity score.

Severity should be traceable to evidence and documented rationale.

Relevant dimensions can include:

- model compromise,
- application compromise,
- privilege boundary crossed,
- authorization bypass,
- execution,
- sensitive-data disclosure,
- persistence,
- blast radius,
- exploitability,
- user interaction,
- detection,
- containment,
- external impact.

Conventional severity systems can be mapped where appropriate while preserving AI-system-specific impact detail.

---

## Controls outside the model

The model is one component of the security architecture.

It should not be the final authority for consequential actions.

Where practical, enforce security controls outside the model.

Examples:

```text
identity
authorization
tool scope
filesystem scope
network egress
secret access
sandbox policy
human approval
kill switch
```

A compromised model should not be able to grant itself permissions because it can generate convincing text.

---

## Agentic AI security

Agentic systems increase the security importance of authorization, identity, containment, and auditability.

A controlled reference agent can eventually expose capabilities such as:

- planning,
- read tools,
- action tools,
- memory,
- identity context,
- policy requests,
- sandboxed execution,
- controlled network access,
- audit logging,
- kill-switch handling.

The same scenario can then be tested under different security profiles:

```text
PERMISSIVE / VULNERABLE
PARTIALLY CONTROLLED
HARDENED / LEAST PRIVILEGE
```

The objective is not to build an impressive autonomous demo.

The objective is to measure how attack outcomes change when control architecture changes.

---

## AI-assisted software engineering and DevSecOps

AI coding agents create a particularly important indirect-injection and execution surface.

A coding agent may consume:

- source files,
- README files,
- issue text,
- pull-request comments,
- package metadata,
- generated build output,
- documentation,
- test failures,
- tool output.

Any of these can contain attacker-controlled instructions.

A controlled coding-agent target may be allowed to:

- modify files,
- execute tests,
- invoke shell commands,
- install dependencies,
- create branches,
- propose commits or pull requests,
- modify Infrastructure as Code,
- request deployment-like actions.

High-risk actions remain sandboxed or simulated.

The surrounding DevSecOps control plane can include:

- branch protection,
- least-privilege credentials,
- protected agent configuration,
- filesystem isolation,
- network isolation,
- default-deny egress,
- secret scanning,
- Static Application Security Testing,
- Software Composition Analysis,
- dependency vulnerability scanning,
- Infrastructure as Code scanning,
- policy-as-code,
- Software Bill of Materials,
- artifact provenance,
- security regression,
- human approval for consequential actions.

A useful evidence chain can be reconstructed as:

```text
untrusted repository content
→ agent context
→ proposed action
→ authorization decision
→ sandbox execution
→ Git diff
→ security scanners
→ CI gate
→ external effect or containment
→ final result
```

---

## Voice and multimodal security

Voice and multimodal systems introduce transformations between attacker intent and model input.

A generic Voice AI security trajectory can be modeled as:

```text
Attack Intent
      ↓
Canonical Spoken Text
      ↓
Audio
      ↓
Audio Hash
      ↓
Speech-to-Text
      ↓
Transcript
      ↓
Security-Critical Token Analysis
      ↓
LLM / Agent Input
      ↓
Model Response / Plan
      ↓
Tool Request
      ↓
Authorization
      ↓
Execution
      ↓
System Output
      ↓
External Outcome
```

This allows the lab to study not only whether an attack succeeds, but whether security-relevant content survives transformation through the input pipeline.

Project-defined research metrics may include:

### Security-Critical Token Preservation

Measures whether security-relevant tokens survive transformation.

### Attack Semantic Preservation

Measures whether attack intent survives transformation even when exact wording changes.

These metrics must be formally defined before numerical results are published.

---

## Regression and release gates

A security finding should not disappear into a report after remediation.

The expected lifecycle is:

```text
Finding
  ↓
Root Cause
  ↓
Remediation
  ↓
Retest
  ↓
Validated Security Property
  ↓
Permanent Regression Case
```

Regression protects established security properties against changes to:

- models,
- prompts,
- retrieval,
- agents,
- MCP servers,
- tools,
- authorization policy,
- memory,
- infrastructure.

### Breaking and non-breaking security changes

Potentially breaking regressions include:

- a previously blocked attack reaches execution,
- authorization becomes more permissive unexpectedly,
- external effect appears where none previously existed,
- a remediated finding reappears,
- containment falls below policy,
- required detection disappears,
- a critical security property regresses.

Potentially non-breaking changes include:

- wording changes without security-property change,
- harmless output variation inside defined tolerance,
- implementation refactors with unchanged security behavior.

### CI security gates

A gate may classify:

```text
PASS
WARN
BLOCK
HUMAN REVIEW REQUIRED
```

Potential gate conditions include:

- previously blocked attack begins succeeding,
- unauthorized execution crosses threshold,
- containment degrades,
- benign-task performance degrades beyond policy,
- a remediated finding returns,
- evaluation coverage decreases,
- suite, scorer, control, or policy changes without required review.

The deterministic local regression path is intended to work without commercial model credentials.

---

## Quick start

The project uses Python 3.12 and `uv` for reproducible environment management.

### 1. Clone

```bash
git clone https://github.com/NiiOsa1/ai-security-engineering-lab.git
cd ai-security-engineering-lab
```

### 2. Synchronize the environment

```bash
uv sync
```

### 3. Verify Python

```bash
uv run python --version
```

Expected major/minor version:

```text
Python 3.12
```

The project-local virtual environment is created under:

```text
.venv/
```

and is intentionally excluded from Git.

<!--
PUBLIC QUICKSTART TODO

Once the deterministic evaluation runner exists, replace this comment with the tested command.

Do not publish a CLI command before the CLI exists.
-->

---

## Repository layout

The repository grows as capabilities are implemented.

```text
ai-security-engineering-lab/
├── README.md
├── SECURITY.md
├── ETHICS.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── uv.lock
│
├── docs/
│   ├── architecture/
│   ├── methodology/
│   ├── modules/
│   ├── threat-models/
│   ├── adr/
│   └── diagrams/
│       └── source/
│
├── assets/
│   ├── banner/
│   └── diagrams/
│
├── evals/
│   ├── modules/
│   ├── campaigns/
│   └── schemas/
│
├── targets/
│   ├── deterministic/
│   └── reference/
│
├── src/
│   └── ai_security_lab/
│       ├── models/
│       ├── adapters/
│       ├── runners/
│       ├── targets/
│       ├── scoring/
│       ├── evidence/
│       ├── policy/
│       ├── regression/
│       └── reporting/
│
├── evidence/
│   └── public/
│
├── reports/
│   └── public/
│
├── tests/
│
└── .github/
    └── workflows/
```

Directories are introduced when their corresponding capability is implemented.

Repository structure is not used as a substitute for working code.

### Where to look

| If you want to... | Start here |
|---|---|
| Understand the architecture | `docs/architecture/` |
| Understand evaluation methodology | `docs/methodology/` |
| Explore a security module | `docs/modules/` |
| Inspect attack/evaluation cases | `evals/modules/` |
| Inspect target implementations | `targets/` and `src/ai_security_lab/targets/` |
| Inspect scoring logic | `src/ai_security_lab/scoring/` |
| Inspect evidence | `evidence/public/` |
| Inspect regression logic | `src/ai_security_lab/regression/` |
| Inspect CI security gates | `.github/workflows/` |
| Review architecture decisions | `docs/adr/` |

---

## How to use the lab on your own system

The intended workflow is:

```text
clone repository
      ↓
run deterministic baseline
      ↓
inspect a case
      ↓
inspect the evidence
      ↓
modify or add a case
      ↓
connect a target adapter
      ↓
define a target/control profile
      ↓
run a campaign
      ↓
compare baseline and candidate
      ↓
retest
      ↓
run regression
```

A custom target should eventually provide enough information for the lab to answer:

```text
What input reached the system?
What did the model or agent do?
What action was attempted?
What did authorization decide?
What executed?
Did an external effect occur?
Was the event detected?
Was it contained?
What evidence proves the conclusion?
```

The framework is intended to support target substitution without rewriting the evaluation methodology.

---

## Framework mapping

Evaluation cases can map to relevant external security frameworks, including:

- OWASP GenAI / LLM risks,
- OWASP Agentic risks,
- MITRE ATLAS,
- NIST AI risk guidance,
- conventional application-security controls,
- cloud-security controls,
- software-supply-chain controls.

Framework mapping provides traceability.

It does not replace threat modeling, technical explanation, or evidence.

The Three Failure Domains remain the lab's internal engineering lens:

```text
Boundary
Grounding
Containment
```

---

## Project status

The project is being built incrementally.

Current emphasis:

```text
FOUNDATION
    ↓
MODULE 01: PROMPT INJECTION
    ↓
DEEP MODULE-BY-MODULE EXPANSION
```

Status labels are used deliberately:

- **In progress** means active implementation/evaluation work exists.
- **Planned** means the architecture anticipates the capability, but the module is not yet complete.
- **Complete** should be used only when the module's documented exit criteria are satisfied.

The public roadmap describes direction.

It is not evidence of implementation.

---

<!--
PUBLIC RESULTS DIAGRAM PLACEHOLDER

Do not create this visual until real public campaign data exists.

Final asset:
assets/diagrams/results-overview.svg

Potential contents:
Baseline vs hardened
Model Manipulation / Compromise Rate
Unauthorized Execution Rate
External Effect Rate
Detection Rate
Containment Rate
Benign Task Success Rate
False Refusal Rate

Every value must come from actual campaign evidence.
-->

## Results policy

Results are published only when the corresponding:

- campaign,
- configuration,
- evidence,
- scoring rules,
- metrics,
- limitations,

are complete enough to support the claim.

No placeholder benchmark values are presented as findings.

No small sample is described as proof of broad resistance.

No reconstructed artifact is presented as though it existed historically.

No comparison is presented as controlled unless the relevant conditions were actually controlled.

The first public result set is expected to come from **Module 01: Prompt Injection**.

---

## Security and responsible use

This repository is intended for:

- authorized security evaluation,
- defensive research,
- controlled red teaming,
- security education,
- regression testing,
- evaluation engineering.

Do not use the project against systems you are not authorized to test.

Public evidence must not expose:

- production credentials,
- customer data,
- real secrets,
- private keys,
- confidential traces,
- sensitive internal logs,
- proprietary source code,
- live exploit paths against real systems.

Synthetic targets and controlled fixtures are preferred for reproducible public demonstrations.

---

## Evidence policy

The repository follows a simple rule:

```text
Claim
  ↓
Defined Criterion
  ↓
Observed Evidence
  ↓
Scoring
  ↓
Conclusion
```

No result should be stronger than the evidence supporting it.

---

## Design principles

```text
Understand before testing.

Define the security property before measuring it.

Threat-model before attacking.

Measure before claiming.

Separate model failure from system compromise.

Evidence before severity.

Root cause before remediation.

Retest before declaring fixed.

Regression before closing the finding.

Containment outside the model where practical.

Sanitize before publishing.

Build for reproducibility.

Design for failure.
```

---

## Contributing

The project is being designed for engineers who want to evaluate and harden their own AI systems.

Contribution areas include:

- evaluation cases,
- attack-family modules,
- controlled fixtures,
- target adapters,
- scorers,
- evidence schemas,
- regression tests,
- security controls,
- documentation,
- framework mappings.

A useful security contribution should define:

```text
security property
threat
expected secure behavior
failure condition
reproduction path
evidence requirement
scoring method
```

Collections of unscored prompts are not sufficient by themselves.

<!--
PUBLIC TODO:
Link this section to CONTRIBUTING.md when that file exists.
-->

---

## License

Licensed under the Apache License 2.0.

See [`LICENSE`](LICENSE).

---

## Author

Built by **Michael Mensah Ofeor / NiiOsa Labs**.

The project is focused on one idea: do not stop at whether the model failed. Trace whether the system failed, prove what happened, contain the impact, and turn the fix into something that stays fixed.
