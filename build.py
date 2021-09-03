#!/usr/bin/env python3

import subprocess
import urllib.request

from pathlib import Path


def download_files():
    reqs_path = Path('requirements')
    if reqs_path.exists():
        for file in reqs_path.glob('*.txt'):
            file.unlink()

    reqs_path.mkdir(exist_ok=True)

    files = {
        'requirements.txt': [
            'https://raw.githubusercontent.com/ansible/ansible-builder/e8fff0692a9ed18b3bec073ab672d1dd6aa2f587/requirements.txt',
            'https://raw.githubusercontent.com/ansible/ansible-builder/e8fff0692a9ed18b3bec073ab672d1dd6aa2f587/test/requirements.txt',
        ],
        'constraints.txt': [
            'https://raw.githubusercontent.com/ansible/ansible-builder/e8fff0692a9ed18b3bec073ab672d1dd6aa2f587/test/constraints.txt',
        ]
    }

    for filename, urls in files.items():
        for url in urls:
            with urllib.request.urlopen(url) as resp:
                with open(reqs_path / filename, 'ab') as f:
                    f.write(resp.read())


def build_image(tag, path, containerfile='Containerfile'):
    cmd = [
        'docker',
        'build',
        '--tag', tag,
        '--file', containerfile,
        path,
    ]
    subprocess.run(cmd)


def main():
    download_files()
    build_image('quay.io/ansible/ansible-builder-test-container', Path('.').absolute())


if __name__ == '__main__':
    main()
