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
```

## Skills

### Git

| Skill | Description |
| --- | --- |
| [push](skills/git/push/SKILL.md) | Stage, commit, and push changes to the current branch using a Conventional Commit message. |
| [squash-and-cleanup](skills/git/squash-and-cleanup/SKILL.md) | Squash a work branch into a target branch and clean up approved branches after explicit plan confirmation. |

## Adding a skill

Place each skill in `skills/<category>/<skill-name>/SKILL.md`. Include a YAML frontmatter `name` and `description`, followed by the agent instructions. Skill names must be unique across the repository.

To check which skills the CLI discovers locally:

```bash
npx skills add . --list
```
