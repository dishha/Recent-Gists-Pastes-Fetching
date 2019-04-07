"""Setuptools script."""

from setuptools import setup, find_packages


setup(
    name='tfw_myworker',
    version='1.0',
    description='CHANGEME: worker short description',
    long_description="CHANGEME: Worker long description",
    classifiers=[
        "Programming Language :: Python"
    ],
    author='your name here',
    author_email='your_email@here.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tfw_myworker',
    install_requires=[]
)
