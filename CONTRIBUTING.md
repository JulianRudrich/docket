# Contributing

## Workflow

`main` is always releasable. All changes go through a pull request, including my own.

1. **Branch** from an up-to-date `main`:
   ```bash
   git switch main && git pull
   git switch -c feat/metrics-implementation
   ```
2. **Commit** in small, logical steps using [Conventional Commits](#commit-messages).
3. **Push** and open a pull request that references its issue (`Closes #4`).
4. **CI must be green**: lint, type check and tests.
5. **Squash merge.** The PR title becomes the commit message on `main`; the branch is deleted automatically.

## Branch names

`<type>/<short-description>`, e.g. `feat/local-extractor`, `fix/iban-normalization`, `docs/labeling-edge-cases`.

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <imperative summary, max ~70 chars>

<optional body: what and why, not how>
```

| Type | Use for |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `refactor` | Code change without behavior change |
| `test` | Adding or changing tests |
| `docs` | Documentation only |
| `data` | Dataset, labels, splits, labeling guide |
| `exp` | Evaluation runs and experiment results |
| `chore` | Tooling, dependencies, CI |

Examples: `feat(eval): implement document-level scoring`, `fix(extractor): handle max_tokens stop reason`, `exp: baseline results for Opus on dev split`.

## Before opening a pull request

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest
```

Or once: `uv run pre-commit install` to run formatting and linting on every commit.
