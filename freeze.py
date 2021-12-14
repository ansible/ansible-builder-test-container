#!/usr/bin/env python
"""Freeze container requirements for use with a final container build."""

from __future__ import annotations

import argparse
import pathlib
import subprocess


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('container', nargs='?', default='ansible-builder-freezer')

    args = parser.parse_args()
    container = args.container

    print("Building a container to freeze the requirements.")
    subprocess.run(['docker', 'build', '-t', container, '-f', 'Containerfile', '.'], check=True)
    container_id = subprocess.run(['docker', 'run', '--rm', '--tty', '--detach', container], check=True, capture_output=True, text=True).stdout.rstrip()

    print('Freezing requirements')
    subprocess.run(['docker', 'cp', 'requirements/requirements.in', f'{container_id}:/tmp/requirements.in'], check=True)

    command = [
        'docker', 'exec', container_id,
        '/usr/bin/python', '-m', 'pip', 'install', '--upgrade', '--requirement', '/tmp/requirements.in', '--disable-pip-version-check',
    ]
    subprocess.run(command, check=True)

    command = [
        'docker', 'exec', container_id,
        '/usr/bin/python', '-m', 'pip.__main__', 'freeze', '-qqq', '--disable-pip-version-check',
    ]
    freeze = subprocess.run(command, check=True, capture_output=True, text=True).stdout

    freeze_file = pathlib.Path('requirements/requirements.txt')
    freeze_file.write_text(freeze)

    subprocess.run(['docker', 'stop', container_id])

    print("Freezing completed.")


if __name__ == '__main__':
    main()
