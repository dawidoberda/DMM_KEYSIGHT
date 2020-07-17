from setuptools import setup
#trzeba to zainstalowac pip install --editable .
#TODO: dodac kolejne pomiary do measurement_tool
#TODO: dodac wymagania do stup() wszystkie pakiey ktore sa zainstalowane.
#TODO: dodac do entry_points measurement_tool
setup(
    name="DMM Keysight",
    version="2020.07.15",
    description="Package which can be used to control Keysight dmm using Visa toolkit",
    author="Dawid Oberda",
    author_email="dawidoberda@gmail.com",
    py_modules=['dmm_test', 'measurement_tool'],
    entry_points={
        'console_scripts': [
            'dmm_test=dmm_test:test'
        ]
    },
)