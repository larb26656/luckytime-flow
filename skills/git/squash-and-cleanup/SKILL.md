---
name: squash-and-cleanup
description: Prepare a squash in an isolated worktree, then merge and clean up only after separate confirmations. Use for squash into main, merging and deleting intermediate branches, or cleanup after a squash, including “เอาเข้า main แบบ squash” and “ลบ branch ระหว่างทาง”.
---

# Squash and cleanup

Use two separately authorized states: **prepare** creates and tests a squash commit on a mirror branch in a new worktree; **finalize** integrates that exact commit only after another explicit confirmation. Worktrees share branch refs and repository configuration, so isolation does not eliminate ref races or side effects of test commands.

## Inspect and request prepare approval

Inspect without changing state: repository, all worktrees and their status; source branch and committed SHA; target branch, local and remote tips, remote URL and default branch (`git ls-remote`); changes and commits; applicable verification commands; proposed Conventional Commit message; candidate mirror branch name and unused worktree path. Resolve target from the request or remote default, not by assuming main. Identify cleanup candidates with ancestry and unique-commit evidence, not names alone.

Before approval do not fetch, create branches or worktrees, stage, switch, merge, commit, push, delete, stash, reset, or run commands that write generated files. Report dirty paths. A dirty original worktree need not block prepare: preserve it and explicitly say only committed source content is included. Protect branches checked out in any worktree.

Present the user, in their language, the exact source and target SHAs, remote, change summary, mirror branch and worktree path, squash and test commands, proposed commit message, potential cleanup names and evidence, retained branches, and risks. Explain prepare does not authorize integration, push, or cleanup. Ask for explicit approval of prepare using the host's question tool if available; otherwise ask in chat. If declined, change nothing. If inputs change, present a revised plan and obtain approval again.

For cleanup-only requests skip prepare/finalize: inspect recorded source/target commit evidence of the completed squash or equal trees, verify the target commit is on the remote, show exact deletion candidates and obtain explicit approval before cleanup. Merged-branch detection alone is insufficient after squash; retain branches where integration cannot be established.

## Prepare

Recheck source, target, remote tips, worktrees, mirror name and path against the approved plan. Stop if changed. Fetch the approved remote, verify the fetched target SHA equals the approved target, and stop on divergence or unreviewed local target commits. Create a new mirror branch at that exact target SHA with `git worktree add -b <mirror> <path> <target-sha>`; never switch or modify the original worktree. In the new worktree:

1. Run `git merge --squash <source-sha>`. If empty, stop and report the retained worktree without committing. Inspect the staged diff and run `git diff --cached --check` and the approved verification commands. After tests and before committing, recheck the staged diff and worktree including untracked files; stop if tests changed the staged content or left unexpected files or changes.
2. Commit once with `<type>(<optional-scope>): <imperative English description>` without a final period. Mark breaking changes with `!` and a `BREAKING CHANGE:` footer. If the actual scope or message materially differs, request a revised approval.
3. Record source SHA, base target SHA, mirror commit SHA, worktree path, staged/committed diff, and observed verification results. Confirm the commit has exactly the approved target as parent and no uncommitted changes remain in the mirror worktree; test-generated changes must not be silently included.

On conflict, failed test or mutation, stop, report the command and state including unmerged paths, and retain the worktree for inspection; do not reset, automatically resolve, commit, push or clean up. Do not modify target or push during prepare.

## Review and request finalize approval

Show the exact prepared commit and parent, source and target SHAs, committed diff summary, actual test results, target integration and push method, and explicit cleanup list with reasons. Ask for a **new explicit approval** to finalize this exact commit and the listed operations. Prepare approval or a general prior approval is not finalize approval. If declined, leave the prepared worktree and branches intact. Any expanded deletion list requires fresh approval.

## Finalize

Before and after approval, recheck the mirror commit, its parent, worktree cleanliness, source SHA, target local and remote tips and worktree occupancy. If any reviewed input changed, stop; if target advanced, prepare and test a new squash on the new base and obtain approvals again. Never merge an untested old-base commit.

Integrate the exact tested commit by fast-forward only. If target is checked out in another worktree, stop and propose a safe explicit plan for that worktree; do not update its ref behind it. Require no concurrent Git operations affecting target or worktree occupancy during finalize; if that cannot be ensured, stop. Verify the approved base is an ancestor of the prepared commit and update the local target using `git update-ref refs/heads/<target> <prepared-sha> <base-sha>` so a changed local tip fails atomically. Push the exact prepared SHA with an explicit expected-old remote lease for the approved base (`git push --force-with-lease=refs/heads/<target>:<base-sha> <remote> <prepared-sha>:refs/heads/<target>`). The ancestry check is essential: the lease protects against races but alone permits a non-fast-forward. Never overwrite a changed remote or bypass the lease. A rejected push or other failure stops the workflow; report exact local and remote state and retain all source and intermediate branches. Confirm the remote target actually points to the prepared commit before cleanup. Record source SHA and target commit as squash evidence.

## Cleanup and report

Only after successful verified integration (including a cleanup-only request with verified prior integration), delete the exact approved candidates. Before each deletion check its current tip and all worktrees; stop on changed tips or relevant remote state. Require no concurrent Git operations affecting candidate refs or worktree occupancy during local deletion; otherwise stop. Protect target, current branch, remote default, unrelated branches and branches checked out in any worktree. Use `git branch -d` where Git recognizes a merge. After a squash, `git branch -D` is permitted only for an explicitly approved branch whose contents were verified as integrated, or whose unique discarded work was explicitly disclosed and approved. Source ancestry alone does not prove all content survived the squash; inspect the integrated changes and retain uncertain branches. For each remote deletion use an explicit expected-tip lease, `git push --force-with-lease=refs/heads/<branch>:<approved-sha> <remote> :refs/heads/<branch>`, and stop if the server cannot enforce it. Stop on failure and report completed and remaining deletions.

Remove the created worktree and mirror branch only if their removal was explicitly included in the approved plan, after checking that the worktree is clean and mirror still points to the prepared commit. Never force-remove a dirty worktree. Report the prepared commit, observed checks, integration and push result, deletions and retained branches. On cancellation distinguish unchanged repository from retained prepared state; never claim an unobserved check or push.
