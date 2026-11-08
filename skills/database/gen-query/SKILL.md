---
name: gen-query
description: Turn business reporting or data lookup requirements into database-specific, read-only queries for the user to run. Use when users ask to generate SQL, MongoDB pipelines, native NoSQL queries, reports, metrics, or data extracts from existing entities or schemas, even without naming tables. Inspect relevant models and relationships, identify the database dialect, and briefly explain joins or equivalent operations. Generate queries only; do not execute them.
---

# Generate queries

Translate the user's information need into a query grounded in the actual project. Support SQL and NoSQL through a storage-independent workflow, not a supposedly universal query syntax. Respond in the user's language. Keep the initial explanation brief; explain implementation details and performance more deeply only when asked.

## Boundaries

- Generate read-only queries for the user to run themselves. Do not execute queries, connect to databases, run EXPLAIN, or fetch live records. Repository inspection is sufficient for this workflow; requesting a query is not authorization to access a database.
- Exclude writes and side effects, including data-changing CTEs, SELECT INTO, locking reads, write-capable procedures, and MongoDB $out/$merge. If asked for mutations, explain that they are outside this skill's read-only scope.
- Never invent tables, collections, fields, relationships, enum values, or database capabilities. Distinguish observed facts from assumptions. Do not expose credentials or sensitive values found in configuration.
- Return the query in chat; create files only if requested. Do not modify the application or schema.

## Discover the relevant data

1. Extract the desired result: what one output row or document represents, requested fields or metrics, population, filters, time range, sorting, and whether the user wants all results or a sample.
2. Identify the relevant database engine and, where evidenced, version from dependencies, provider configuration, migrations, or project documentation. In multi-database projects, trace the requested entities to their actual store. Do not assume PostgreSQL or force NoSQL into SQL. If engine/version uncertainty affects correctness, resolve it before emitting engine-specific syntax.
3. Locate the relevant entity/model/schema definitions, migrations, relation mappings, and existing query patterns. Start narrow and follow only necessary relationships. Resolve physical table/collection names, mapped columns, key types, embedded documents, bridge tables, and join keys. Cite concise source paths supporting the mapping.
4. Check applicable business rules in nearby readers/writers: tenant boundaries, soft deletion, statuses, historical versus current values, date fields, currency, units, and null/missing semantics. An ORM relation does not prove a deployed foreign key or production schema; migrations and models may disagree. Surface material mismatches rather than silently choosing one.
5. Ask only questions whose answers materially change the result and cannot be established from available evidence. Examples include revenue before/after refunds, order date versus payment date, or reporting timezone. Batch related questions. State low-impact assumptions and proceed. If schema or a necessary relationship is unavailable, request that specific evidence instead of presenting a fabricated runnable query.

## Build the query

- Choose native syntax and operators supported by the identified engine/version. For stores without joins, use supported lookup/graph operations or an explicit sequence of read-only queries, explaining how the user passes keys between steps. State capability limits instead of inventing a cross-store join.
- Preserve the requested result grain. Check one-to-many and many-to-many fan-out before aggregating; pre-aggregate or use an existence filter when appropriate. Do not hide incorrect joins with DISTINCT. Explain intentional deduplication and what defines uniqueness.
- Choose inner versus outer joins deliberately. Preserve unmatched rows when required and avoid turning an outer join into an inner join through filtering. Handle null, missing fields, empty arrays, and zero-result aggregates according to the requested meaning.
- Apply evidenced tenant and soft-delete rules at all relevant levels, including joined entities. Never guess a tenant identifier. A raw query may bypass ORM scopes: carry required predicates into the query explicitly.
- Use the correct date field, timezone, and boundary semantics; prefer half-open intervals for time ranges. Do not silently mix currencies or units. Use deterministic ordering for ranking or pagination where keys permit it.
- Select only necessary fields. Do not silently limit complete reports or aggregates. For a requested preview, label the limit and use the engine's supported syntax.
- Use clearly named parameters and state their types and how to bind them in the named client. For clients without bind variables, use explicit replacement markers and instructions. Do not call an unsubstituted template directly runnable. Do not interpolate untrusted values into query text.
- Review the result against the requested meaning and inspected schema without execution. Label it as not executed; do not claim verified results, performance, index availability, or production compatibility. Mention a material full-scan or unsupported-operation risk briefly when evidence warrants it; leave extended tuning to follow-up questions.

## Response

Lead with the query, preceded only by the engine/client and any essential assumption. Use the appropriate code fence. Then provide:

- **Parameters:** values/types to supply and binding or replacement instructions; omit when unnecessary.
- **How it works:** a few short bullets describing the base population, each join/lookup and why it is needed, and aggregation/filter meaning. If no join is needed, say so without manufacturing one.
- **Notes:** concise source paths, material assumptions or limitations, and confirmation that the query was not executed.

Do not dump the full entity scan, a schema tutorial, an execution plan, or speculative alternatives. Expand those only when the user asks.
