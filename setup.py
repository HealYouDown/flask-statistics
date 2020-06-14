import setuptools


with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="flask-statistics",
    version="1.0.1",
    author="HealYouDown",
    description="Package to collect statistics in Flask.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/HealYouDown/flask-statistics",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "flask", "flask-sqlalchemy"
    ]
)
