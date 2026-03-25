# R Experiments Workspace

Use this area for R-based AI/data-analysis experiments.

## Structure

- `project-template/`: starter template for a new R experiment
- `projects/`: actual R experiments (copy the template into here)

## Start A New Experiment

```bash
cp -R experiments/r/project-template experiments/r/projects/<project-name>
```

Then customize:

- `experiments/r/projects/<project-name>/README.md`
- `experiments/r/projects/<project-name>/analysis.R`
- `experiments/r/projects/<project-name>/config/.env.example`

## Isolation Guidelines

- Keep each experiment self-contained.
- Keep raw data in `data/raw/` and derived data in `data/processed/`.
- Write outputs to `outputs/`.
- Do not share project-specific secrets across experiments.
