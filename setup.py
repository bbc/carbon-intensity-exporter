import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbon-intensity-exporter",
    version="0.0.1",
    author="Iain McClenaghan",
    author_email="iain.mcclenaghan@bbc.co.uk",
    description="A prometheus exporter for the carbon intensity api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bbc/rd-carbon-intensity-exporter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    python_requires=">=3.6"
)
