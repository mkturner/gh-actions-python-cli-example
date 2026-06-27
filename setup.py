"""Package configuration for blkpy-demo."""

from setuptools import find_packages, setup

# read the requirements.txt file and use it to install dependencies
with open('requirements.txt', encoding='utf-8') as f:
    install_requires = f.read().splitlines()


setup(
    name='blkpy-demo',
    description='demo python CLI tool to list block devices',
    packages=find_packages(),
    author='Alfredo Deza',
    entry_points="""
    [console_scripts]
    blkpy=blkpy.main:main
    """,
    # install_requires=['click==7.1.2'],
    install_requires=install_requires,
    version='0.0.1',
    url='https://github.com/alfredodeza/python-cli-example',
)
