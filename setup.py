from setuptools import setup

setup(
    name='power-logging',
    version='',
    packages=['power_logging'],
    url='AGPLv3',
    license='',
    author='andi',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'power-logging = power_logging:main',
        ]
    },
    install_requires=['influxdb', 'pyserial'],
)
