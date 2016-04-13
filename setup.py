from setuptools import setup

setup(name='geocity',
      version='0.1',
      description='offline geo city data',
      package_data={'': ['cities.txt']},
      include_package_data=True,
      url='https://github.com/royi1000/pycity',
      author='Royi Reshef',
      author_email='roy.myapp@gmail.com',
      license='MIT',
      packages=['geocity'],
      zip_safe=False)
