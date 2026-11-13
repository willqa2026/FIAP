# Exporta a apresentação .pptx para PDF usando o PowerPoint instalado.
# Uso: powershell -ExecutionPolicy Bypass -File exportar_pdf.ps1
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$pptx = Join-Path $base "GS_CuidaMais_RM576183.pptx"
$pdf  = Join-Path $base "GS_CuidaMais_RM576183.pdf"

$app = New-Object -ComObject PowerPoint.Application
try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $pres = $app.Presentations.Open($pptx, $true, $false, $false)
    $pres.SaveAs($pdf, 32)   # 32 = ppSaveAsPDF
    $pres.Close()
    Write-Output "PDF gerado: $pdf"
}
finally {
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
