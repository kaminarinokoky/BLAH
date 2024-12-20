@echo off

:: Set DNS
netsh interface ip set dns "Ethernet" static 78.157.42.100
netsh interface ip add dns "Ethernet" 78.157.42.101 index=2

:: Install SSH
powershell -Command "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0"
powershell -Command "Start-Service sshd"
powershell -Command "Set-Service -Name sshd -StartupType 'Automatic'"

:: Install FTP
powershell -Command "Install-WindowsFeature -Name Web-FTP-Server -IncludeManagementTools"
powershell -Command "Start-Service ftpsvc"
powershell -Command "Set-Service -Name ftpsvc -StartupType 'Automatic'"
