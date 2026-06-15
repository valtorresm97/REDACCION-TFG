#!/usr/bin/env python3
"""Construye una figura 2x4 con las señales temporales de validación de montaje.

Uso desde la raiz de REDACCION-TFG:

    python TFG_EEG_MIDI/images/validacion/build_mounting_timeseries_grid.py ^
        --victor-root C:/ruta/a/VICTOR-TFG

La salida se guarda en:

    TFG_EEG_MIDI/images/validacion/fig_02_mounting_timeseries_grid.png

El script lee los CSV del repositorio técnico VICTOR-TFG y no modifica esos datos.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CAPTURES = [
    (
        "Ear-EEG CH1 / reposo",
        "20260523-195752_ear_eeg_ch1_only_still_30s",
    ),
    (
        "Ear-EEG CH1 / ojos abiertos",
        "20260523-200925_ear_eeg_ch1_only_eyes_open_60s",
    ),
    (
        "Ear-EEG CH1 / ojos cerrados",
        "20260523-201055_ear_eeg_ch1_only_eyes_closed_60s",
    ),
    (
        "Ear-EEG CH1 / mandíbula",
        "20260523-201321_ear_eeg_ch1_only_jaw_movement_30s",
    ),
    (
        "Fp1-Fp2 CH1 / reposo",
        "20260523-202120_fp1_fp2_ch1_only_quiet_30s",
    ),
    (
        "Fp1-Fp2 CH1 / ojos abiertos",
        "20260523-202208_fp1_fp2_ch1_only_eyes_open_60s",
    ),
    (
        "Fp1-Fp2 CH1 / ojos cerrados",
        "20260523-202323_fp1_fp2_ch1_only_eyes_closed_60s",
    ),
    (
        "Fp1-Fp2 CH1 / parpadeo/frente",
        "20260523-202451_fp1_fp2_ch1_only_forehead_blink_artifact_30s",
    ),
]


def read_capture(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe: {csv_path}")

    df = pd.read_csv(csv_path, usecols=["t_capture_sec", "sample_idx", "status", "ch1_uV"])
    df = df.dropna(subset=["sample_idx", "ch1_uV"])
    df = df.sort_values("sample_idx")

    # El timestamp de bloque se repite para 8 muestras. Para representar una señal temporal
    # continua se reconstruye el tiempo con el índice de muestra y fs=250 Hz.
    first_sample = float(df["sample_idx"].iloc[0])
    df["t_sec"] = (df["sample_idx"].astype(float) - first_sample) / 250.0
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--victor-root",
        required=True,
        help="Ruta local al repositorio VICTOR-TFG",
    )
    parser.add_argument(
        "--output",
        default="TFG_EEG_MIDI/images/validacion/fig_02_mounting_timeseries_grid.png",
        help="Ruta de salida dentro de REDACCION-TFG",
    )
    parser.add_argument(
        "--ylim",
        type=float,
        default=750.0,
        help="Límite vertical simétrico en microvoltios",
    )
    args = parser.parse_args()

    victor_root = Path(args.victor_root).expanduser().resolve()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 4, figsize=(18, 7), sharey=True)
    axes = axes.ravel()

    missing = []
    for ax, (title, folder) in zip(axes, CAPTURES):
        csv_path = victor_root / "captures" / folder / "eeg_timeseries.csv"
        try:
            df = read_capture(csv_path)
        except FileNotFoundError:
            missing.append(str(csv_path))
            ax.text(0.5, 0.5, "CSV no encontrado", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(title, fontsize=9)
            ax.set_axis_off()
            continue

        ax.plot(df["t_sec"], df["ch1_uV"], linewidth=0.55)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("Tiempo (s)")
        ax.grid(True, linewidth=0.3, alpha=0.35)
        ax.set_ylim(-args.ylim, args.ylim)

        gaps = int(df["sample_idx"].diff().fillna(1).ne(1).sum())
        invalid = int((df["status"] != 12582912).sum())
        ax.text(
            0.02,
            0.96,
            f"gaps={gaps}, invalid={invalid}",
            transform=ax.transAxes,
            va="top",
            fontsize=7,
            bbox={"boxstyle": "round,pad=0.2", "alpha": 0.15},
        )

    axes[0].set_ylabel("CH1 (µV)")
    axes[4].set_ylabel("CH1 (µV)")
    fig.suptitle("Validación temporal por montaje y condición", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output, dpi=220)
    plt.close(fig)

    if missing:
        print("Aviso: faltan CSV:")
        for path in missing:
            print(f" - {path}")
    print(f"Figura guardada en: {output}")


if __name__ == "__main__":
    main()
