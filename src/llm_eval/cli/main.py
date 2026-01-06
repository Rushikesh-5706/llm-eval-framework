import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import logging
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
import logging
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

import argparse
import json
from pathlib import Path

from llm_eval.config.loader import load_config
from llm_eval.config.validator import (
    validate_metrics,
    validate_models,
)
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

    if args.models:
        names = [m.strip() for m in args.models.split(",")]
        validate_models(names, cfg.models)
        cfg.models = {k: v for k, v in cfg.models.items() if k in names}

    if args.metrics:
        cfg.metrics = [m.strip().lower() for m in args.metrics.split(",")]
        validate_metrics(cfg.metrics)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    model_outputs = {}
    for name, path in cfg.models.items():
        with open(path) as f:
            model_outputs[name] = {
                i: json.loads(line)["answer"]
                for i, line in enumerate(f)
            }

    results = run_evaluation(
        cfg.dataset_path,
        model_outputs,
        cfg.metrics,
        judge_config=cfg.judge,
    )

    df, stats = aggregate(results)

    write_json(out / "results.json", results)
    write_markdown(out / "report.md", stats)

    plots = out / "plots"
    plot_histograms(df, plots)
    plot_radar(stats, plots / "radar.png")


if __name__ == "__main__":
    main()

