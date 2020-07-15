from setuptools import setup

setup(
    name="DMM Keysight",
    version="2020.07.15",
    description="Package which can be used to control Keysight dmm using Visa toolkit",
    author="Dawid Oberda",
    author_email="dawidoberda@gmail.com",
    py_modules=['dmm_test'],
    entry_points={
        'console_scripts': [
            'dmm_test = dmm_test:test'
        ]
    }
)