ADR-0001: AI Security Engineering Lab and Evaluation Harness

Status

Accepted

Date

2026-09-04

Context

The project is evolving into a reusable AI security engineering platform for evaluating, hardening, and retesting modern AI systems.

The platform must support multiple target types, including:

language models

RAG systems

agents

MCP-enabled systems

coding agents

voice and multimodal systems

infrastructure and execution components

The project must preserve a strict distinction between:

model compromise

action attempt

authorization granted

execution occurred

external effect occurred

detection

containment

recovery

A prompt-only red-team framework is therefore insufficient.

The project also needs a clear distinction between the overall engineering project and the executable machinery that performs evaluations.

Decision

The project will remain named:

AI Security Engineering Lab

The executable evaluation core will be referred to as:

AI Security Evaluation Harness

The AI Security Engineering Lab is the broader engineering project.

The AI Security Evaluation Harness is the reusable execution and evaluation subsystem within that project.

The project lifecycle is:

attack
    ↓
measure
    ↓
evaluate controls
    ↓
capture evidence
    ↓
identify findings
    ↓
remediate
    ↓
retest
    ↓
regression

The harness must support evaluation of both vulnerable and hardened system configurations.

It must preserve enough information to determine:

what Target was evaluated

what exact evaluation material was used

what Evaluation Environment was active

what Controls were defined and configured

what Case was executed

what actions were attempted

what authorization decisions occurred

what execution occurred

what external effects occurred

what Evidence supports those conclusions

whether detection, containment, and recovery occurred

Primary Interfaces

The platform should evolve around reusable machine-accessible interfaces.

Primary interfaces are expected to include:

Python library and domain contracts

command-line interface

Target adapters and programmatic APIs

CI/CD integration

optional presentation and operational interfaces

The command-line and programmatic interfaces must remain usable without a graphical interface.

Target Integration

The harness does not require a user's source code to be embedded directly into the lab.

A Target may be:

a local Python application

a remote HTTP service

a hosted model

a RAG application

an MCP server

an agent framework

a coding agent

a voice system

another controlled execution environment

Target adapters provide the boundary between the harness and the system under evaluation.

The adapter architecture must allow new Target types to be added without redesigning the evaluation data model.

Dashboard Decision

A dashboard may be added later as a usability, visualization, reporting, or operational layer.

The dashboard is not part of the security source of truth.

The architecture must remain:

Python / CLI / API / CI
          ↓
Evaluation Harness
          ↓
Machine-readable evaluation records
          ↓
Evidence and results
          ↓
Optional Dashboard

The system must remain fully operable without the dashboard.

A dashboard must render or query evaluation records rather than inventing independent security state.

Source of Truth

Machine-readable evaluation records and captured Evidence are the authoritative source for evaluation results.

Presentation layers, dashboards, reports, and model-generated summaries are derived views.

They must not silently alter the underlying Evidence or security outcome.

Repository state, versioned contracts, evaluation records, and Evidence take precedence over conversational memory.

Forkability and Extensibility

The repository should remain forkable and useful without proprietary services.

A basic fork should eventually be able to:

clone repository
    ↓
install dependencies
    ↓
run deterministic reference evaluation
    ↓
inspect evidence
    ↓
modify or add a Case
    ↓
run a Campaign
    ↓
plug in a custom Target
    ↓
compare vulnerable and hardened states
    ↓
run regression

Paid model credentials must not be required for the deterministic baseline.

External model and service providers may be supported through optional adapters.

Alternatives Considered

Alternative 1: Rename the entire project to AI Security Evaluation Harness

Rejected.

The harness is only one component of the broader project.

The project also includes:

security architecture

reference Targets

Controls

threat models

evidence engineering

remediation

regression

infrastructure security

DevSecOps

teaching material

research modules

The name AI Security Engineering Lab better represents the full scope.

Alternative 2: Build primarily as a graphical dashboard

Rejected.

A dashboard-first architecture would make presentation a dependency of the security engine and weaken automation, CI/CD integration, reproducibility, and forkability.

Alternative 3: Build only an attack or jailbreak framework

Rejected.

Attack generation alone does not determine whether model manipulation results in authorization, execution, external effect, detection, containment, or recovery.

The project must evaluate system consequences and Controls, not only model responses.

Alternative 4: Build around one specific AI system

Rejected.

The lab must support multiple Target types through reusable contracts and adapters.

A single reference implementation may inform the architecture, but it must not define the limits of the platform.

Consequences

Positive

This decision provides:

a stable project identity

a precise name for the executable evaluation subsystem

separation between the security engine and user interface

reusable Target integration

compatibility with local, remote, and hosted systems

CI/CD-friendly operation

stronger forkability

space for future dashboards without coupling them to core security logic

a foundation for reproducible attack, control, evidence, remediation, and regression workflows

Costs

This architecture requires more engineering than a prompt-only testing tool.

It requires explicit contracts for:

Targets

Datasets

Evaluation Samples

Controls

Evaluation Environments

Cases

Campaigns

Runs

Trajectories

Evidence

Outcomes

Assessments

Findings

Remediations

Retests

Regressions

Adapters, evidence collection, and execution orchestration also require deliberate interface design.

These costs are accepted because they are necessary to support defensible system-level AI security evaluation.

Non-Goals of This Decision

This ADR does not decide:

the final dashboard technology

the final storage or database architecture

the final Target adapter protocol

the final CLI framework

the final execution engine

the final cloud provider

the Infrastructure as Code tool

the final model-based evaluation strategy

Those decisions require separate evidence and ADRs when their implementation requirements become concrete.

Follow-Up Decisions

Separate ADRs should be created when required for:

evaluation authority and evidence hierarchy

Target adapter contract

Control versus Evaluation Environment ownership

evaluation record persistence

deterministic versus model-based scoring

execution sandbox and containment architecture

Infrastructure as Code strategy

dashboard architecture

Public-Safe Scope

This ADR intentionally records only public architectural decisions.

It does not contain customer information, production-sensitive details, confidential implementation details, or private business strategy.

Decision Principle

The project exists to answer a stronger question than:

Can an attacker manipulate the model?

The engineering question is:

If the model is manipulated, what can the system actually authorize, execute, affect, detect, contain, recover from, and prove?