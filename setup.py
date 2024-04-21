from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.4.3'
DESCRIPTION = 'Discrete Function HUB'
LONG_DESCRIPTION = 'HUB that adds higher-level functionalities to discrete functions created from scratch.'

# Setting up
setup(
    name="discrete_function",
    version=VERSION,
    author=["Ian dos Anjos"],
    author_email="<iannaianjos@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['matplotlib', 'scipy', 'line_profiler'],
    keywords=['python', 'discrete_function', 'hub_discrete_function'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
