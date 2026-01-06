import os
import math
import matplotlib.pyplot as plt

def plot_histograms(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for metric in df["metric"].unique():
        subset = df[df["metric"] == metric]
        plt.figure()
        plt.hist(subset["score"], bins=10)
        plt.title(f"Score Distribution — {metric}")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{metric}_hist.png"))
        plt.close()

def plot_radar(stats, output_path):
    metrics = stats["metric"].unique().tolist()
    models = stats["model"].unique().tolist()

    angles = [n / float(len(metrics)) * 2 * math.pi for n in range(len(metrics))]
    angles += angles[:1]

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    for model in models:
        values = stats[stats["model"] == model]["mean"].tolist()
        values += values[:1]
        ax.plot(angles, values, label=model)
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], metrics)
    ax.set_title("Model Comparison Radar")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
