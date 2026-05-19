"""Volcanic eruption analysis plots — mirrors earthquake/famines pattern.

Conventions:
- Detection-clean for VEI≥5 since ~1500 globally; pre-1500 entries excluded
- VEI is roughly logarithmic; VEI 5/6/7 are decade-equivalents of M5/M6/M7
- Cumulative-vs-constant-rate for VEI≥6 (~once per generation)
- Power-law on tail
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
PLOTS = HERE / "plots"
PLOTS.mkdir(exist_ok=True)

CATALOG_START = 1500
GREAT_VEI = 6
PARTIAL_DECADE_START = 2020

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.size": 10, "axes.titlesize": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linestyle": "--",
})


def load_events() -> pd.DataFrame:
    df = pd.read_csv(HERE / "volcanoes.csv")
    df["vei"] = df["vei"].astype(str).str.extract(r"(\d+)")[0].astype(float)
    df = df[df["vei"] >= 5].copy()
    df["deaths_estimate"] = pd.to_numeric(df["deaths_estimate"], errors="coerce").fillna(0)
    return df


def plot_01_vei_timeline(df: pd.DataFrame):
    """Scatter of VEI vs year with deaths bubble size."""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    sizes = np.where(df["deaths_estimate"] > 0,
                       np.sqrt(df["deaths_estimate"] + 1) * 5 + 30,
                       60)
    colors = ["#cc3322" if v >= GREAT_VEI else "#ee9933" for v in df["vei"]]
    ax.scatter(df["year"], df["vei"], s=sizes, c=colors, alpha=0.7,
                edgecolor="black", linewidth=0.6)
    ax.set_xlabel("Year")
    ax.set_ylabel("VEI")
    ax.set_yticks([5, 6, 7])
    ax.set_title("VEI≥5 eruptions over time — bubble size ∝ √deaths, red = VEI≥6")
    for _, row in df.iterrows():
        if row["vei"] >= GREAT_VEI or row["deaths_estimate"] >= 5000:
            ax.annotate(row["name"].split(" (")[0][:18], (row["year"], row["vei"]),
                         xytext=(5, 5), textcoords="offset points",
                         fontsize=8, alpha=0.85)
    ax.set_xlim(CATALOG_START - 20, 2030)
    plt.tight_layout()
    plt.savefig(PLOTS / "01_vei_timeline.png")
    plt.close()


def plot_02_decadal_counts_by_vei(df: pd.DataFrame):
    """Stacked bars: eruptions per decade by VEI band."""
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10
    bands = [(5, 6, "VEI 5", "#bbdd99"),
             (6, 7, "VEI 6", "#dd9966"),
             (7, 99, "VEI 7+", "#cc3322")]
    fig, ax = plt.subplots(figsize=(11, 5))
    decades = np.arange(CATALOG_START, 2030, 10)
    bottom = np.zeros(len(decades))
    for lo, hi, label, color in bands:
        counts = []
        for d in decades:
            n = ((df["decade"] == d) & (df["vei"] >= lo) & (df["vei"] < hi)).sum()
            counts.append(n)
        ax.bar(decades, counts, width=8, bottom=bottom, label=label,
                color=color, edgecolor="black", linewidth=0.4)
        bottom += counts
    ax.axvspan(PARTIAL_DECADE_START, PARTIAL_DECADE_START + 10,
                color="grey", alpha=0.18, label="partial")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Eruptions per decade")
    ax.set_title(f"Eruptions per decade by VEI band (catalog ≥{CATALOG_START})")
    ax.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(PLOTS / "02_decadal_counts_by_vei.png")
    plt.close()


def plot_03_great_eruption_timing(df: pd.DataFrame):
    """Cumulative VEI≥6 vs constant-rate reference + inter-event intervals."""
    great = df[df["vei"] >= GREAT_VEI].sort_values("year").reset_index(drop=True)
    great["n"] = np.arange(1, len(great) + 1)
    if len(great) < 2:
        return
    span_yr = great["year"].iloc[-1] - CATALOG_START
    rate = len(great) / span_yr
    yrs = np.arange(CATALOG_START, 2026)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    ax.step(great["year"], great["n"], where="post",
            color="#cc3322", linewidth=2, label="Observed cumulative VEI≥6")
    ax.plot(yrs, rate * (yrs - CATALOG_START), color="gray", linestyle="--",
            label=f"Constant rate ({rate:.3f}/yr ≈ once per {1/rate:.0f}yr)")
    for _, row in great.iterrows():
        ax.annotate(row["name"].split(" (")[0][:15],
                    (row["year"], row["n"]),
                    xytext=(3, -10), textcoords="offset points",
                    fontsize=7, alpha=0.7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative VEI≥6 count")
    ax.set_title(f"VEI≥6 cumulative vs constant-rate ({CATALOG_START}+)")
    ax.legend()

    ax = axes[1]
    intervals = np.diff(great["year"].values)
    if len(intervals) > 0:
        ax.bar(range(len(intervals)), intervals,
                color="#cc3322", alpha=0.7, edgecolor="black", linewidth=0.4)
        ax.axhline(intervals.mean(), color="gray", linestyle="--",
                    label=f"mean = {intervals.mean():.1f} yr")
        labels = [f"{a}→{b}" for a, b in zip(great["year"].values[:-1],
                                              great["year"].values[1:])]
        ax.set_xticks(range(len(intervals)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Years between VEI≥6 events")
        ax.set_title("Inter-event intervals")
        ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS / "03_great_eruption_timing.png")
    plt.close()


def plot_04_vei_distribution(df: pd.DataFrame):
    """VEI histogram + survival curve."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    counts = df["vei"].value_counts().sort_index()
    ax.bar(counts.index, counts.values, color="#ee9933", edgecolor="black", linewidth=0.4)
    ax.set_xlabel("VEI")
    ax.set_ylabel("Eruption count")
    ax.set_title(f"VEI distribution (catalog ≥{CATALOG_START})")
    ax.set_xticks([5, 6, 7])

    ax = axes[1]
    vei_sorted = np.sort(df["vei"].values)[::-1]
    survival = np.arange(1, len(vei_sorted) + 1)
    ax.semilogy(vei_sorted, survival, "o-", color="#cc3322", markeredgecolor="black")
    ax.set_xlabel("VEI threshold")
    ax.set_ylabel("Survival count (log)")
    ax.set_title("Survival function — each step is half of a VEI band increase")
    plt.tight_layout()
    plt.savefig(PLOTS / "04_vei_distribution.png")
    plt.close()


def main():
    df = load_events()
    print(f"Loaded {len(df)} VEI≥5 eruptions; {int(df['year'].min())}–{int(df['year'].max())}")
    print(f"VEI≥6: {(df['vei'] >= 6).sum()}; VEI≥7: {(df['vei'] >= 7).sum()}")
    plot_01_vei_timeline(df)
    plot_02_decadal_counts_by_vei(df)
    plot_03_great_eruption_timing(df)
    plot_04_vei_distribution(df)
    print(f"Wrote 4 plots to {PLOTS}/")


if __name__ == "__main__":
    main()
