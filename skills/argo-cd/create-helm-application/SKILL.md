---
name: create-helm-application
description: Add or configure a Kubernetes application deployed from a Helm chart, including chart version, values, GitOps integration, and validation. Use for chart-managed workloads rather than applications maintained as ordinary Kubernetes manifests.
---

# Create Helm Application

Deploy or configure the chart using the target repository's existing Helm and GitOps workflow, not a presumed repository layout or Argo CD source structure.

## Inspect

1. Read the applicable `AGENTS.md`, deployment documentation, and a comparable chart-managed application. Identify the chart source, values location, deployment mechanism, target environment, and sync policies.
2. Establish the chart name, repository or OCI registry, intended version, namespace, and required configuration from the request and authoritative chart documentation. Ask for missing required choices; do not invent chart value names or Secret keys.
3. Check the chart's CRD installation, dependencies, upgrade implications, and how it accepts existing or externally managed Secrets. Follow the repository's approved secret policy; never commit plaintext credentials. If no approved safe method can supply a required secret, explain the blocker rather than putting it in values.

## Implement

- Configure the chart and only the documented values needed by the request. Use the existing repository convention for Helm CLI, HelmRelease, Argo CD, or another deployment mechanism; use multi-source and external values references only where that is the chosen pattern.
- Register the application and set namespace, sync policy, and dependency ordering according to the repository's actual configuration. Do not enable pruning or self-healing by default.
- Document externally provisioned Secrets using the `secret-readme` skill when available. For application exposure, use `expose-application` when appropriate; the chart itself may already own those resources.

## Verify

Render with the repository's documented workflow or `helm template` using the selected chart version and values when possible. Check values against chart documentation and inspect the rendered resources, Secret references, namespace, and dependencies. Report chart identity and version, changed files, prerequisites, and verification limitations; do not report secret values.
