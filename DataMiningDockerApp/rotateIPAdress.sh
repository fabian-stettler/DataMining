#!/bin/bash

# Benutzeranmeldedaten
userCredentialsUserName="xYBtezT88DRLsFzzA6r3AJa4"
userCredentialsPassword="cAKw8nCh7XfzAn5J4jCtGSZc"

# Liste der möglichen IP-Adressen
staticPossibleIPAdresses=(
    "de-ber.prod.surfshark.com_tcp.ovpn"
    "de-ber.prod.surfshark.com_udp.ovpn"
    "de-fra.prod.surfshark.com_tcp.ovpn"
    "de-fra.prod.surfshark.com_udp.ovpn"
    "fr-par.prod.surfshark.com_tcp.ovpn"
    "fr-par.prod.surfshark.com_udp.ovpn"
    "uk-edi.prod.surfshark.com_tcp.ovpn"
    "uk-edi.prod.surfshark.com_udp.ovpn"
    "uk-gla.prod.surfshark.com_tcp.ovpn"
    "uk-gla.prod.surfshark.com_udp.ovpn"
)

# Überprüfen und Installieren von OpenVPN
if ! command -v openvpn &> /dev/null
then
    echo "OpenVPN wird installiert..."
    sudo apt update
    sudo apt install openvpn -y
fi

# Erstellen des Verzeichnisses /etc/openvpn, falls es nicht existiert
if [ ! -d /etc/openvpn ]; then
    sudo mkdir -p /etc/openvpn
fi

# Ermittlung der aktuellen Rotationsnummer (Tage seit der Epoche)
rotatingNumber=$((($(date +%s) / 86400)))
currentVpnConnectionNumber=$((rotatingNumber % ${#staticPossibleIPAdresses[@]}))

# Auswahl der aktuellen VPN-Verbindung
currentVpnConnection="${staticPossibleIPAdresses[currentVpnConnectionNumber]}"
initialCommandVpnConnection="sudo openvpn --config /etc/openvpn/$currentVpnConnection --auth-user-pass /home/pi/openvpn/userpass.txt --dev tun0"

# Erstellung einer Datei mit den Benutzerdaten
echo -e "$userCredentialsUserName\n$userCredentialsPassword" > /home/pi/openvpn/userpass.txt

# Starten der OpenVPN-Verbindung im Hintergrund
(cd /etc/openvpn/ && $initialCommandVpnConnection &)

# Warten auf die Herstellung der OpenVPN-Verbindung
sleep 10
