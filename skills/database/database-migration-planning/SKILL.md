---
name: database-migration-planning
description: Assess whether existing data needs migration and plan safe changes across databases and object storage, including PostgreSQL, MySQL, MongoDB, and S3. Use when a changelog, schema or application change, new status or business rule may affect historical data, or when asked to plan a data migration, backfill, compatibility rollout, or recovery. Do not assume a migration is needed.
---

# Database migration planning

Assess the impact on existing data before proposing a migration. Respond in the user's language. Apply storage-independent reasoning, then adapt to the actual storage's capabilities; an object store is not a relational database. Keep the response proportional to the change and its risk.

## Boundaries

- Default to read-only investigation and a plan in chat. Do not write a report unless asked. Do not write a migration script unless explicitly asked; writing one does not authorize running it or changing data. Require explicit authorization before executing a migration or modifying stored data.
- Inspect available repository evidence first; ask only for material business rules, production conditions, or other facts that cannot be established safely. Do not access live data, secrets, or external systems without appropriate authorization. Never expose sensitive data in the report.
- Clearly separate observed facts and source locations from assumptions, unknowns, and proposed checks. A changelog describes intent, not proof of deployed versions or actual data. Do not infer production data characteristics from code alone.

## Assess the change

1. Identify the change, affected data and environments, and the relevant old and new behavior. Inspect relevant schemas or object formats, readers, writers, validation, defaults, consumers, deployment configuration, and existing migration patterns. Trace external consumers and scheduled or asynchronous jobs where relevant; repository evidence alone cannot rule them out.
2. Determine how existing data behaves under the new code and how old code handles newly written data. Consider missing, null, legacy, invalid and newly introduced values, and distinguish a read-time default from a persisted backfill. Check business meaning: a technically valid default can still misrepresent historical records. Identify required mapping, source of truth, exclusions, and records that cannot be mapped safely.
3. Classify the outcome as **migration required**, **migration not required under stated conditions**, or **insufficient evidence**. Explain the decision and its scope. Name evidence needed to resolve material unknowns rather than inventing data, mapping rules, or guarantees. A change in status values does not by itself prove a backfill is required.

## Plan when needed

Recommend the simplest safe approach and explain alternatives or prerequisites where material. Tailor detail to the change and storage rather than applying every technique by default:

- Define affected population, transformation and intended invariants; estimate volume and impact only from evidence. Address legacy or malformed records and how exceptions are handled without silently losing data.
- Specify deployment and compatibility order, including old and new readers/writers and downstream consumers. For live writes, explain how concurrent updates and records created during migration are captured or reconciled, and when cutover is safe. Discuss downtime only where appropriate.
- Describe batching, progress/checkpointing, retry and idempotency where relevant, including partial failures and race conditions. Do not promise atomicity or transaction guarantees unsupported by the actual system.
- Specify preflight and post-migration verification with meaningful invariants, counts or reconciliation and representative behavioral checks; account for records changing during verification. Identify observability and stop conditions proportional to risk. Distinguish checks performed from checks merely proposed.
- Explain recovery: backup or versioning prerequisites, rollback boundaries, and how to restore or reconcile writes made after migration. A code rollback alone does not restore transformed or deleted data; irreversible transformations may require a recovery strategy rather than an automatic rollback.
- Adapt to the actual storage model: for example object keys, versions, metadata and concurrent object replacement for object storage; document shapes and update semantics for document stores; schema and transaction constraints for relational stores. Verify actual capabilities and configuration rather than assuming them.

## Report

Lead with the verdict, scope, and reasoning. Summarize evidence and affected behavior, then the recommended plan, verification and recovery when applicable. List assumptions and unresolved questions separately. For a no-migration verdict, state the compatibility and data conditions that make it safe and how to verify them. For insufficient evidence, identify what decision each missing fact blocks. Make clear what was actually inspected or changed; planning is not execution.
