from setuptools import setup, find_packages


setup(
    name='pcdl',
    url='https://github.com/bwhmather/pcdl',
    version='0.0.1',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='GPLv3',
    description=(
        "Tools for designing pneumatic integrated circuits"
    ),
    long_description=__doc__,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=[
        'Pillow',
        'toml',
    ],
    packages=find_packages(),
    package_data={
        '': ['*.*'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
    test_suite='pcdl.tests.suite',
)
