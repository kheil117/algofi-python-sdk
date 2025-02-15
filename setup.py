import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="algofi-python-sdk",
    description="Official Algofi Protocol Python SDK",
    author="Algofi",
    author_email="founders@algofi.org",
    version="2.1.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source": "https://github.com/Algofiorg/algofi-python-sdk",
    },
    install_requires=["py-algorand-sdk >= 1.6.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
)
