"""Utilities for discovering block devices with lsblk."""

import json
import shlex
import subprocess

def run_command(command):
    """Run a trusted shell command string and return its output."""
    cmd = shlex.split(command)
    output = subprocess.check_output(cmd)
    return output

def run_lsblk(device):
    """
    Runs lsblk command and produces JSON output:

    lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT
    {
    "blockdevices": [
        {"name": "vda", "size": "59.6G", "type": "disk", "mountpoint": null,
            "children": [
                {"name": "vda1", "size": "59.6G", "type": "part", "mountpoint": "/etc/hosts"}
            ]
        }
    ]
    }
    """
    command = 'lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT'
    output = run_command(command)
    devices = json.loads(output)['blockdevices']
    for parent in devices:
        if parent['name'] == device:
            return parent
        for child in parent.get('children', []):
            if child['name'] == device:
                return child
    return None
