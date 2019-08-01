from setuptools import setup, find_packages

with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()

setup(name='py_adobeio_api',
      version='0.41',
      description='Python API wrapper for Adobe IO.  Made for portability.',
      url='https://github.com/MattJermyWright/adobeio-python-general-api',
      author='Matt Wright',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='matthew.jeremy.wright@gmail.com',
      license='GPLv3.0',
      install_requires=["jwt", "loguru", "requests"],
      packages=find_packages(),
      classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent",
      ],
      zip_safe=False)
