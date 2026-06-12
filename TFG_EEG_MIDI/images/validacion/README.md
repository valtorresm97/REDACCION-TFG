# Figuras de validación

La sección `sections/validacion_resultados.tex` referencia varias figuras en esta carpeta mediante nombres preparados para la memoria.

Estado actual:

- La redacción de las subsecciones 7.1--7.4 ya está integrada en `sections/validacion_resultados.tex`.
- El LaTeX usa una macro con `\IfFileExists`, de modo que el documento puede compilar aunque falten imágenes; en ese caso aparece un recuadro indicando la figura pendiente.
- Las figuras proceden del paquete documental `7.zip`, carpeta `validacion_tfg/figures/`.

Figuras compuestas esperadas por la sección:

```text
val_shorted_inputs_timeseries.jpg
val_mounting_metrics_grid.jpg
val_mounting_quality_score.jpg
val_quality_timeline_grid.jpg
val_quality_state_distribution.jpg
val_state_timeseries_grid.jpg
val_eyes_closed_timeseries_grid.jpg
val_state_psd_grid.jpg
val_eyes_closed_psd_grid.jpg
val_periodogram_multitaper_global_grid.jpg
val_spectrogram_state_bar.jpg
val_windowed_bandpowers.jpg
val_alpha_alpha_beta_grid.jpg
val_bands_robustness_grid.jpg
```

Estas figuras son composiciones preparadas a partir de los PNG originales para evitar llenar la memoria con demasiadas imágenes independientes.

Si se trabaja localmente, copiar o generar esas figuras en:

```text
TFG_EEG_MIDI/images/validacion/
```

Figuras originales usadas como fuente:

```text
fig_01_shorted_inputs_timeseries.png
fig_02_mounting_rms_comparison.png
fig_02_mounting_ptp_comparison.png
fig_02_mounting_50hz_comparison.png
fig_02_mounting_artifact_fraction.png
fig_02_mounting_quality_score.png
fig_00_final_capture_rms_timeline.png
fig_00_final_capture_quality_timeline.png
fig_11_quality_state_distribution.png
fig_03_state_ojos_abiertos_reposo_timeseries.png
fig_03_state_recuperacion_1_timeseries.png
fig_03_state_mandibula_timeseries.png
fig_03_state_parpadeo_frente_timeseries.png
fig_03_state_ojos_cerrados_reposo_1_timeseries.png
fig_03_state_ojos_cerrados_reposo_2_timeseries.png
fig_03_state_ojos_abiertos_reposo_psd.png
fig_03_state_recuperacion_1_psd.png
fig_03_state_mandibula_psd.png
fig_03_state_parpadeo_frente_psd.png
fig_03_state_ojos_cerrados_reposo_1_psd.png
fig_03_state_ojos_cerrados_reposo_2_psd.png
fig_04_periodogram_by_state.png
fig_04_multitaper_psd_by_state.png
fig_04_spectrogram_with_state_bar.png
fig_08_windowed_bandpowers.png
fig_07_eyes_open_vs_closed_alpha.png
fig_05_alpha_beta_ratio_comparison.png
fig_05_relative_bandpowers_by_mounting.png
fig_05_feature_robustness_heatmap.png
```
