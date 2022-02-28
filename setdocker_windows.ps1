#ps1
# Enable needed Windows features
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart
# Say no to reboot
Enable-WindowsOptionalFeature -Online -FeatureName Containers -All -NoRestart
# Say no to reboot

# Install Docker Enterprise
Install-Module DockerMsftProvider -Force
Install-Package Docker -ProviderName DockerMsftProvider -Force -RequiredVersion 19.03

# Open Needed Firewall ports
netsh advfirewall firewall add rule name=`"docker`_rancher`_in`_tcp`" dir=in action=allow protocol=tcp localport=80,443,2376,9099,10250,10254,30000-32767
netsh advfirewall firewall add rule name=`"docker`_rancher`_out`_tcp`" dir=out action=allow protocol=tcp localport=80,443,2376,9099,10250,10254,30000-32767
# Note 4789 is for VXLAN
netsh advfirewall firewall add rule name=`"docker`_rancher`_in`_udp`" dir=in action=allow protocol=tcp localport=4789,8472,30000-32767
netsh advfirewall firewall add rule name=`"docker`_rancher`_out`_udp`" dir=out action=allow protocol=tcp localport=4789,8472,30000-32767

#reboot
echo "You must now reboot. Run Restart-Computer"
Restart-Computer


# Install-WindowsFeature -Name Containers
# Install-PackageProvider -Name NuGet -Force
# Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
# Install-Package -Name docker -ProviderName DockerMsftProvider -Force -RequiredVersion 19.03

