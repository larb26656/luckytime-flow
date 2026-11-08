---
name: squash-and-cleanup
description: Squash a completed work branch into a target branch, push, and clean up related branches after explicit plan confirmation. Use when asked to squash into main, merge and delete intermediate branches, or clean up branches after a squash merge, including Thai requests such as “เอาเข้า main แบบ squash” and “ลบ branch ระหว่างทาง”.
---

# Squash and cleanup

## 1. Inspect without changing state

Use read-only inspection to determine:
- Repository, current branch, worktree status, and other worktrees.
- Source branch and commit, target branch, remote URL, and current remote branch tips (`git ls-remote`). Resolve the target from the request or remote default branch rather than assuming `main`.
- Changes and commits between target and source, repository verification commands, and a proposed Conventional Commit message based on the changes.
- Local and remote cleanup candidates, with evidence connecting each to this work. Names alone are not evidence; inspect ancestry and unique commits.

Before confirmation, do not fetch, stage, switch branches, merge, commit, push, delete branches, stash, reset, or run commands that write generated files. A request to invoke this skill is not approval of an unseen plan.

If the worktree is dirty, report the paths and pause. Preserve the user's changes rather than automatically staging or stashing them. Treat branches used by another worktree as protected.

For cleanup-only requests, inspect the completed merge/squash evidence and skip the merge workflow. Ordinary merged-branch detection is insufficient after a squash: use the recorded source/target commit pair from the completed operation, or equal source and target trees as evidence. Retain branches when integration cannot be established.

Completion: enough evidence to show an exact plan without modifying the repository.

## 2. Present the plan and wait for confirmation

Respond in the user's language with:

```text
Repository: <path>
Source → target: <branch>@<sha> → <branch>@<sha>
Changes: <brief summary>
Steps:
1. <fetch/update target safely>
2. <squash source into target>
3. <exact verification commands>
4. <proposed Conventional Commit message>
5. <push remote/target>
6. <delete the listed branches only after successful push>
Delete local: <explicit names + why each is safe, or none>
Delete remote: <remote/name pairs + why each is safe, or none>
Keep: <unrelated, uncertain, protected, or unique-work branches + reason>
Risks/blockers: <dirty state, divergence, unverified branches, or none>
Confirm this plan before I make changes?
```

For cleanup-only requests, show only the applicable steps. Include all intended mutations, including deletion of any branch with unique commits. Retain such branches by default; removing them requires explaining the unique work and getting explicit approval for that branch.

Use the host's confirmation/question tool when available, after showing the plan. Otherwise ask in chat and end the turn. Wait for an explicit affirmative response to this plan. Cancellation or a requested revision makes no changes; present a revised plan when needed. A generic earlier approval does not authorize a later expanded deletion list.

Completion: the user explicitly approves this exact plan.

## 3. Execute the approved merge

Recheck the worktree, source commit, and remote tips before mutating. If the inputs changed since approval, stop and present the changed plan for confirmation. The approved commit IDs bind the operation to reviewed content.

For a merge:
1. Fetch the approved remote, then switch to the target branch. Bring it to the approved remote tip with a fast-forward-only update. Stop for divergence or unreviewed local target commits.
2. Run `git merge --squash <source>`. This leaves changes staged without importing the source's commit history.
3. Inspect the staged diff and run `git diff --cached --check`, then the approved verification commands. Observe their results. If the squash yields no changes, report it rather than creating an empty commit.
4. Commit once using `<type>(<optional-scope>): <imperative English description>`, without a final period. Choose the type from the staged changes. Mark breaking changes with `!` and include a `BREAKING CHANGE:` footer when applicable. If the resulting diff requires a materially different message or scope, revise the plan first.
5. Push the target normally to the approved remote. Do not force-push. Record the source SHA and the new target commit as evidence of the squash.

Stop on a failed mutation or failed check and report the command, error, and current state. A squash conflict leaves a merge to resolve; report the unmerged paths and preserve that state rather than resetting, automatically resolving, committing, or continuing to push. Interpret expected negative inspection results (for example, `merge-base --is-ancestor` exiting 1) as evidence, not successful integration.

Completion: the target push succeeded. Until then, preserve all source and intermediate branches.

## 4. Delete only approved, integrated branches

For cleanup-only operations, first verify that the approved target commit is already present on the remote. For a merge just completed, use its successful push as evidence.

Before each deletion, verify the branch still points to the approved commit and is not checked out in any worktree. Protect the target, current branch, remote default branch, and unrelated branches. If a tip or relevant remote state changed, pause for a revised plan rather than expanding scope.

Delete only the exact approved names:
- Use `git branch -d <branch>` for branches Git recognizes as merged.
- After a squash, `git branch -D <branch>` is permitted only for an explicitly approved branch whose contents were integrated, or whose unique discarded work was explicitly approved in step 2. An ancestor of the recorded squash source is integrated by that squash; a similar name is not proof.
- Use `git push <remote> --delete <branch>` for approved remote branches. Recheck remote tips immediately before deletion; if an atomic expected-tip deletion is supported, prefer it so a concurrent update cannot be removed.

Stop on deletion failure and report which deletions succeeded and which remain. Leave unrelated branches and worktrees untouched.

Completion: every approved deletion succeeded, or a precise failure was reported without continuing.

## 5. Report observed results

Report the squash commit and push result (if applicable), deleted local/remote branches, retained uncertain branches, and only the verification actually run. On cancellation, report that nothing was changed. Keep the result concise; do not claim a check or push that was not observed.
