#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = "skyeye",
	version = "0.1",
	packages = find_packages(),
	include_package_data = True,
	description = "Strategic analyzer and general map system.",
	url = "none",
	author = "TsaoNima",
	author_email = "none@none.none",
	license = "MIT Who Cares License",
	long_description = open("readme.txt").read(), 
	scripts = ["SkyEye/skyEye.py", "SkyEye/testAll.py"],
	install_requires = ["enum34", "servbase"],
	zip_safe = False
	)