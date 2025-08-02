from setuptools import setup, find_packages

setup(
     name="inventree-batch-entnahme",
     version="1.0.1",
     author="GrischaMedia",
     author_email="info@grischamedia.ch",
     description="Inventree Plugin für Batch-Entnahme",
     license="MIT",          # falls noch nicht drin
     url="https://github.com/Grischabock/Inventree-batch-entnahme",
     packages=find_packages(),
     install_requires=[],
     include_package_data=True,
     entry_points={
         "inventree_plugins": [
             "BatchEntnahmePlugin = inventree-batch-entnahme.plugin:BatchEntnahmePlugin"
         ]
     },
     package_data={
         "inventree_batch_entnahme": ["templates/*.html"]
     },
     classifiers=[
         "Programming Language :: Python :: 3",
         "Framework :: Django",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.7',
 )