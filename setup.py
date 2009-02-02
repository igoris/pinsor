#!/usr/bin/env python

from setuptools import setup,find_packages

setup(
	name='pinsor',
	version='0.2.1',
	description='IoC container',
	author='Ryan Svihla',
	author_email='rssvihla@gmail.com',
	url='http://code.google.com/p/pinsor',
	download_url='http://code.google.com/p/pinsor/downloads/list',
	packages=find_packages('pinsor'),
	package_dir = {'':'pinsor'},
	
	long_description="""\
		pinsor is an IoC container with an emphasis on dependency resolution""",
	classifiers=[
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Operating System :: OS Independent"
	],
	keywords = "ioc, dependency injection",
	license="Apache License 2.0",
	install_requires=[
	'setuptools'
	],
	)
