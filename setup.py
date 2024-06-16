from setuptools import setup, find_packages

setup(
    name="gunstats",
    version="0.1.0",
    author="Manuel Lavin",
    author_email="mlavinv@uoc.edu",
    description="A package to analyze firearm statistics in the United States.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mlavinv117/gunstats",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "folium",
        "selenium"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
