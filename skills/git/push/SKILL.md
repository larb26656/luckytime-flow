---
name: push
description: Stage, commit, and push changes to the current branch when the user asks to push changes or invokes the push skill.
---

# Push

1. Run `git add .` to stage changes.
2. Inspect the staged diff and write a commit message following the format below.
3. Run `git commit -m "<message>"`.
4. Determine the current branch and run `git push origin <current-branch>`.
5. Report the commit and push result. If a command fails, stop and report the error rather than claiming success.

## Commit message

Use Conventional Commits: `<type>(<scope>): <description>`.

- Type is required; scope is optional and should identify the affected area when clear.
- Write a concise English description in the imperative mood, without a final period.
- Choose the type from the staged diff, not the branch name. For mixed changes, choose the type describing the primary change.
- Mark breaking changes with `!` after the type or scope, and explain them in a `BREAKING CHANGE:` footer. Include the footer in the commit message passed to `git commit`.

Types:

- `feat`: add a user-facing feature.
- `fix`: correct a bug.
- `docs`: change documentation only.
- `style`: change formatting without changing behavior.
- `refactor`: restructure code without adding a feature or fixing a bug.
- `perf`: improve performance.
- `test`: add or update tests.
- `build`: change the build system or dependencies.
- `ci`: change CI configuration or scripts.
- `chore`: maintenance that does not fit the other types.
- `revert`: revert a previous commit.

Examples:

- `feat(auth): add password reset`
- `fix(api): handle expired tokens`
- `docs: update installation instructions`
- `build: update dependencies`
- `feat(api)!: remove legacy endpoints` followed by a `BREAKING CHANGE:` footer.
