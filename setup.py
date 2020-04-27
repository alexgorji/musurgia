import setuptools

setuptools.setup(
    name="musurgia",
    version="1.10.11",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="tools for algorithmic composition",
    url="https://github.com/alexgorji/musurgia.git",
    packages=setuptools.find_packages(),
    install_requires=['quicktions',
                      'prettytable',
                      'fpdf2',
                      'diff-pdf-visually'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
