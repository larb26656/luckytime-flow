---
name: design-preview
description: >-
  Discuss and iteratively refine a proposed implementation before writing code,
  using concise rationale, Mermaid diagrams, file structure, and implementation
  steps. Use only when explicitly invoked or when the user explicitly asks for a
  design-preview conversation, such as “วางแบบให้ดูก่อน”,
  “ขอคุยแนวทางก่อน ยังไม่ต้องทำ”, or “show me the approach and files before we implement”.
  Do not activate for ordinary coding requests. This is discussion-only:
  confirmation does not trigger implementation.
---

# Design preview

Make the intended result and approach concrete enough for the user to correct misunderstandings before implementation. Respond in the user's language. Explain decisions and concise rationale, not private internal deliberation.

## Keep the conversation separate from execution

- Discuss and revise the design; do not implement the proposed feature. “Looks good”, “confirmed”, “ยืนยัน”, and answers to questions acknowledge the current draft, not permission to change files. They do not lock the design or end the conversation.
- Do not offer an automatic “approve → implement” next step. Implementation requires a separate explicit task outside this workflow; an ordinary confirmation is not that task.
- Inspect relevant project context read-only. Do not create scaffolding, edit project code, install dependencies, or run implementation commands while discussing the design.
- Keep the proposal in chat. Save it only when the user explicitly asks, following the target repository's documentation conventions; permission to save a plan is not permission to implement it.
- Requests for more implementation detail mean explanation in chat, not file changes.

## Start with a useful overview

1. Read enough available context to ground the proposal in existing conventions. Do not ask for information the repository provides. Distinguish observed facts, proposed changes, and assumptions. For a new project, label all suggested paths as proposed rather than existing.
2. Show a rough, useful design before conducting a long interview. If the request is ambiguous, make assumptions visible and ask only questions that materially affect the design. Do not invent missing requirements as facts.
3. Recommend one approach with brief reasons. Compare alternatives only when their tradeoffs would change the user's decision.
4. Start at overview level. Deepen technical contracts, data models, algorithms, or implementation walkthroughs only when the user asks.

Include the following where relevant, keeping small tasks compact:

- **Outcome and scope:** what the user would get, and important exclusions.
- **Approach:** main components, responsibilities, and concise rationale.
- **Visual:** Mermaid for meaningful flow, state, sequence, or relationships. Omit diagrams that add no clarity; do not duplicate the same information in several forms.
- **Files:** a file tree marking proposed create/modify/remove actions and each affected file's responsibility. Ground existing paths in inspection; do not invent a second project convention.
- **Steps and checks:** the main implementation sequence and observable acceptance checks, described as future work rather than completed actions.
- **Assumptions and open choices:** provisional decisions and focused questions needed to refine the draft.

Use a file tree for project structure, not a redundant Mermaid version of the same tree. Do not force every heading into every reply.

## Use code sketches sparingly

A short snippet may clarify an interface, a call site, or a key design choice. Keep it illustrative and focused, not a complete module or code for every proposed file. Do not proactively turn a small sketch into detailed implementation. Wait for the user to ask before going deeper, and keep that explanation in chat.

For example, a reservation discussion might show only:

```ts
reserveEquipment(input: ReservationRequest): Promise<Reservation>
```

Explain the contract or tradeoff that matters; do not generate its implementation unless the user asks to discuss that detail.

## Iterate without replaying the whole design

- Answer the user's current question directly, then update only affected parts of the approach, diagram, file structure, steps, or assumptions.
- Explain meaningful consequences of a change. Carry accepted revisions forward rather than reverting silently to an older draft.
- Do not repeat the complete proposal every turn or keep asking for approval. Confirmation is compatible with further questions and revisions.
- When asked for the latest consolidated design, assemble the current version with all revisions and remaining assumptions. Keep it in chat unless saving is explicitly requested.
- Do not claim that proposed files exist, code was implemented, or checks passed unless those facts were actually observed.
