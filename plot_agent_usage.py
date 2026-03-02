import matplotlib.pyplot as plt
import numpy as np

functions = [
    "Supply chain/inventory mgmt",
    "Manufacturing",
    "IT",
    "Product and/or service dev",
    "Software engineering",
    "Knowledge management",
    "Marketing and sales",
    "Strategy and corporate finance",
    "Human resources",
    "Service operations",
    "Risk, legal, and compliance",
]
values = [0, 1, 3, 3, 3, 4, 4, 4, 4, 5, 7]

fig, ax = plt.subplots(figsize=(10, 6))

y = np.arange(len(functions))
bar_color = "#428bca"
bars = ax.barh(y, values, height=0.6, color=bar_color, edgecolor="white", linewidth=0.6)

for bar, val in zip(bars, values):
    if val > 0:
        ax.text(
            bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
            f"{val}%", va="center", ha="left", fontsize=10, fontweight="bold", color="#333333",
        )
    else:
        ax.text(
            0.15, bar.get_y() + bar.get_height() / 2,
            "0%", va="center", ha="left", fontsize=10, color="#999999",
        )

ax.set_yticks(y)
ax.set_yticklabels(functions, fontsize=11)
ax.set_xlabel("% of survey respondents", fontsize=12)
ax.set_xlim(0, max(values) + 1.5)

ax.set_title(
    "Use of AI Agents in Financial Institutions by Business Function",
    fontsize=14, fontweight="bold", pad=14,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("agent_usage_by_function.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.show()
