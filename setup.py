from setuptools import setup, find_packages
from typing import List
def get_requirements(file_path: str) -> List[str]:
    """This function will return the list of requirements"""
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
        if '-e .' in requirements:
            requirements.remove('-e .')
    
    return requirements

setup(
    name="your_package_name",
    version="0.1",
    author="Sathyaraj Medipalli",
    author_email="sathyarajmedipalli6@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)