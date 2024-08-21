# setup.py

import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'chat', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        msg = 'Cannot find version in chat/__init__.py'
        raise RuntimeError(msg)


install_requires = ['aiohttp>=3.6',
                    'aiohttp_jinja2',
                    'faker']


setup(name='chat',
      version=read_version(),
      description='API News APP ON AIOHTTP',
      platforms=['POSIX'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
