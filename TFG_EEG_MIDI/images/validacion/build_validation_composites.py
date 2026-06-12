from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent


def _font(size: int = 34):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for item in candidates:
        try:
            return ImageFont.truetype(item, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _open_rgb(filename: str) -> Image.Image:
    path = BASE / filename
    if not path.exists():
        raise FileNotFoundError(f"Falta la figura fuente: {path}")
    return Image.open(path).convert("RGB")


def _resize_w(im: Image.Image, width: int) -> Image.Image:
    if im.width == width:
        return im
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


def standalone(source: str, target: str, width: int = 1300) -> None:
    im = _resize_w(_open_rgb(source), width)
    im.save(BASE / target, quality=84, optimize=True, progressive=True)
    print(f"OK {target}")


def grid(files: list[str], labels: list[str], target: str, cols: int = 2, cellw: int = 900) -> None:
    font = _font()
    margin = 35
    label_h = 44
    ims = [_resize_w(_open_rgb(f), cellw) for f in files]
    rows = (len(ims) + cols - 1) // cols
    cellh = max(im.height for im in ims) + label_h
    canvas = Image.new("RGB", (cols * cellw + (cols + 1) * margin, rows * cellh + (rows + 1) * margin), "white")
    draw = ImageDraw.Draw(canvas)

    for i, im in enumerate(ims):
        row = i // cols
        col = i % cols
        x = margin + col * (cellw + margin)
        y = margin + row * (cellh + margin)
        draw.text((x, y), labels[i], fill=(0, 0, 0), font=font)
        canvas.paste(im, (x, y + label_h))

    canvas.save(BASE / target, quality=84, optimize=True, progressive=True)
    print(f"OK {target}")


def main() -> None:
    standalone("fig_01_shorted_inputs_timeseries.png", "val_shorted_inputs_timeseries.jpg")
    standalone("fig_02_mounting_quality_score.png", "val_mounting_quality_score.jpg")
    standalone("fig_11_quality_state_distribution.png", "val_quality_state_distribution.jpg")
    standalone("fig_04_spectrogram_with_state_bar.png", "val_spectrogram_state_bar.jpg")
    standalone("fig_08_windowed_bandpowers.png", "val_windowed_bandpowers.jpg")

    grid(
        [
            "fig_02_mounting_rms_comparison.png",
            "fig_02_mounting_ptp_comparison.png",
            "fig_02_mounting_50hz_comparison.png",
            "fig_02_mounting_artifact_fraction.png",
        ],
        ["(a) RMS mediano", "(b) Amplitud pico a pico", "(c) Componente de 50 Hz", "(d) Fracción de artefactos"],
        "val_mounting_metrics_grid.jpg",
    )

    grid(
        ["fig_00_final_capture_rms_timeline.png", "fig_00_final_capture_quality_timeline.png"],
        ["(a) RMS por ventanas", "(b) Índice de calidad por ventanas"],
        "val_quality_timeline_grid.jpg",
    )

    grid(
        [
            "fig_03_state_ojos_abiertos_reposo_timeseries.png",
            "fig_03_state_recuperacion_1_timeseries.png",
            "fig_03_state_mandibula_timeseries.png",
            "fig_03_state_parpadeo_frente_timeseries.png",
        ],
        ["(a) Ojos abiertos / reposo", "(b) Recuperación 1", "(c) Mandíbula", "(d) Parpadeo / frente"],
        "val_state_timeseries_grid.jpg",
    )

    grid(
        ["fig_03_state_ojos_cerrados_reposo_1_timeseries.png", "fig_03_state_ojos_cerrados_reposo_2_timeseries.png"],
        ["(a) Ojos cerrados / reposo 1", "(b) Ojos cerrados / reposo 2"],
        "val_eyes_closed_timeseries_grid.jpg",
    )

    grid(
        [
            "fig_03_state_ojos_abiertos_reposo_psd.png",
            "fig_03_state_recuperacion_1_psd.png",
            "fig_03_state_mandibula_psd.png",
            "fig_03_state_parpadeo_frente_psd.png",
        ],
        ["(a) Ojos abiertos / reposo", "(b) Recuperación 1", "(c) Mandíbula", "(d) Parpadeo / frente"],
        "val_state_psd_grid.jpg",
    )

    grid(
        ["fig_03_state_ojos_cerrados_reposo_1_psd.png", "fig_03_state_ojos_cerrados_reposo_2_psd.png"],
        ["(a) Ojos cerrados / reposo 1", "(b) Ojos cerrados / reposo 2"],
        "val_eyes_closed_psd_grid.jpg",
    )

    grid(
        ["fig_04_periodogram_by_state.png", "fig_04_multitaper_psd_by_state.png"],
        ["(a) Periodograma por estado", "(b) PSD multitaper por estado"],
        "val_periodogram_multitaper_global_grid.jpg",
    )

    grid(
        ["fig_07_eyes_open_vs_closed_alpha.png", "fig_05_alpha_beta_ratio_comparison.png"],
        ["(a) Alpha ojos abiertos/cerrados", "(b) Relación alpha/beta"],
        "val_alpha_alpha_beta_grid.jpg",
        cellw=850,
    )

    grid(
        ["fig_05_relative_bandpowers_by_mounting.png", "fig_05_feature_robustness_heatmap.png"],
        ["(a) Potencias relativas por montaje", "(b) Robustez de características"],
        "val_bands_robustness_grid.jpg",
        cellw=850,
    )


if __name__ == "__main__":
    main()
