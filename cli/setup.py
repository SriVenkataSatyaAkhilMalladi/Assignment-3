from setuptools import setup

setup(
    name='goesNexrad',
    version='0.1.0',
    packages=['cli'],
    install_requires=[
        'typer',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        goesNexrad=cli.goesNexrad:app
    '''
)