# luckytime-flow

A collection of reusable agent skills, organized by topic.

## Install

Requires Node.js 22.20 or later. Run from the project where you want to use the skill:

```bash
npx skills add https://github.com/larb26656/luckytime-flow
```

Select the skills and agents when prompted. To install a specific skill, pass `--skill`:

```bash
npx skills add https://github.com/larb26656/luckytime-flow --skill push
npx skills add https://github.com/larb26656/luckytime-flow --skill squash-and-cleanup
npx skills add https://github.com/larb26656/luckytime-flow --skill design-preview
```

## Skills

### Engineering

| Skill | Description |
| --- | --- |
| [design-preview](skills/engineering/design-preview/SKILL.md) | Discuss and refine an implementation approach with diagrams, file structure, steps, and short code sketches. Discussion-only: confirmation does not trigger implementation. |
| [is-safe-to-remove](skills/engineering/is-safe-to-remove/SKILL.md) | Assess removal safety, dependencies, impact, risk, and confidence without changing or deleting anything; implementation is a separate task. |

### Database

| Skill | Description |
| --- | --- |
| [database-migration-planning](skills/database/database-migration-planning/SKILL.md) | Assess whether existing data needs migration and plan compatible, verifiable changes across databases and object storage. |
| [gen-query](skills/database/gen-query/SKILL.md) | Generate database-specific SQL or NoSQL queries from business requirements and inspected entities, with brief join explanations; never execute them. |

### Git

| Skill | Description |
| --- | --- |
| [push](skills/git/push/SKILL.md) | Stage, commit, and push changes to the current branch using a Conventional Commit message. |
| [squash-and-cleanup](skills/git/squash-and-cleanup/SKILL.md) | Squash a work branch into a target branch and clean up approved branches after explicit plan confirmation. |

### Argo CD

| Skill | Description |
| --- | --- |
| [create-application](skills/argo-cd/create-application/SKILL.md) | Create a Kubernetes workload from repository-managed manifests. |
| [create-helm-application](skills/argo-cd/create-helm-application/SKILL.md) | Deploy or configure a Helm chart using the project's deployment workflow. |
| [expose-application](skills/argo-cd/expose-application/SKILL.md) | Expose an application using the project's ingress or gateway and TLS conventions. |
| [secret-readme](skills/argo-cd/secret-readme/SKILL.md) | Document external Secret requirements and safe provisioning. |

### Setting up `AGENTS.md` for GitOps

In the target repository, document the actual deployment conventions in the
applicable `AGENTS.md` before using these skills. Inspect the existing
configuration and documentation first; omit unknown or inapplicable items
instead of copying example values as facts.

- **Delivery and layout:** where Applications, manifests, Helm values, and
  environment overlays live; which repository and revisions deploy to which
  environments; how resources are registered and reconciled.
- **Safety and ordering:** sync, pruning, self-healing, namespace creation,
  CRD/controller dependencies, sync waves, and any approval requirements.
- **Workloads and images:** namespace, naming, registry, image pull, and
  configuration conventions.
- **Exposure:** the ingress or gateway controller and resource types, route
  ownership, TLS and issuer workflow, cross-namespace rules, and auth/CORS
  policies. Refer to existing configuration rather than duplicating hostnames.
- **Secrets:** approved encrypted or external secret systems, ownership,
  provisioning and documentation locations, and what must never be committed.
  Do not put credentials or secret values in `AGENTS.md`.
- **Verification:** exact render and validation commands for each deployment
  type, plus restrictions on cluster access and live changes.

Keep `AGENTS.md` concise and link to the authoritative manifests and
documentation; record project-specific exceptions there, not inside the
reusable skills. If a required decision is undocumented, inspect the repo or
ask rather than assuming a default.

## Adding a skill

Place each skill in `skills/<category>/<skill-name>/SKILL.md`. Include a YAML frontmatter `name` and `description`, followed by the agent instructions. Skill names must be unique across the repository.

To check which skills the CLI discovers locally:

```bash
npx skills add . --list
```
