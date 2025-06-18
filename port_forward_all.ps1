$services = @(
    @{Name="webapp";      LocalPort=3000; Service="svc/ai-webapp";                              TargetPort=80;   Namespace=""},
    @{Name="prometheus";  LocalPort=9090; Service="svc/prometheus-kube-prometheus-prometheus";  TargetPort=9090; Namespace="monitoring"},
    @{Name="pushgateway"; LocalPort=9091; Service="svc/pushgateway";                            TargetPort=9091; Namespace="monitoring"},
    @{Name="grafana";     LocalPort=5000; Service="svc/prometheus-grafana";                     TargetPort=80;   Namespace="monitoring"}
)

Write-Host "🚀 Starting all port-forwards (including Grafana)..."
$jobs = @()

foreach ($svc in $services) {
    $jobScript = {
        param($svc)
        while ($true) {
            try {
                $cmd = "kubectl port-forward $($svc.Service) $($svc.LocalPort):$($svc.TargetPort)"
                if ($svc.Namespace) { $cmd += " -n $($svc.Namespace)" }
                Write-Host "[$($svc.Name)] Running: $cmd"
                Invoke-Expression $cmd
            }
            catch {
                Write-Host "[$($svc.Name)] Error: $_ - Retrying in 5 seconds..." -ForegroundColor Red
                Start-Sleep -Seconds 5
            }
        }
    }
    $job = Start-Job -ScriptBlock $jobScript -ArgumentList $svc -Name $svc.Name
    $jobs += $job
}

Write-Host "`n✅ All services forwarded:" -ForegroundColor Green
Write-Host "WebApp:      http://localhost:3000"
Write-Host "Prometheus:  http://localhost:9090"
Write-Host "Pushgateway: http://localhost:9091"
Write-Host "Grafana:     http://localhost:5000"
Write-Host "`nPress ENTER to stop all..." -ForegroundColor Yellow
Read-Host

# Cleanup
Write-Host "`n🛑 Stopping all port-forwards..."
$jobs | Stop-Job -PassThru | Remove-Job
Write-Host "Done." -ForegroundColor Green