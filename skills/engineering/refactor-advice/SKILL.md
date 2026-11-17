---
name: refactor-advice
description: >-
  Inspect existing code and propose practical refactoring alternatives with
  evidence, tradeoffs, affected callers, and a recommendation. Use when the user
  asks how to refactor a case, compares restructuring approaches, or wants advice
  before changing code, including “เคสนี้ refactor ยังไงดี”, “เสนอทางเลือก refactor”,
  “ควรแยกตรงไหนดี”, and “ช่วยดูว่าจะจัดโค้ดนี้ใหม่แบบไหนดี”. Advice-only by default;
  do not activate for direct implementation requests, bug diagnosis alone,
  removal-safety assessments alone, or new-feature design without existing code.
---

# Refactor advice

Help the user choose whether and how to restructure existing code. Respond in
the user's language. Ground the advice in the actual code and the cost of future
changes, rather than a preferred pattern or an arbitrary file-size limit.

## Scope and execution

- Inspect relevant code and report in chat. Do not edit source, generate patches,
  install dependencies, or perform the proposed refactor during advice.
- Save the advice only if asked. Permission to save a report does not authorize
  implementation. A separate explicit request to implement the chosen option can
  move the conversation into implementation; simple agreement with the advice
  does not do so.
- Use read-only inspection commands. Describe tests and migrations as proposed
  work unless safely performed and actually observed; do not run commands with
  unknown writes or external effects just to prepare advice.
- Preserve observable behavior as the default refactoring constraint. Mark any
  proposed bug fix, contract change, or business-rule change separately so the
  user can assess it on its own merits.

## 1. Understand this case

1. Resolve the target from the supplied code, file, symbol, diff, or conversation.
   Read applicable repository guidance and existing conventions. If no target can
   be inferred, ask for a file, symbol, or snippet rather than auditing the repo.
2. Inspect the target plus relevant callers, dependencies, contracts, and tests.
   Use targeted searches and follow the paths needed to understand impact; avoid
   turning a local question into a whole-codebase review.
3. Identify the concrete pain: repeated business rules, changes spread across
   files, mixed responsibilities, hard-to-isolate side effects, tangled
   dependencies, or an interface that makes callers manage internal details.
   Connect each finding to an observed example or a realistic change scenario.
   Length and duplication are clues, not sufficient reasons by themselves.
4. Establish constraints that affect the choice: compatibility, team conventions,
   delivery scope, data consistency, and test coverage where relevant. Distinguish
   observed facts from assumptions. Ask only questions that materially change the
   recommendation and cannot be answered from available context.

If only a snippet is available, analyze it provisionally. State which caller or
runtime facts remain unknown; do not invent files, usage chains, or test results.

## 2. Develop meaningful alternatives

Normally offer two or three viable choices with different costs or responsibility
placement. Adapt the number to the case; do not invent weak options to fill a
table. Keeping the current design is a valid choice when its cost is small or the
future requirement is speculative.

For each option, explain:

- **Change:** what moves or gets simplified, who owns each affected responsibility,
  and what the caller would need to know afterward.
- **Benefit:** which observed pain improves and which change becomes easier.
- **Cost and limitation:** implementation effort, added concepts or indirection,
  and what pain remains. Use qualitative effort with reasons, not invented hours.
- **Impact and risk:** affected callers, public contracts, state or side-effect
  ordering, error behavior, transaction boundaries, and compatibility as relevant.
- **Fit:** the condition under which this option is worth choosing.

Useful alternatives might range from local simplification to consolidating a
business rule or moving responsibility behind a smaller interface. They need not
form a small/medium/large ladder. Renaming the same extraction is not a distinct
design, and more layers do not automatically improve the result.

Prefer approaches that keep knowledge and changes local. Introduce an abstraction
when it hides meaningful complexity or supports observed variation; explain what
it buys. Do not prescribe a strategy, factory, repository, service, or generic
framework solely because it is a familiar pattern. Keep distinct business rules
separate even when their code currently looks similar.

## 3. Recommend and make it actionable

Lead with a recommended option and its main reason. Tie the decision to the
current pain, constraints, and tradeoff that matters most. State what evidence
or future condition would make another option preferable. If evidence is weak,
make the recommendation provisional and name the missing evidence.

For the recommended option, outline a short, incremental sequence:

1. Establish the relevant behavior to preserve from current callers and tests;
   propose focused characterization coverage if important behavior is unprotected.
2. Move or simplify the smallest coherent responsibility, keeping callers working
   through the transition where necessary.
3. Update affected callers and remove replaced structures only after verifying
   their consumers. Flag external-consumer uncertainty rather than assuming none.
4. Verify the specific behavior at risk: outputs, failure modes, side-effect
   order, transaction behavior, or performance where the change affects them.

Scale the steps to the case. Identify a useful stopping point so the proposal
does not require a broad rewrite to deliver value. Avoid promising performance
improvements without measurements or treating data migrations as ordinary moves.

## Present the advice

Keep small cases compact. Include a recommendation, evidence for the problem,
an options comparison, and next steps with proposed checks. Use source links or
`file:line` references for inspected findings; mark proposed files as proposed.
Use a comparison table when it makes the choices easier to assess.

Use a short before/after interface or call-site sketch only when it distinguishes
the choices. Use Mermaid only when responsibility or dependency flow is otherwise
hard to follow. Do not produce complete replacement files as advice.

On follow-up, answer the new question and revise the affected tradeoffs. Carry
accepted constraints forward and avoid repeating the entire report or repeatedly
asking for approval. Do not claim that proposed changes or checks are complete.
