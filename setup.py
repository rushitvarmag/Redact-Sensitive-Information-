from setuptools import setup, find_packages

setup(
	name='cise6930fa24-project1',
	version='1.0',
	author='RushitVarmaGadiraju',
	authour_email='vgadiraju@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)