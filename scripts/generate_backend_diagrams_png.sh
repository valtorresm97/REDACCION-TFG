#!/usr/bin/env bash
set -euo pipefail

# Ejecutar desde la carpeta TFG_EEG_MIDI
# cd TFG_EEG_MIDI

CONFIG="../puppeteer-config.json"
ARGS=()
if [[ -f "$CONFIG" ]]; then
  ARGS=(-p "$CONFIG")
else
  echo "No encuentro ../puppeteer-config.json. Intento usar Puppeteer por defecto." >&2
fi

render() {
  local input="$1"
  local output="$2"
  local width="$3"
  local height="$4"
  if [[ ! -f "$input" ]]; then
    echo "No existe $input" >&2
    exit 1
  fi
  npx -y @mermaid-js/mermaid-cli "${ARGS[@]}" -b white -w "$width" -H "$height" \
    -i "$input" \
    -o "$output"
}

render images/uml/impl_backend_flujo_python.mmd images/uml/impl_backend_flujo_python.png 1400 950
render images/uml/impl_backend_buffer_ventana.mmd images/uml/impl_backend_buffer_ventana.png 1400 950
render images/uml/impl_backend_features_quality.mmd images/uml/impl_backend_features_quality.png 1400 850
render images/uml/impl_backend_runtime_states.mmd images/uml/impl_backend_runtime_states.png 1300 950

render images/uml/impl_sonificacion_flujo.mmd images/uml/impl_sonificacion_flujo.png 1800 1250
render images/uml/impl_sonificacion_controles.mmd images/uml/impl_sonificacion_controles.png 1500 1050
render images/uml/impl_sonificacion_quality_gate.mmd images/uml/impl_sonificacion_quality_gate.png 1500 1050
render images/uml/impl_sonificacion_segmento_compas_nota.mmd images/uml/impl_sonificacion_segmento_compas_nota.png 1600 950
render images/uml/impl_midi_eventos_bytes.mmd images/uml/impl_midi_eventos_bytes.png 1600 900

ls -lh images/uml/impl_*.png
