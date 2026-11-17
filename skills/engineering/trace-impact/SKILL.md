---
name: trace-impact
description: >-
  Analyze the impact of changing a function, interface, schema, field, API, or
  event contract. Trace dependencies, implementations, direct and transitive
  callers, affected behavior, and specific tests with source evidence. Use when
  users ask what a change would affect, which callers need updating, or where to
  test, including “ถ้าเปลี่ยน Order.status จะกระทบตรงไหนบ้าง”, “ไล่ dependencies”,
  and “blast radius”. Default to assessment, not implementation. For removal
  safety decisions use is-safe-to-remove; for detailed data migration plans use
  database-migration-planning.
---

# Trace impact

Explain what a proposed change affects, why, and how to verify the affected
behavior. Respond in the user's language. Ground conclusions in inspected code;
a list of matching names is not an impact analysis.

## Scope and boundaries

- Inspect read-only and report in chat by default. Do not edit callers, generate
  clients, install tools, run migrations, or save a report without a request for
  that work. A later implementation request can use this assessment as input.
- Read applicable repository guidance. Preserve existing work. Identify the
  repository/workspaces and revision or working-tree state being assessed.
- Inspect scripts before executing them. Builds and tests can write artifacts,
  access networks, or change external state; during assessment prefer source
  inspection and proposed commands over execution with unknown effects.
- Do not access live databases, secrets, or external systems merely to complete
  a trace. State external-consumer and runtime evidence gaps explicitly.

## 1. Resolve the target and change

Locate the authoritative definition and establish its identity, including module,
type, overload, endpoint method/path, or schema ownership. Distinguish generated
artifacts from their source. Read relevant manifests, contracts, and tests.

Establish old and proposed behavior from the request or diff. Consider signature,
return type, nullability, error behavior, side effects, serialization, and business
meaning as relevant. Do not assume a signature-preserving change is harmless.

If only a target is supplied, first map its actual consumers. Explain conditional
impact for materially different changes (for example adding an enum value versus
renaming one) and ask for the intended change only when needed to resolve a
conclusion. Ask about ambiguous identities only after inspecting available context.
Never invent the proposed behavior or present one hypothetical as confirmed intent.

## 2. Trace consumers and relevant dependencies

Use available language-aware definition/reference tools, then supplement with
targeted `rg` searches and source inspection. If reference tools are unavailable,
say so; neither an empty search nor a failed lookup proves absence of consumers.

Trace inbound callers/consumers to meaningful entry points or observable output.
Inspect outbound dependencies where changed inputs, ordering, side effects, or
invariants can alter their behavior. Direction matters: a dependency used by the
target does not automatically need changing when the target changes.

Follow applicable paths rather than applying an exhaustive generic checklist:

- Functions: callers, wrappers, callbacks, arguments, return-value assumptions,
  exceptions, retries, transaction boundaries, and side effects.
- Interfaces: implementations, dependency injection bindings, adapters, mocks,
  re-exports, and consumers through the abstraction.
- Schema/fields: writers, readers, defaults, validation, enum switches, mappings,
  queries, indexes/constraints, persistence representation, and existing data.
- APIs/events: request/response schemas, serializers, routes, publishers,
  subscribers, clients, SDK generation sources, versioning, and error contracts.
- Cross-cutting paths when relevant: UI rendering/filtering, jobs, reports,
  caches, config, registries, reflection, dynamic/string-based lookups, feature
  flags, and workspace or package exports.

For each meaningful path record a short chain and source locations, for example
`route → service → implementation → writer → event consumer`. Separate production
paths from test/tooling-only references. Exclude unrelated same-name symbols with
a reason when they could confuse the result. Tests and docs provide clues, not
proof of production reachability or external consumer coverage.

Continue transitive tracing until an entry point, observable behavior, inspected
contract boundary, or explicit evidence gap. Deduplicate cycles. Do not impose an
arbitrary hop limit or claim exhaustive coverage after searching only one module.
At an uninspected boundary name what evidence would allow tracing further.

## 3. Explain the consequences

Connect each finding to the proposed change. Identify whether it requires a code
update, may behave differently despite compiling, or only needs verification.
Do not label every caller as broken. Mark findings as:

- **Confirmed:** an inspected dependency and concrete consequence under the
  stated change are supported by evidence.
- **Conditional:** explain the specific assumption/change variant that causes
  the consequence; do not present it as observed runtime behavior.
- **Unknown:** identify missing source, runtime configuration, business rule, or
  external owner/consumer evidence and what it prevents concluding.

For stored or exchanged data consider old/new readers and writers, legacy values,
queued events, and mixed-version deployments where relevant. Adding a status
does not by itself imply a backfill. Surface compatibility/migration prerequisites;
use database-migration-planning for a detailed data migration assessment when
needed and available. Do not claim knowledge of production data from source alone.

Report risk and confidence separately with reasons. Risk reflects severity,
reach, compatibility, and recovery; confidence reflects evidence quality and
coverage. Unknown external callers are not zero callers. Avoid numeric scores
without a defined basis and avoid absolute guarantees of safety.

## 4. Map impact to verification

For each material behavior, identify existing tests by actual source location and
explain what they exercise. Inspect assertions rather than inferring coverage
from filenames. Identify gaps explicitly; do not fabricate paths or passing tests.

Propose the smallest useful set of checks:

- Unit tests for transitions, branching, mapping, null/error handling, or changed
  calculations.
- Integration tests for persistence, queries, transactions, framework wiring, or
  asynchronous flows.
- Contract tests for API/event serialization, clients, and old/new compatibility.
- End-to-end checks only where a user journey crosses the affected boundaries.

Each proposed check needs a scenario and expected result tied to an impact.
Include negative, legacy, retry/idempotency, or concurrency cases only when the
change makes them relevant. Distinguish existing tests, proposed tests, commands
actually run, and commands merely suggested. A green build cannot rule out a
behavioral or external compatibility break.

## 5. Report proportionally

Lead with the most important consequence and assessed scope. Keep small cases
short; use a table for several paths:

| Path and evidence | Consequence under the change | Evidence status | Required update / verification |
| --- | --- | --- | --- |

Include:

- Exact target, old/new behavior or unresolved change variants, and scope.
- Relevant caller/dependency chains with inspectable `file:line` evidence.
- Affected behavior and required updates versus verification-only consumers.
- Test mapping with existing coverage, gaps, scenarios, and expected results.
- Risk/confidence with reasons; unknown boundaries and how to resolve them.
- Necessary update/deployment order when compatibility requires it.

Use a small Mermaid diagram only if it clarifies a complex path. Clearly label
illustrative examples; never invent repository evidence. End with actionable
findings, not an automatic implementation or repetitive approval request.
