import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

years = [2021, 2022, 2023, 2024]

data = {
    "Deep Adoption":           [ 1,  0,  2,  4],
    "Production Level":        [ 0,  4,  2,  4],
    "Significant Integration": [19, 14, 26, 33],
    "In Process":              [ 1,  5,  7,  8],
    "No Mention":              [32, 30, 16,  4],
}

# Dark blue → red (dict is Deep Adoption first, No Mention last)
colors = ["#003f8a", "#5bafd6", "#f5c842", "#f4873a", "#d93025"]

fig, ax = plt.subplots(figsize=(9, 6))

bottoms = np.zeros(len(years))
for (label, counts), color in zip(data.items(), colors):
    counts_arr = np.array(counts)
    ax.bar(
        years,
        counts_arr,
        bottom=bottoms,
        label=label,
        color=color,
        width=0.55,
        edgecolor="white",
        linewidth=0.8,
    )
    for i, (y, b, c) in enumerate(zip(years, bottoms, counts_arr)):
        if c > 0:
            ax.text(
                y, b + c / 2, str(c),
                ha="center", va="center",
                fontsize=9, color="white", fontweight="bold",
            )
    bottoms += counts_arr

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=12)
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.set_ylabel("Number of Enterprises in S&P 500", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_title("AI Adoption in the Financial Sector by Year", fontsize=14, fontweight="bold")
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles[::-1], labels[::-1],
    title="AI Adoption Level",
    loc="upper left",
    bbox_to_anchor=(1.01, 1),
    borderaxespad=0,
    fontsize=9,
    title_fontsize=10,
    framealpha=0.9,
)
ax.set_ylim(0, max(bottoms) * 1.1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout(rect=[0, 0, 0.82, 1])
plt.savefig("ai_adoption.png", dpi=150, bbox_inches="tight")

# --- Version 2: Total adopters (AI score >= 2) by year ---
adopter_labels = ["In Process", "Significant Integration", "Production Level", "Deep Adoption"]
adopter_colors = ["#f0ad4e", "#5bc0de", "#428bca", "#5cb85c"]
adopter_totals = [
    sum(data[label][i] for label in adopter_labels)
    for i in range(len(years))
]

fig2, ax2 = plt.subplots(figsize=(8, 5))
bars = ax2.bar(years, adopter_totals, color="#428bca", width=0.55, edgecolor="white", linewidth=0.8)

for bar, total in zip(bars, adopter_totals):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(total),
        ha="center", va="bottom",
        fontsize=11, fontweight="bold", color="#333333",
    )

ax2.set_xticks(years)
ax2.set_xticklabels([str(y) for y in years], fontsize=12)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax2.set_ylabel("Number of Enterprises in S&P 500", fontsize=12)
ax2.set_xlabel("Year", fontsize=12)
ax2.set_title("Total AI Adopters in the Financial Sector by Year", fontsize=14, fontweight="bold")
ax2.set_ylim(0, max(adopter_totals) * 1.15)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("ai_adoption_totals.png", dpi=150, bbox_inches="tight")
