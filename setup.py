from setuptools import setup, find_packages
from pathlib import Path

with open('README.md') as f:
    long_description = f.read()

setup(
    name='mir-asap',
    version='0.0.2',
    author='Paul Maevskikh',
    author_email='arquolo@gmail.com',
    description='Wrapper for ASAP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['**/*.so', '**/*.dll', '**/*.pyd']
    },
    python_requires='>=3.6,<3.7',
    install_requires=[
        'dataclasses',
        'numpy>=1.15',
        'opencv-python>=4.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
)
