from setuptools import find_packages, setup

setup(
    name='pre-commit-hooks',
    description='',
    url='Some out-of-the-box hooks for pre-commit',
    version='v0.0.12',

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
            'forbidden_pattern = hooks.forbidden_pattern:main'
        ],
    },
    install_requires = [
        "pyyaml"
    ]
)