#!/usr/bin/env python3
"""Plot historical upper limits for charged lepton flavor violation searches."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd

DEFAULT_OUTPUT = "muon_clfv_history.pdf"
MARKER_SIZE = 180

MUON_CHANNELS = (
    {
        "year": "MEG-year",
        "limit": "MEG-br",
        "marker": "v",
        "color": "#FF4500",
        "label": r"$\mu^+\to e^+\gamma$",
    },
    {
        "year": "ME2G-year",
        "limit": "ME2G-br",
        "marker": "^",
        "color": "#000080",
        "label": r"$\mu^+\to e^+\gamma\gamma$",
    },
    {
        "year": "Mu3e-year",
        "limit": "Mu3e-br",
        "marker": "o",
        "color": "#F4A460",
        "label": r"$\mu^+\to e^+e^-e^+$",
    },
    {
        "year": "Mu2em-year",
        "limit": "Mu2em-cr",
        "marker": "s",
        "color": "#006400",
        "label": r"$\mu~\mathrm{N}\to e~\mathrm{N}$",
    },
    {
        "year": "Mu2ep-year",
        "limit": "Mu2ep-cr",
        "marker": "s",
        "color": "#006400",
        "label": None,
    },
    {
        "year": "MACE-year",
        "limit": "MACE-cr",
        "marker": "D",
        "color": "purple",
        "label": r"$\mu^+e^-\to \mu^-e^+$",
    },
)

TAU_CHANNELS = (
    {
        "year": "TEG-year",
        "limit": "TEG-br",
        "marker": "v",
        "color": "cyan",
        "label": r"$\tau^+\to \mu^+\gamma$",
    },
)

FUTURE_LIMITS = (
    {"year": 2026, "limit": 1e-15, "marker": "o", "color": "#F4A460"},
    {"year": 2030, "limit": 1e-16, "marker": "o", "color": "#F4A460"},
    {"year": 2027, "limit": 6.2e-16, "marker": "s", "color": "#006400"},
    {"year": 2030, "limit": 6e-17, "marker": "s", "color": "#006400"},
    {"year": 2027, "limit": 7e-15, "marker": "s", "color": "#006400"},
    {"year": 2030, "limit": 3.2e-17, "marker": "s", "color": "#006400"},
    {"year": 2027, "limit": 6e-14, "marker": "v", "color": "#FF4500"},
    {"year": 2030, "limit": 1.3e-13, "marker": "D", "color": "purple"},
    {"year": 2028, "limit": 1e-12, "marker": "^", "color": "#000080"},
)


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Plot historical upper limits for charged lepton flavor violation searches."
    )
    parser.add_argument(
        "--muon-data",
        type=Path,
        default=script_dir / "muon_clfv_history.csv",
        help="Path to the muon CLFV history CSV file.",
    )
    parser.add_argument(
        "--tau-data",
        type=Path,
        default=script_dir / "tau_clfv_history.csv",
        help="Path to the tau CLFV history CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=script_dir / DEFAULT_OUTPUT,
        help="Path for the output figure.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the figure in an interactive window after saving it.",
    )
    return parser.parse_args()


def read_history(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def plot_channel(ax: plt.Axes, data: pd.DataFrame, channel: dict[str, str | None]) -> None:
    rows = data[[channel["year"], channel["limit"]]].dropna()
    ax.scatter(
        rows[channel["year"]],
        rows[channel["limit"]],
        marker=channel["marker"],
        color=channel["color"],
        s=MARKER_SIZE,
        label=channel["label"],
    )


def plot_future_limits(ax: plt.Axes) -> None:
    for limit in FUTURE_LIMITS:
        ax.scatter(
            limit["year"],
            limit["limit"],
            marker=limit["marker"],
            edgecolor=limit["color"],
            facecolor="#DCDCDC",
            s=MARKER_SIZE,
        )


def configure_axes(ax: plt.Axes) -> None:
    ax.set_yscale("log")
    ax.set_xlabel("Year", loc="right")
    ax.set_xlim(1940, 2040)
    ax.set_ylabel("Upper limits", loc="top")
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.grid(True, which="major", linestyle="--", linewidth=0.5)

    legend = ax.legend(frameon=True, loc="upper right")
    for handle in legend.legend_handles:
        handle.set_alpha(1)


def set_plot_style() -> None:
    plt.rcParams.update(
        {
            "axes.labelsize": 30,
            "xtick.labelsize": 26,
            "ytick.labelsize": 26,
            "legend.fontsize": 20,
        }
    )


def build_plot(muon_history: pd.DataFrame, tau_history: pd.DataFrame) -> plt.Figure:
    set_plot_style()
    fig, ax = plt.subplots(figsize=(16, 9))

    for channel in MUON_CHANNELS:
        plot_channel(ax, muon_history, channel)
    for channel in TAU_CHANNELS:
        plot_channel(ax, tau_history, channel)

    plot_future_limits(ax)
    configure_axes(ax)
    fig.tight_layout()
    return fig


def main() -> None:
    args = parse_args()
    muon_history = read_history(args.muon_data)
    tau_history = read_history(args.tau_data)
    figure = build_plot(muon_history, tau_history)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output)
    if args.show:
        plt.show()
    plt.close(figure)


if __name__ == "__main__":
    main()
