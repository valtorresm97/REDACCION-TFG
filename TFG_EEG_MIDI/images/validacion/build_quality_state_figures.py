#!/usr/bin/env python3
"""Genera figuras de validación de calidad para la captura mixed_states.

Salida en TFG_EEG_MIDI/images/validacion:
- fig_03_mixed_states_temporal_750uv.png
- fig_03_state_timeseries_grid.png
- fig_03_state_psd_grid.png

El script lee la captura y la tabla de estados desde VICTOR-TFG.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CAPTURE_FOLDER = "20260524-122200_final_atenuacion_artefactos_mixed_states"
CSV_REL = Path("captures") / CAPTURE_FOLDER / "eeg_timeseries.csv"
STATS_REL = Path("docs") / "validacion_tfg" / "tables" / "table_03_mixed_state_stats.csv"
FS = 250.0
VALID_STATUS = 12582912

STATE_COLORS = {
    "ojos_abiertos_reposo": "tab:blue",
    "ojos_cerrados_reposo_1": "tab:orange",
    "mandibula": "tab:red",
    "recuperacion_1": "tab:green",
    "parpadeo_frente": "tab:purple",
    "recuperacion_2": "tab:olive",
    "ojos_cerrados_reposo_2": "tab:brown",
}


def read_capture(victor_root: Path) -> pd.DataFrame:
    csv_path = victor_root / CSV_REL
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe la captura: {csv_path}")

    df = pd.read_csv(csv_path, usecols=["sample_idx", "status", "ch1_uV"], on_bad_lines="skip")
    df = df.dropna(subset=["sample_idx", "ch1_uV"]).copy()
    df["sample_idx"] = pd.to_numeric(df["sample_idx"], errors="coerce")
    df["status"] = pd.to_numeric(df["status"], errors="coerce")
    df["ch1_uV"] = pd.to_numeric(df["ch1_uV"], errors="coerce")
    df = df.dropna(subset=["sample_idx", "ch1_uV"]).sort_values("sample_idx")

    first_sample = float(df["sample_idx"].iloc[0])
    df["t_sec"] = (df["sample_idx"].astype(float) - first_sample) / FS
    return df


def read_states(victor_root: Path) -> pd.DataFrame:
    stats_path = victor_root / STATS_REL
    if not stats_path.exists():
        raise FileNotFoundError(f"No existe la tabla de estados: {stats_path}")

    states = pd.read_csv(stats_path)
    states["start_sec"] = pd.to_numeric(states["start_sec"], errors="coerce")
    states["stop_sec"] = pd.to_numeric(states["stop_sec"], errors="coerce")
    return states.dropna(subset=["start_sec", "stop_sec"])


def annotate_integrity(ax, segment: pd.DataFrame) -> None:
    gaps = int(segment["sample_idx"].diff().fillna(1).ne(1).sum())
    invalid = int((segment["status"] != VALID_STATUS).sum())
    ax.text(
        0.02,
        0.95,
        f"gaps={gaps}, invalid={invalid}",
        transform=ax.transAxes,
        va="top",
        fontsize=7,
        bbox={"boxstyle": "round,pad=0.2", "alpha": 0.15},
    )


def plot_global(df: pd.DataFrame, states: pd.DataFrame, output: Path, ylim: float) -> None:
    fig, ax = plt.subplots(figsize=(15, 5.8))
    ax.plot(df["t_sec"], df["ch1_uV"], linewidth=0.55)

    y_text = ylim * 0.90
    for _, row in states.iterrows():
        state = str(row["state"])
        label = str(row["label"])
        start = float(row["start_sec"])
        stop = float(row["stop_sec"])
        color = STATE_COLORS.get(state, "0.7")
        ax.axvspan(start, stop, alpha=0.14, color=color)
        ax.text((start + stop) / 2, y_text, label, ha="center", va="top", fontsize=8, rotation=0)

    ax.set_ylim(-ylim, ylim)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("CH1 (µV)")
    ax.set_title("Captura temporal completa para validación de calidad (escala ±750 µV)")
    ax.grid(True, linewidth=0.3, alpha=0.35)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(fig)


def segment_df(df: pd.DataFrame, start: float, stop: float) -> pd.DataFrame:
    return df[(df["t_sec"] >= start) & (df["t_sec"] < stop)].copy()


def plot_state_timeseries(df: pd.DataFrame, states: pd.DataFrame, output: Path, ylim: float) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(16, 7.6), sharey=True)
    axes = axes.ravel()

    for ax, (_, row) in zip(axes, states.iterrows()):
        start = float(row["start_sec"])
        stop = float(row["stop_sec"])
        label = str(row["label"])
        state = str(row["state"])
        seg = segment_df(df, start, stop)
        t_local = seg["t_sec"] - start

        ax.plot(t_local, seg["ch1_uV"], linewidth=0.55, color=STATE_COLORS.get(state, None))
        ax.set_title(f"{label} ({start:.0f}-{stop:.0f} s)", fontsize=9)
        ax.set_xlabel("Tiempo local (s)")
        ax.set_ylim(-ylim, ylim)
        ax.grid(True, linewidth=0.3, alpha=0.35)
        annotate_integrity(ax, seg)

    for ax in axes[len(states):]:
        ax.set_axis_off()

    axes[0].set_ylabel("CH1 (µV)")
    axes[4].set_ylabel("CH1 (µV)")
    fig.suptitle("Señal temporal por estados - validación de calidad", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(fig)


def compute_psd_uV2_hz(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 16:
        return np.array([]), np.array([])

    values = values - np.mean(values)
    window = np.hanning(values.size)
    xw = values * window
    spec = np.fft.rfft(xw)
    freqs = np.fft.rfftfreq(values.size, d=1.0 / FS)
    scale = FS * np.sum(window ** 2)
    psd = (np.abs(spec) ** 2) / scale
    if psd.size > 2:
        psd[1:-1] *= 2.0
    return freqs, psd


def plot_state_psd(df: pd.DataFrame, states: pd.DataFrame, output: Path) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(16, 7.6), sharey=True)
    axes = axes.ravel()

    for ax, (_, row) in zip(axes, states.iterrows()):
        start = float(row["start_sec"])
        stop = float(row["stop_sec"])
        label = str(row["label"])
        state = str(row["state"])
        seg = segment_df(df, start, stop)
        freqs, psd = compute_psd_uV2_hz(seg["ch1_uV"].to_numpy())

        mask = (freqs >= 0.5) & (freqs <= 50.0)
        ax.plot(freqs[mask], 10.0 * np.log10(psd[mask] + 1e-18), linewidth=0.7, color=STATE_COLORS.get(state, None))
        ax.set_title(f"{label} ({start:.0f}-{stop:.0f} s)", fontsize=9)
        ax.set_xlabel("Frecuencia (Hz)")
        ax.grid(True, linewidth=0.3, alpha=0.35)
        ax.axvline(50.0, linewidth=0.7, linestyle="--", alpha=0.45)

    for ax in axes[len(states):]:
        ax.set_axis_off()

    axes[0].set_ylabel("PSD (dB µV²/Hz)")
    axes[4].set_ylabel("PSD (dB µV²/Hz)")
    fig.suptitle("PSD por estados - validación de calidad", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--victor-root", required=True, help="Ruta local al repositorio VICTOR-TFG")
    parser.add_argument("--output-dir", default="TFG_EEG_MIDI/images/validacion")
    parser.add_argument("--ylim", type=float, default=750.0)
    args = parser.parse_args()

    victor_root = Path(args.victor_root).expanduser().resolve()
    output_dir = Path(args.output_dir).resolve()

    df = read_capture(victor_root)
    states = read_states(victor_root)

    plot_global(df, states, output_dir / "fig_03_mixed_states_temporal_750uv.png", args.ylim)
    plot_state_timeseries(df, states, output_dir / "fig_03_state_timeseries_grid.png", args.ylim)
    plot_state_psd(df, states, output_dir / "fig_03_state_psd_grid.png")

    print(f"Figura guardada: {output_dir / 'fig_03_mixed_states_temporal_750uv.png'}")
    print(f"Figura guardada: {output_dir / 'fig_03_state_timeseries_grid.png'}")
    print(f"Figura guardada: {output_dir / 'fig_03_state_psd_grid.png'}")


if __name__ == "__main__":
    main()
