import sys
from pathlib import Path

import setuptools


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(self):
        return True


platform = ''
for key, platform in {'--windows': 'win_amd64',
                      '--linux': 'manylinux1_x86_64'}.items():
    if key in sys.argv[1:]:
        sys.argv.remove(key)
        sys.argv += ['-p', platform]
        break
else:
    if 'bdist' in sys.argv[1:]:
        raise ValueError(f'specify either --windows or --linux')


setuptools.setup(
    name='mir-asap',
    version='0.1',
    url='https://github.com/arquolo/gigaslide-bin',
    author='Paul Maevskikh',
    author_email='arquolo@gmail.com',
    description='Wrapper for ASAP',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    package_data={
        '': ['**/*.dll', '**/*.pyd'] if 'win' in platform else ['**/*.so'],
    },
    python_requires='>=3.6, <3.7',
    install_requires=[
        'dataclasses',
        'numpy>=1.15',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    distclass=BinaryDistribution,
)
