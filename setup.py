"""Setup of brymen bm257s serial interface library"""

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="bm257s",
    version="0.1",
    author="Robert Wilbrandt",
    author_email="robert@stamm-wilbrandt.de",
    description="Small python library to interface with brymen bm257s multimeters",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=["scripts/bm257s-console"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
)
