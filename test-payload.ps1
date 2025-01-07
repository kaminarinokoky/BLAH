# Set DNS
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("78.157.42.100", "78.157.42.101")

# Install SSH
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Install FTP
Install-WindowsFeature -Name Web-FTP-Server -IncludeManagementTools
Start-Service ftpsvc
Set-Service -Name ftpsvc -StartupType Automatic
