from setuptools import setup, find_packages

setup(
    name='telco_llm',
    version='1.0.0',
    author='Tan Chia Yan',
    author_email='chiayan@waulabs.com',
    description='A package for generating SQL queries for Telecommunication RF Domain Expert',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add any dependencies your package requires
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)