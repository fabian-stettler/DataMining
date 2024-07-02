#!/bin/bash

userCredentialsUserName="xYBtezT88DRLsFzzA6r3AJa4"
userCredentialsPassword="cAKw8nCh7XfzAn5J4jCtGSZc"
staticPossibleIPAdresses=("de-ber.prod.surfshark.com_tcp.ovpn" "de-ber.prod.surfshark.com_udp.ovpn" "de-fra.prod.surfshark.com_tcp.ovpn"
"de-fra.prod.surfshark.com_udp.ovpn" "fr-par.prod.surfshark.com_tcp.ovpn" "fr-par.prod.surfshark.com_udp.ovpn" "uk-edi.prod.surfshark.com_tcp.ovpn"
"uk-edi.prod.surfshark.com_udp.ovpn" "uk-gla.prod.surfshark.com_tcp.ovpn" "uk-gla.prod.surfshark.com_udp.ovpn")
# Get the current date in days since the epoch
rotatingNumber=$((($(date +%s) / 86400)))
currentVpnConnectionNumber=$((rotatingNumber % 10))

currentVpnConnection="${staticPossibleIPAdresses[currentVpnConnectionNumber]}"
initialCommandVpnConnection="sudo openvpn --config /etc/openvpn/$currentVpnConnection --auth-user-pass /home/supremeleader/Documents/DataMiningProjekt/userpass.txt --dev tun0"

# Create a file with the username and password
echo -e "$userCredentialsUserName\n$userCredentialsPassword" > /home/supremeleader/Documents/DataMiningProjekt/userpass.txt

# Run the OpenVPN command in the background
(cd /etc/openvpn/; $initialCommandVpnConnection &)

# Wait for the OpenVPN connection to be established
sleep 10
