# Ejecutar desde la carpeta TFG_EEG_MIDI
# cd "C:\Users\PC\Documents\REDACCIÓN TFG\TFG_EEG_MIDI"
# Recomendado para LaTeX: usar PNG. Este PDF queda como alternativa.

$ErrorActionPreference = "Stop"
$PuppeteerConfig = "..\puppeteer-config.json"

if (Test-Path $PuppeteerConfig) {
    $PuppeteerArgs = @("-p", $PuppeteerConfig)
} else {
    Write-Host "No encuentro ..\puppeteer-config.json. Intento usar Puppeteer por defecto." -ForegroundColor Yellow
    $PuppeteerArgs = @()
}

$diagrams = @(
    @{In="images\uml\impl_backend_flujo_python.mmd"; Out="images\uml\impl_backend_flujo_python.pdf"; W="1400"; H="950"},
    @{In="images\uml\impl_backend_buffer_ventana.mmd"; Out="images\uml\impl_backend_buffer_ventana.pdf"; W="1400"; H="950"},
    @{In="images\uml\impl_backend_features_quality.mmd"; Out="images\uml\impl_backend_features_quality.pdf"; W="1400"; H="850"},
    @{In="images\uml\impl_backend_runtime_states.mmd"; Out="images\uml\impl_backend_runtime_states.pdf"; W="1300"; H="950"},
    @{In="images\uml\impl_sonificacion_flujo.mmd"; Out="images\uml\impl_sonificacion_flujo.pdf"; W="1600"; H="900"},
    @{In="images\uml\impl_sonificacion_controles.mmd"; Out="images\uml\impl_sonificacion_controles.pdf"; W="1500"; H="1050"},
    @{In="images\uml\impl_sonificacion_quality_gate.mmd"; Out="images\uml\impl_sonificacion_quality_gate.pdf"; W="1500"; H="1050"},
    @{In="images\uml\impl_sonificacion_segmento_compas_nota.mmd"; Out="images\uml\impl_sonificacion_segmento_compas_nota.pdf"; W="1600"; H="950"},
    @{In="images\uml\impl_midi_eventos_bytes.mmd"; Out="images\uml\impl_midi_eventos_bytes.pdf"; W="1600"; H="900"}
)

foreach ($d in $diagrams) {
    if (-not (Test-Path $d.In)) { throw "No existe $($d.In)" }
    Write-Host "Generando $($d.Out)..."
    npx -y @mermaid-js/mermaid-cli @PuppeteerArgs -b white -w $d.W -H $d.H -i $d.In -o $d.Out
}

Write-Host "PDF generados:" -ForegroundColor Green
Get-ChildItem images\uml\impl_*.pdf | Select-Object Name,Length,LastWriteTime
