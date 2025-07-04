from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="euil",
    version="0.1.0",
    author="IronBill25",
    author_email="(not provided)",
    description="Extensible UI Language - A simple XML-based UI library for making apps with Tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IronBill25/euil",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        'tk',
    ],
    entry_points={
        'console_scripts': [
            'euil=euil.main:cli_main',
        ],
    },
)
