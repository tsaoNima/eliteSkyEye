#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = "SkyEye",
	version = "0.1",
	packages = find_packages(),
	include_package_data = True,
	description = "Placeholder text for description.",
	url = "none",
	author = "Tsao Nima",
	author_email = "none@none.none",
	license = "MIT Who Cares License",
	long_description = open("readme.txt").read(), 
	scripts = ["SkyEye/skyEye.py", "SkyEye/testAll.py", "SkyEye/setupTables.py"],
	install_requires = ["psycopg2", "enum34", "colorama", "pytz", "keyring", "pypiwin32"],
	zip_safe = False
	)