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

    # Load config
    cfg = load_config(args.config)

    # Override models if provided
    if args.models:
        names = [m.strip() for m in args.models.split(",")]
        validate_models(names, cfg.models)
        cfg.models = {k: v for k, v in cfg.models.items() if k in names}

    # Override metrics if provided
    if args.metrics:
        cfg.metrics = [m.strip().lower() for m in args.metrics.split(",")]
        validate_metrics(cfg.metrics)

    # Resolve output dir
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve paths relative to the current working directory (Project Root)
    project_root = Path.cwd()

    model_outputs = {}
    for name, path_str in cfg.models.items():
        # Clean path and handle potential absolute paths from Docker/CI
        raw_path = Path(path_str)
        
        if raw_path.is_absolute():
            # If it's an absolute path that doesn't exist (like /app/...), 
            # try to find it relative to project root
            if not raw_path.exists():
                path = (project_root / path_str.lstrip("/")).resolve()
            else:
                path = raw_path
        else:
            path = (project_root / raw_path).resolve()

        if not path.exists():
            # Fallback: check relative to the config file location
            config_dir = Path(args.config).expanduser().resolve().parent
            path = (config_dir / raw_path).resolve()

        if not path.exists():
            raise FileNotFoundError(f"Model output file not found: {path}")

        with open(path) as f:
            model_outputs[name] = {
                i: json.loads(line)["answer"]
                for i, line in enumerate(f)
                if line.strip()
            }

    # Resolve dataset path
    dataset_path = Path(cfg.dataset_path)
    if not dataset_path.is_absolute():
        dataset_path = (project_root / dataset_path).resolve()
    
    if not dataset_path.exists():
        # Fallback to config dir
        config_dir = Path(args.config).expanduser().resolve().parent
        dataset_path = (config_dir / Path(cfg.dataset_path)).resolve()

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    # Run evaluation
    results = run_evaluation(
        str(dataset_path),
        model_outputs,
        cfg.metrics,
        judge_config=cfg.judge,
    )

    # Aggregate + report
    df, stats = aggregate(results)
    write_json(out_dir / "results.json", results)
    write_markdown(out_dir / "report.md", stats)

    plots_dir = out_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    plot_histograms(df, plots_dir)
    plot_radar(stats, plots_dir / "radar.png")


if __name__ == "__main__":
    main()
