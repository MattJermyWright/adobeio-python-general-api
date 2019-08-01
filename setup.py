from setuptools import setup, find_packages

setup(name='py_adobeio_api',
      version='0.2',
      description='Python API wrapper for Adobe IO.  Made for portability.',
      url='https://github.com/MattJermyWright/adobeio-python-general-api',
      author='Matt Wright',
      author_email='matthew.jeremy.wright@gmail.com',
      license='GPLv3.0',
      install_requires=["jwt", "loguru", "requests"],
      packages=find_packages(),
      classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
      zip_safe=False)
