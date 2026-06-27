"""Utilities for discovering block devices with lsblk."""

import json
import subprocess

LSBLK_COMMAND = ('lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT')


def run_command(command):
    """Run the supported lsblk command and return its output."""
    if tuple(command) != LSBLK_COMMAND:
        raise ValueError('Unsupported command')
    return subprocess.check_output(command)

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
    output = run_command(LSBLK_COMMAND)
    devices = json.loads(output)['blockdevices']
    for parent in devices:
        if parent['name'] == device:
            return parent
        for child in parent.get('children', []):
            if child['name'] == device:
                return child
    return None
