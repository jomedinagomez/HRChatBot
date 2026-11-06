# Changes a worker's role in the mock Workday, on the fly. Defaults to you.
#
#   .\mock_workday\set-role.ps1 manager
#   .\mock_workday\set-role.ps1 employee -User <user principal name or service principal client ID>
#   .\mock_workday\set-role.ps1 manager -Url http://localhost:7071/api/workers/me   # local mock
#
# Authenticates with your az sign-in; changing roles needs the Workers.Admin app role,
# which Terraform (infra/) gives the person who deployed it.
# Copilot Studio asks Workday on every question, so a change shows on the next one.
param(
    [Parameter(Mandatory)][ValidateSet("manager", "employee")][string]$Role,
    [string]$User,
    [string]$Url
)

$cfg = @{}
foreach ($line in Get-Content (Join-Path (Split-Path $PSScriptRoot -Parent) ".env")) {
    if ($line -match '^\s*([A-Z_]+)\s*=\s*(.*?)\s*$') { $cfg[$Matches[1]] = $Matches[2].Trim('"') }
}
if (-not $Url) { $Url = $cfg.WORKDAY_MOCK_URL }
# Whoever az is signed in as: your user principal name, or a service principal's client ID.
if (-not $User) { $User = az account show --query user.name -o tsv }
$token = az account get-access-token --resource "api://$($cfg.WORKDAY_API_APP_ID)" --query accessToken -o tsv

$target = "$($Url -replace '/me$', '')/$([uri]::EscapeDataString($User.ToLower()))"
$body = @{ isManager = ($Role -eq "manager") } | ConvertTo-Json
$worker = Invoke-RestMethod $target -Method Put -Body $body -ContentType "application/json" `
    -Headers @{ Authorization = "Bearer $token" }
Write-Host "$($worker.descriptor) is now $(if ($worker.isManager) { 'a manager' } else { 'an employee' }) in mock Workday."
