import setuptools

requirements = [
    "Flask>=1.1.2",
    "dpkt>=1.9.2",
    "netifaces>=0.10.9",
    "requests>=2.21.0"
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wifichameleon",
    packages=setuptools.find_packages(),
    package_dir={'': 'src'},
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)