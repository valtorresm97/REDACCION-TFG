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

npx -y @mermaid-js/mermaid-cli "${ARGS[@]}" -b white -w 1200 -H 850 \
  -i images/uml/impl_backend_flujo_python.mmd \
  -o images/uml/impl_backend_flujo_python.png

npx -y @mermaid-js/mermaid-cli "${ARGS[@]}" -b white -w 1000 -H 800 \
  -i images/uml/impl_backend_buffer_ventana.mmd \
  -o images/uml/impl_backend_buffer_ventana.png

npx -y @mermaid-js/mermaid-cli "${ARGS[@]}" -b white -w 1000 -H 760 \
  -i images/uml/impl_backend_runtime_states.mmd \
  -o images/uml/impl_backend_runtime_states.png

ls -lh images/uml/impl_backend_*.png
