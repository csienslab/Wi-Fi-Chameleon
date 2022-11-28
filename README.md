# Wi-Fi Chameleon

Captive Portal attack and Captive Portal Browser measurement tool suite.

## Install
Python3 (version >=3.6) is required for this project.

Installation script:
```bash
mkvirtualenv wifi-chameleon
git clone https://git.nslab.csie.ntu.edu.tw/joeywang4/wifi-chameleon-tool
cd wifi-chameleon-tool
sudo pip install .
```

For development:
```bash
mkvirtualenv wifi-chameleon
git clone https://git.nslab.csie.ntu.edu.tw/joeywang4/wifi-chameleon-tool
cd wifi-chameleon-tool
sudo pip install -e .
```

If something went wrong, please check the configuration files located in `conf` directory is properly installed.

## Test Portal
To create a test portal:
```bash
cd src
sudo python3 main.py http_portal
```

To cleanup this portal:
```bash
cd src
sudo python3 main.py cleanup
```

To set static portal files:
Put the portal files to `portals/<portal name>` and use
```bash
sudo python3 src/main.py set_portal <portal name>
```

To set portal to a given URL
```bash
sudo python3 src/main.py set_portal <URL>
```

## Testing
*\*Under development\**

`pytest` is required for testing. 
```bash
pip install pytest
# Under the root directory of this project
pytest
```
