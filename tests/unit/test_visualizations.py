import pandas as pd
from llm_eval.visualization.plots import plot_histograms, plot_radar

def test_plots(tmp_path):
    df = pd.DataFrame({
        "model": ["a", "a", "b"],
        "metric": ["bleu", "bleu", "bleu"],
        "score": [0.5, 0.6, 0.7]
    })

    stats = pd.DataFrame({
        "model": ["a", "b"],
        "metric": ["bleu", "bleu"],
        "mean": [0.55, 0.7]
    })

    plot_histograms(df, tmp_path)
    plot_radar(stats, tmp_path / "radar.png")

