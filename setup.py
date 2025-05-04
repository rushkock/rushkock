from setuptools import setup, find_packages
import pip 

links = []
requires = []

try:
    requirements = pip.req.parse_requirements('requirements.txt')
except:
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        'requirements.txt', session=pip.download.PipSession())

for item in requirements:
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None): # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

setup(
    name='ruchella_resume',
    version='0.0.1',    
    description='An overdone installable package that displays my CV',
    url='https://github.com/rushkock/rushkock',
    author='Ruchella Kock',
    license='BSD 2-clause',
    python_requires=">=3.10",
    packages=['rushkock'],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Recruiters',
        'License :: BSD License',  
        'Operating System :: POSIX :: Linux'
    ],
)