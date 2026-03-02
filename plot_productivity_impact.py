import argparse
import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def find_csv(folder, prefix):
    matches = glob.glob(os.path.join(folder, f"{prefix}*.csv"))
    if not matches:
        sys.exit(f"No CSV file starting with '{prefix}' found in {folder}")
    return matches[0]


def main():
    parser = argparse.ArgumentParser(
        description="Plot stacked horizontal bars of AI productivity impact by country."
    )
    parser.add_argument("-f", "--folder", help="Path to folder containing the two CSV files")
    args = parser.parse_args()

    impact_path = find_csv(args.folder, "impact")
    cumulative_path = find_csv(args.folder, "cumulative_impact")

    impact_df = pd.read_csv(impact_path)
    cumulative_df = pd.read_csv(cumulative_path)

    category_col = impact_df.columns[0]
    categories = impact_df[category_col].tolist()
    country_cols = [c for c in impact_df.columns[1:] if "All Firms" not in c]

    cumulative_map = {}
    for _, row in cumulative_df.iterrows():
        cumulative_map[row.iloc[0]] = row.iloc[1]

    colors = ["#c0392b", "#e67e22", "#95a5a6", "#2ecc71", "#27ae60"]

    fig, axes = plt.subplots(
        nrows=len(country_cols), ncols=1, figsize=(10, 1.6 * len(country_cols) + 1.2),
        sharex=True,
    )
    if len(country_cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, country_cols):
        values = impact_df[col].values.astype(float)
        lefts = np.zeros(1)
        for val, cat, color in zip(values, categories, colors):
            bar = ax.barh(0, val, left=lefts[0], height=0.55, color=color, edgecolor="white", linewidth=0.6)
            if val >= 3:
                ax.text(
                    lefts[0] + val / 2, 0, f"{val:.0f}%",
                    ha="center", va="center", fontsize=9, fontweight="bold", color="white",
                )
            lefts[0] += val

        cum_key = col
        cum_val = cumulative_map.get(cum_key)
        label = col.split("(")[0].strip().split()[0]
        if cum_val is not None:
            ax.set_ylabel(label, fontsize=11, fontweight="medium", rotation=0, labelpad=75, va="center")
            ax.annotate(
                f"Average: {cum_val:+.2f}%",
                xy=(1.01, 0.5), xycoords="axes fraction",
                fontsize=10, fontweight="bold", color="#2c3e50", va="center",
            )
        else:
            ax.set_ylabel(label, fontsize=11, fontweight="medium", rotation=0, labelpad=75, va="center")

        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    axes[-1].set_xlabel("Share of firms (%)", fontsize=11)
    axes[-1].set_xlim(0, 105)

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor="white") for c in colors
    ]
    fig.legend(
        legend_handles, categories,
        loc="lower center", ncol=len(categories),
        fontsize=9, frameon=False,
        bbox_to_anchor=(0.45, -0.01),
    )

    folder_name = os.path.basename(os.path.normpath(args.folder))
    parts = folder_name.replace("_", "-").split("-")
    if len(parts) >= 2:
        title = f"Impact of AI on {parts[0].title()} over {parts[1].title()} 3 Years"
    else:
        title = folder_name.replace("-", " ").replace("_", " ").title()
    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.01)

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    out_path = os.path.join(args.folder, f"{folder_name}.png")
    plt.savefig(out_path, dpi=180, bbox_inches="tight", facecolor="white")
    print(f"Saved to {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
