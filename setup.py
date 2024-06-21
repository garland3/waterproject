from setuptools import setup, find_packages

setup(
    name="waterproject",
    version="0.1",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        # Add your dependencies here
        # e.g. 'requests', 'numpy'
    ],
    entry_points={
        'console_scripts': [
            # Add console script entry points here if needed
            # e.g. 'mycommand=my_module:main_function'
        ],
    },
)
