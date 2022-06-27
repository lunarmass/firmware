# Lunar Mass Device Firmware

Device firmware repository
Directory structure:
lunarmass
+---firmware
| fwcheck.py
| fwdb.json
| README.md
| +---fw
| <linkedfw.bin>
| +---unlinkedfw
| <unlinkedfw.bin>
| <unlinkedfw.info>

Please only use firmware check-in script (fwcheck.py) to manage fwdb.json. DO NOT HAND EDIT!
fwcheck.py usage:
○ fwcheck.py --checkinlink| -c <fwfile.bin>
○ fwcheck.py --unlink | -u <fwfile.bin>
○ fwcheck.py --removeunlinked | -ru <filter or file name> (qualifies each unlinked firmware file before removing)
○ fwcheck.py --list | -l (can grep this list to filter on things)
○ fwcheck.py --listunlinked | -lu (can grep this list to filter on things)
