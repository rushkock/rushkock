from setuptools import setup,find_packages

setup(
    name='OOP_CV',
    version='0.0.1',    
    description='An overdone installable package that displays my CV',
    url='https://github.com/rushkock/rushkock',
    author='Ruchella Kock',
    license='BSD 2-clause',
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[ 'rushkock @ git+ssh://git@github.com:rushkock/rushkock.git'
        'getContinent','numpy','pandas','circlify', 'plotly','fastapi','kaleido','marimo','plotly','pycountry','pycountry-convert','python-dateutil','squarify','wordcloud','markdownify'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Recruiters',
        'License :: BSD License',  
        'Operating System :: POSIX :: Linux'
    ],
)