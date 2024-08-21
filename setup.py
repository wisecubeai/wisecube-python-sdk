import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="wisecube",
    version="1.0.0",
    author="Wisecube",
    author_email="info@wisecube.ai",
    description="Wisecube SDK for graph Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wisecubeai/wisecube-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    extras_require={
        "pandas": ["pandas==1.5.3"],
    }
)