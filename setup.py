from setuptools import find_packages, setup

setup(
    name='namespace-pre-commit',
    description='Check for Kubernetes manifest without namespace',
    url='https://github.com/containeroo/namespace-pre-commit',
    version='0.0.1',

    author='containeroo',
    author_email='hello@containeroo.ch',

    platforms='linux',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'namespaced = hooks.namespaced:main',
        ],
    },
)