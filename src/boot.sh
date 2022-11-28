sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv4.conf.all.route_localnet=1
iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
wpa_cli -i wlan0 disc
python3 /home/pi/WiFi-Chameleon/src/checker.py
