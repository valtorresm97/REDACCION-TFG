#!/usr/bin/env python3
"""Genera figuras temporales para la validación de montajes.

Salida:
- fig_02_mounting_timeseries_grid_ear.png
- fig_02_mounting_timeseries_grid_fp1fp2.png
- fig_02_mounting_timeseries_grid.png, versión 2x4 legacy por compatibilidad.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

EAR_CAPTURES = [
    ("M1 - Ear-EEG CH1 / reposo quieto", "20260523-195752_ear_eeg_ch1_only_still_30s"),
    ("M2 - Ear-EEG CH1 / ojos abiertos", "20260523-200925_ear_eeg_ch1_only_eyes_open_60s"),
    ("M3 - Ear-EEG CH1 / ojos cerrados", "20260523-201055_ear_eeg_ch1_only_eyes_closed_60s"),
    ("M4 - Ear-EEG CH1 / mandíbula", "20260523-201321_ear_eeg_ch1_only_jaw_movement_30s"),
]

FP1FP2_CAPTURES = [
    ("M5 - Fp1-Fp2 CH1 / reposo quieto", "20260523-202120_fp1_fp2_ch1_only_quiet_30s"),
    ("M6 - Fp1-Fp2 CH1 / ojos abiertos", "20260523-202208_fp1_fp2_ch1_only_eyes_open_60s"),
    ("M7 - Fp1-Fp2 CH1 / ojos cerrados", "20260523-202323_fp1_fp2_ch1_only_eyes_closed_60s"),
    ("M8 - Fp1-Fp2 CH1 / parpadeo/frente", "20260523-202451_fp1_fp2_ch1_only_forehead_blink_artifact_30s"),
]


def read_capture(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe: {csv_path}")

    df = pd.read_csv(
        csv_path,
        usecols=["sample_idx", "status", "ch1_uV"],
        on_bad_lines="skip",
    )
    df = df.dropna(subset=["sample_idx", "ch1_uV"]).copy()
    df["sample_idx"] = pd.to_numeric(df["sample_idx"], errors="coerce")
    df["ch1_uV"] = pd.to_numeric(df["ch1_uV"], errors="coerce")
    df["status"] = pd.to_numeric(df["status"], errors="coerce")
    df = df.dropna(subset=["sample_idx", "ch1_uV"]).sort_values("sample_idx")

    first_sample = float(df["sample_idx"].iloc[0])
    df["t_sec"] = (df["sample_idx"].astype(float) - first_sample) / 250.0
    return df


def annotate_integrity(ax, df: pd.DataFrame, fontsize: int = 8) -> None:
    gaps = int(df["sample_idx"].diff().fillna(1).ne(1).sum())
    invalid = int((df["status"] != 12582912).sum())
    ax.text(
        0.02,
        0.96,
        f"gaps={gaps}, invalid={invalid}",
        transform=ax.transAxes,
        va="top",
        fontsize=fontsize,
        bbox={"boxstyle": "round,pad=0.2", "alpha": 0.15},
    )


def plot_group(victor_root: Path, captures: list[tuple[str, str]], output: Path, title: str, ylim: float) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 7.6), sharey=True)
    axes = axes.ravel()

    for ax, (label, folder) in zip(axes, captures):
        csv_path = victor_root / "captures" / folder / "eeg_timeseries.csv"
        df = read_capture(csv_path)
        ax.plot(df["t_sec"], df["ch1_uV"], linewidth=0.55)
        ax.set_title(label, fontsize=10)
        ax.set_xlabel("Tiempo (s)")
        ax.grid(True, linewidth=0.3, alpha=0.35)
        ax.set_ylim(-ylim, ylim)
        annotate_integrity(ax, df, fontsize=8)

    axes[0].set_ylabel("CH1 (µV)")
    axes[2].set_ylabel("CH1 (µV)")
    fig.suptitle(title, fontsize=15)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(fig)


def plot_legacy_grid(victor_root: Path, output: Path, ylim: float) -> None:
    captures = EAR_CAPTURES + FP1FP2_CAPTURES
    fig, axes = plt.subplots(2, 4, figsize=(18, 7), sharey=True)
    axes = axes.ravel()

    for ax, (label, folder) in zip(axes, captures):
        csv_path = victor_root / "captures" / folder / "eeg_timeseries.csv"
        df = read_capture(csv_path)
        ax.plot(df["t_sec"], df["ch1_uV"], linewidth=0.5)
        ax.set_title(label, fontsize=8)
        ax.set_xlabel("Tiempo (s)")
        ax.grid(True, linewidth=0.3, alpha=0.35)
        ax.set_ylim(-ylim, ylim)
        annotate_integrity(ax, df, fontsize=7)

    axes[0].set_ylabel("CH1 (µV)")
    axes[4].set_ylabel("CH1 (µV)")
    fig.suptitle("Validación temporal por montaje y condición", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--victor-root", required=True, help="Ruta local al repositorio VICTOR-TFG")
    parser.add_argument("--output-dir", default="TFG_EEG_MIDI/images/validacion")
    parser.add_argument("--ylim", type=float, default=750.0, help="Límite vertical simétrico en microvoltios")
    args = parser.parse_args()

    victor_root = Path(args.victor_root).expanduser().resolve()
    output_dir = Path(args.output_dir).resolve()

    ear_output = output_dir / "fig_02_mounting_timeseries_grid_ear.png"
    fp_output = output_dir / "fig_02_mounting_timeseries_grid_fp1fp2.png"
    legacy_output = output_dir / "fig_02_mounting_timeseries_grid.png"

    plot_group(victor_root, EAR_CAPTURES, ear_output, "Validación temporal - montaje ear-EEG CH1", args.ylim)
    plot_group(victor_root, FP1FP2_CAPTURES, fp_output, "Validación temporal - montaje Fp1-Fp2 CH1", args.ylim)
    plot_legacy_grid(victor_root, legacy_output, args.ylim)

    print(f"Figura guardada: {ear_output}")
    print(f"Figura guardada: {fp_output}")
    print(f"Figura legacy guardada: {legacy_output}")


if __name__ == "__main__":
    main()
