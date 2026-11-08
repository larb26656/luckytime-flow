---
name: create-application
description: Create or deploy a Kubernetes application from repository-managed manifests, including workloads, Services, configuration, and GitOps integration. Use for non-Helm workloads; use create-helm-application for a chart-managed application.
---

# Create Application

Create the requested workload using the target repository's deployment model and policies. A GitOps change may be reconciled automatically and pruning may delete resources: inspect the existing configuration before changing it.

## Inspect

1. Read the applicable `AGENTS.md`, deployment documentation, and a comparable application, including its GitOps registration and rendered resource configuration. Identify the source of truth, directory layout, target environment, namespace, and reconciliation behavior.
2. Determine the image and version, ports, replicas, Service needs, configuration, dependencies, and exposure requirements from the request and repository. Ask for required information that cannot be established; do not invent it.
3. If the application is managed as a Helm chart, use `create-helm-application` instead. If external exposure or external Secret documentation is needed, follow the relevant `expose-application` or `secret-readme` skill when available.

## Implement

- Add only the requested resources, following the repository's workload, label, namespace, registry, and GitOps conventions. Keep workload selectors and Pod labels consistent.
- Register resources in the actual build or deployment configuration. For Kustomize, include each intended resource in the appropriate `kustomization.yaml`.
- Put non-sensitive configuration in the project's supported configuration mechanism. Reference sensitive values using its approved secret-management system; never commit plaintext credentials.
- Set sync policies, namespace creation, and ordering only according to documented project policy and actual dependencies. Do not enable automatic pruning or self-healing merely as a default.

## Verify

Render or validate the changed manifests with the repository's documented commands, and check the resulting workload, references, namespace, and registered resources. If a required tool or external dependency is unavailable, report what was not verified. Report changed files and any operational prerequisites without exposing secret values.
