---
name: secret-readme
description: Document Kubernetes application Secret requirements and safe provisioning when adding or changing a workload, Helm chart, or other deployment. Use for externally supplied Secret names, keys, mounts, environment variables, and operational prerequisites without exposing credentials.
---

# Document Secret Requirements

Document externally supplied Secrets where the target repository expects operational documentation. Follow its secret-management policy; never place plaintext credentials in documentation or version control.

## Inspect

1. Read the applicable `AGENTS.md`, deployment documentation, and relevant workload or chart configuration. Identify the actual source of truth and documentation location; do not assume a Kustomize directory exists for Helm applications.
2. Inspect Secret references in environment variables, `envFrom`, projected or Secret volumes, image pull credentials, and chart values as applicable. Determine the namespace, name, required keys, and whether a controller or an external operator creates each Secret.
3. Obtain unknown keys, formats, and required/optional status from authoritative application or chart documentation or the user. `envFrom` alone does not reveal which keys the application requires. Do not invent missing details.

## Document

- Record the namespace, Secret name, ownership, required and optional keys, purpose and expected format, plus environment variable names or mount paths where relevant. Use clearly fictional placeholders, never real credentials.
- Describe the approved provisioning or secret-management workflow and prerequisites. Prefer the project's existing encrypted-secret or external-secret workflow; a local `kubectl create secret` example is appropriate only if consistent with project policy. Avoid commands that expose secrets in shell history or process arguments.
- Distinguish controller-generated Secrets, such as certificate output, from operator-provisioned prerequisites. Do not instruct operators to manually recreate controller-owned Secrets.

## Verify

Compare the documentation against workload references, chart documentation, and the approved provisioning mechanism. Validate or render affected deployment configuration using the repository's workflow when configuration changed. Report unknown keys or unverified prerequisites explicitly; never claim a Secret exists without checking the correct environment.
