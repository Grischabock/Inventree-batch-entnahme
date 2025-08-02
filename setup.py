from setuptools import setup, find_packages

setup(
    name="inventree-batch-entnahme",
    version="1.0.0",
    author="GrischaMedia",
    author_email="info@grischamedia.ch",
    description="Inventree Plugin für Batch-Entnahme: Mehrere Barcodes scannen und gesammelt ausbuchen.",
    long_description="Ein Inventree-Plugin, das eine Maske für das Scannen mehrerer Barcodes bietet. Die gescannten Artikel können anschließend gesammelt aus dem Lager ausgebucht werden.",
    long_description_content_type="text/markdown",
    url="https://github.com/Grischabock/Inventree-batch-entnahme",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
