#!/usr/bin/env python3

import sys

# try to add a known host to settings.py
try:
    new_known_host = sys.argv[1]
    with open("connectedhealth/settings.py") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("ALLOWED_HOSTS ="):
            existing_ips = [ip.strip("'") for ip in line.strip("]\n").split("[")[1].split(", ")]
            if new_known_host not in existing_ips:
                # add new known host if it is not already listed
                existing_ips.append(new_known_host)
                lines[i] = f"ALLOWED_HOSTS = {existing_ips}\n"
            else:
                exit(0)
            break
    with open("connectedhealth/settings.py", 'w') as f:
        f.writelines(lines)
except:
    exit(1)
