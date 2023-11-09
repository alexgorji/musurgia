import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.rst").read_text()
setuptools.setup(
    name="musurgia",
    version="1.0beta",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="Tools for algorithmic composition.",
    url="https://github.com/alexgorji/musurgia.git",
    packages=setuptools.find_packages(),
    install_requires=['musicscore'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True
)
