from setuptools import setup, find_packages
import pkg_resources
import pathlib

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='ruchella_resume',
    version='0.0.1',    
    description='An overdone installable package that displays my CV',
    url='https://github.com/rushkock/rushkock',
    author='Ruchella Kock',
    license='BSD 2-clause',
    python_requires=">=3.10",
    packages=['rushkock'],
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Recruiters',
        'License :: BSD License',  
        'Operating System :: POSIX :: Linux'
    ],
)