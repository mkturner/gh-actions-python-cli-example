"""Utilities for discovering block devices with lsblk."""

import json
import subprocess

LSBLK_COMMAND = ('lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT')
LSBLK_TIMEOUT_SECONDS = 10


def run_command(command):
    """Run the supported lsblk command and return its output.

    :param command: Tuple of command arguments to execute.
    :return: Command output as bytes.
    :raises ValueError: If a command other than the supported lsblk call is requested.
    """
    if tuple(command) != LSBLK_COMMAND:
        raise ValueError(f'Only the lsblk JSON command is supported, got: {command}')
    try:
        return subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            timeout=LSBLK_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as error:
        message = error.output.decode('utf-8', errors='replace').strip()
        raise RuntimeError(
            f'lsblk command failed with exit code {error.returncode}: {message}'
        ) from error


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

    :param device: The block device name to look up.
    :return: The matching device dictionary, or None when not found.
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
