from distutils.core import setup

setup(
    name='python-indexed-collation',
    version='1.0.0dev',
    packages=['indexed_collation',],
    license='MIT',
    description='Python package that provide localized indexed collations.',
    long_description=open('README.md').read(),
    install_requires=[
        'PyICU==1.8',
    ],
)