import io
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

df = pd.read_csv("bloom_adoption_by_category_country.csv")

category_map = {
    "Data processing using ML": "Data",
    "Visual content creation": "Visual",
    "Text generation using LLMs": "Text",
    "Image processing using ML": "Image",
}
df = df[df["Category"].isin(category_map)].copy()
df["Category"] = df["Category"].map(category_map)

category_order = ["Image", "Data", "Visual", "Text"]
df["Category"] = pd.Categorical(df["Category"], categories=category_order, ordered=True)
df = df.sort_values("Category")

countries = {
    "US SBU (N=1032)": ("us", "US"),
    "UK DMP (N=1972)": ("gb", "UK"),
    "DE BOP-F (N=2282)": ("de", "DE"),
    "AUS BOSS (N=602)": ("au", "AU"),
}

FLAG_WIDTH = 40
flag_images = {}
for col, (iso, _label) in countries.items():
    url = f"https://flagcdn.com/w{FLAG_WIDTH}/{iso}.png"
    with urllib.request.urlopen(url) as resp:
        flag_images[col] = Image.open(io.BytesIO(resp.read())).convert("RGBA")

fig, ax = plt.subplots(figsize=(10, 5))

y_positions = {cat: i for i, cat in enumerate(category_order)}
zoom = 0.55
offsets = np.linspace(-0.18, 0.18, len(countries))

for idx, (col, (iso, label)) in enumerate(countries.items()):
    for _, row in df.iterrows():
        cat = row["Category"]
        x = row[col]
        y = y_positions[cat] + offsets[idx]

        flag_img = flag_images[col]
        im = OffsetImage(np.array(flag_img), zoom=zoom)
        ab = AnnotationBbox(im, (x, y), frameon=False)
        ax.add_artist(ab)

ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels(category_order, fontsize=13, fontweight="medium")
ax.set_xlabel("Adoption Rate (%)", fontsize=13)
ax.set_xlim(5, 62)
ax.set_ylim(-0.6, len(category_order) - 0.4)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle="--", alpha=0.4)

for i in range(len(category_order) - 1):
    ax.axhline(i + 0.5, color="#cccccc", linewidth=0.8, linestyle="-", zorder=0)

ax.set_title(
    "AI Technology Adoption by Category and Country",
    fontsize=15, fontweight="bold", pad=16,
)

plt.tight_layout()
plt.savefig("bloom_adoption_by_category_country.png", dpi=180, bbox_inches="tight",
            facecolor="white")
plt.show()
