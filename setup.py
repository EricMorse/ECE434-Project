import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="BBIOPY",
	version="0.1.4",
	author="Eric Morse, Joshua Key, and Mark Yoder",
	author_email="morsee@rose-hulman.edu",
	description="Full python implementation of BBIO gpiod",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/EricMorse/ECE434-Project",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
