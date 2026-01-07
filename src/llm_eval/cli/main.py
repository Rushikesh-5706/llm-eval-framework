import os
import json
import argparse
import logging
from pathlib import Path

# Silence noisy libraries
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

from llm_eval.config.loader import load_config
from llm_eval.config.validator import validate_metrics, validate_models
from llm_eval.core.evaluator import run_evaluation
from llm_eval.reporting.aggregate import aggregate
from llm_eval.reporting.writers import write_json, write_markdown
from llm_eval.visualization.plots import plot_histograms, plot_radar
from llm_eval.utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(description="LLM Evaluation Framework")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--models", help="Comma-separated model names override")
    parser.add_argument("--metrics", help="Comma-separated metrics override")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    setup_logger(verbose=args.verbose)

    cfg = load_config(args.config)

    # Resolve config directory
    config_dir = Path(args.config).expanduser().resolve().parent

    # Handle model overrides
    if args.models:
        names = [m.strip() for m in args.models.split(",")]
        validate_models(names, cfg.models)
        cfg.models = {k: v for k, v in cfg.models.items() if k in names}

    # Handle metric overrides
    if args.metrics:
        cfg.metrics = [m.strip().lower() for m in args.metrics.split(",")]
        validate_metrics(cfg.metrics)

    # Prepare output directory
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

# Resolve paths relative to project root (repo root)
project_root = Path.cwd()

model_outputs = {}

for name, path in cfg.models.items():
    path = Path(path)

    if not path.is_absolute():
        path = (project_root / path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Model output file not found: {path}")

    with open(path) as f:
        model_outputs[name] = {
            i: json.loads(line)["answer"]
            for i, line in enumerate(f)
            if line.strip()
        }

    # Resolve dataset path (relative to config)
    dataset_path = Path(cfg.dataset_path)
    if not dataset_path.is_absolute():
        dataset_path = (config_dir / dataset_path).resolve()

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    # Run evaluation
    results = run_evaluation(
        str(dataset_path),
        model_outputs,
        cfg.metrics,
        judge_config=cfg.judge,
    )

    # Aggregate + reports
    df, stats = aggregate(results)
    write_json(out / "results.json", results)
    write_markdown(out / "report.md", stats)

    # Visualizations
    plots_dir = out / "plots"
    plot_histograms(df, plots_dir)
    plot_radar(stats, plots_dir / "radar.png")


if __name__ == "__main__":
    main()

