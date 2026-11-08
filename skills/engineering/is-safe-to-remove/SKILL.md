---
name: is-safe-to-remove
description: Assess whether code, files, exports, or package dependencies can be removed, tracing usage and reporting impact, prerequisites, risk, and confidence before the user decides. Use whenever the user asks whether something is safe to delete, unused, dead code, still depended on, or what would break if removed, including “ลบได้ไหม”, “ยังมีอะไร depend อยู่”, and “เช็กก่อนลบ”. Assessment-only; never delete or implement a migration within this workflow, even after confirmation.
---

# Is safe to remove

Give the user an evidence-backed removal decision, not an automatic cleanup. Respond in the user's language. Default scope: code, files, exports, and package dependencies. Database/schema changes and production resources need a separate assessment of data, ownership, retention, and recovery; do not treat them as ordinary dead code.

## Keep assessment separate from execution

- Inspect read-only and report in chat. Do not edit, delete, uninstall, migrate callers, create a patch, or save a report unless explicitly asked to save it. Permission to save a report permits only that report, not implementation.
- Invoking this skill, a low-risk conclusion, and responses such as “confirmed”, “ยืนยัน”, or “ลบเลย” do not cause execution inside this workflow. End with the assessment; actual changes require a separate explicit implementation task outside this skill.
- Check commands before running them. Do not install tools, fetch dependencies, generate files, auto-fix, or run builds/tests/scripts with unknown writes, network effects, or external state changes. A command named `check`, `dry-run`, or `test` is not necessarily read-only. Use existing safe inspection tools; describe unsafe verification as proposed work and request separate authorization if it is necessary.
- Never broaden the deletion scope to neighboring code or newly orphaned dependencies. List possible follow-on candidates separately for assessment.

## 1. Establish the target and boundary

1. Resolve the exact file, symbol, export, dependency, or bounded set from the request and repository context. Ask only if a material ambiguity remains after inspection. If no target is supplied, request one rather than auditing the entire repository.
2. Read applicable repository guidance and relevant manifests, entry points, and source. Identify workspaces, generated sources, environments, conditional builds, and the authoritative source of generated artifacts where relevant.
3. State the assessed boundary: repository/workspaces, target, and relevant revision or observed state when available. Preserve unrelated and uncommitted work. History is supporting context, not proof of current usage.

## 2. Trace reachability and effects

Start with the target and follow consumers back to actual entry points. Distinguish an inbound consumer (something uses the target) from an outbound dependency (something the target uses). Outbound dependencies alone do not prove the target is live; callers that are themselves unreachable do not prove it either.

Use available language-aware reference tools for symbols, then supplement with targeted searches and configuration inspection. If reference tooling is unavailable or incomplete, disclose that limitation. Do not interpret an empty or failed tool result as proof of absence.

Check the mechanisms relevant to this target rather than blindly applying every item:

- Direct and transitive imports/callers, aliases, re-exports, package entry points and exports, workspace consumers, and supported platform/build variants.
- Routes, CLI commands, scheduled jobs, framework conventions, plugins/registries, dependency injection, reflection, dynamic imports, globs, string-based lookups, templates, and feature flags, including disabled-but-supported paths.
- Module initialization and import-time side effects: registration, polyfills, instrumentation, hooks, and lifecycle behavior. An unused return value/export does not make loading the module unnecessary.
- Package scripts, CI/CD, bundlers, code generation, config, test setup, tooling, assets, and documentation describing an intentional public contract. A package may be used without a source import; a lockfile entry alone does not prove direct usage.
- External consumers of published APIs, packages, URLs, or commands. Repository search cannot rule them out. Identify the missing consumer or owner evidence instead of assuming zero users.

Record concrete evidence with `file:line` or another inspectable source. For meaningful live paths, show a short chain such as `entry point → registry → target`. Separate production reachability from test/tooling-only usage; neither silently counts as safe to delete. Tests passing or coverage showing no execution cannot prove absence of consumers.

## 3. Classify the decision

Assess each target separately; do not let one safe item authorize a mixed batch.

| Verdict | Meaning |
| --- | --- |
| Safe to remove within assessed scope | Relevant reachability and effects have been checked, with no supported consumer or required effect found. State the boundary; this is not permission to delete. |
| Remove only after prerequisites | Known consumers/effects require migration or replacement first. Name those prerequisites. |
| Keep | Evidence shows required behavior or an intentional supported contract that should remain. |
| Insufficient evidence | Missing runtime, environment, external-consumer, or tooling evidence prevents a defensible decision. Name exactly what would resolve it. |

Use “dead code” only when the evidence supports unreachability within the stated boundary and absence of required effects. Otherwise say “no usage found in the inspected scope”. Do not claim absolute safety.

Report two independent judgments with reasons:

- **Risk: low / medium / high.** Consider breakage severity, blast radius, public compatibility, data/security consequences, and reversibility. Unknown external exposure may itself make removal risky; do not manufacture a numeric score.
- **Confidence: low / medium / high.** Reflect evidence quality and coverage. High confidence that a caller exists can coexist with high removal risk. Missing evidence lowers confidence, not necessarily impact.

## 4. Explain what removal would require

For known impact, name affected consumers and observable behavior that would break. Explain the required order of migration/replacement, removal, and verification without implementing any step. Identify affected contracts, tests, config, or docs when observed; do not invent paths or add unrelated refactoring.

Offer only materially different choices, such as keep, migrate then remove, or remove an independently safe subset. Recommend one with a reason. For a partial removal, list exact boundaries and retained items.

Describe specific post-change checks that exercise the affected behavior, expected observations, and any rollback limitations. A source restore does not undo lost data, external effects, or an already-published compatibility break. Clearly distinguish checks actually run from proposed checks. Do not fabricate test or runtime evidence.

## 5. Report and stop

Keep small cases compact. Use a table for multiple targets and shared notes for repeated evidence. Include:

- **Conclusion and scope:** exact target, verdict, and removal conditions.
- **Evidence and impact:** relevant usage chains, required effects, affected behavior, and source locations.
- **Risk / confidence:** separate levels with reasons.
- **Unknowns:** uninspected areas, failed/unavailable checks, external consumers, and the evidence needed to resolve them.
- **Options and recommendation:** prerequisites, proposed verification, and recovery constraints proportional to the risk.
- **Decision boundary:** nothing changed; user decides whether to keep, investigate further, or commission a separate implementation task.

Do not repeatedly ask for permission as though confirmation runs deletion. If relevant code or consumer evidence changes after the report, reassess before relying on its conclusions. A later implementation task must stay within the exact approved targets and plan; newly discovered impact requires a revised assessment, not automatic scope expansion.
