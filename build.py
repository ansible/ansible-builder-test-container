#!/usr/bin/env python

import pathlib
import subprocess


def main():
    subprocess.run([
        'docker', 'build',
        '--tag', 'quay.io/ansible/ansible-builder-test-container',
        '--file', 'Containerfile',
        pathlib.Path('.').absolute(),
    ])


if __name__ == '__main__':
    main()
