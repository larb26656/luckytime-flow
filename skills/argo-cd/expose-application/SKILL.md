---
name: expose-application
description: Expose a Kubernetes application or change its hostname, ingress, gateway route, HTTPS/TLS, or routing middleware. Use for new or existing applications and discover the project's actual ingress controller and certificate workflow.
---

# Expose Application

Implement only the requested exposure using the project's existing ingress or gateway architecture. Do not assume a particular controller, route resource, issuer, entry point, or TLS termination model.

## Inspect

1. Read applicable `AGENTS.md` instructions, deployment documentation, controller configuration, and comparable existing routes. Locate the application, backend Service, namespace, and declared Service port.
2. Establish the requested hosts, paths, backend mapping, TLS, authentication, CORS, and any path rewriting. Inspect existing routes for overlaps and precedence. Ask for security-sensitive or routing decisions that cannot be determined; do not infer them from an example.
3. Determine whether a certificate is controller-managed, already exists, or must be provisioned through the project's approved workflow. Check controller support and authorization before using cross-namespace references.

## Implement

- Use the supported resource type and repository conventions, such as Gateway API, Ingress, or a controller-specific route. Preserve existing routes and security policies; add middleware or equivalent only as required.
- Reference the actual Service port and the appropriate TLS certificate or Secret. Do not commit generated TLS Secrets or plaintext private keys.
- Register new resources in the project's deployment configuration and respect real controller, CRD, and certificate dependencies. Do not change the controller itself unless requested.
- If the backend is missing, identify the prerequisite; create it only when within the user's request and supported by available information.

## Verify

Render or validate using the repository's commands. Inspect host and path matches, route precedence, backend and namespace references, TLS, auth, CORS, and rewriting as applicable. Rendering alone does not prove live reachability or controller behavior: report any checks that could not be performed. Summarize the exposed mapping and prerequisites.
