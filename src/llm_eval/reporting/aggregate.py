import pandas as pd

def aggregate(results):
    rows = []

    for r in results:
        for metric, score in r["scores"].items():
            if isinstance(score, dict):
                for dim, val in score.items():
                    rows.append({
                        "model": r["model"],
                        "metric": f"{metric}.{dim}",
                        "score": val
                    })
            else:
                rows.append({
                    "model": r["model"],
                    "metric": metric,
                    "score": score
                })

    df = pd.DataFrame(rows)
    stats = df.groupby(["model", "metric"])["score"].agg(
        ["mean", "median", "std", "min", "max"]
    ).reset_index()

    return df, stats
