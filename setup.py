from setuptools import find_packages, setup
from typing import List 

def get_requirements()->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            ##read lines from the file
            lines= file.readlines()
            ##process each line
            for line in lines:
                requirement=line.strip()

                ##ignore empty lines amd -e .
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print("Error: requirements.txt file not found.")

    return requirements

### Setup metadata

setup(
    name="DataScience Project2",
    version="0.0.1",
    author="Saikrishna",
    author_email="saikiven03@gmail.com",
    packages=find_packages(), ###to know the packages available
    install_requires=get_requirements(),
)