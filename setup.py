import setuptools
from setuptools import find_packages

_name = "data_etl_full_app"
_repo_name = "etl_full_app"
_license = 'Proprietary: Taxfix internal use only'
_description = "Persons data ETL and Web application"

setuptools.setup(
    name=_name,
    version='1.0.0',
    description=_description,
    license=_license,
    # url=f'https://github.com/{org.name}/{_repo_name}.git',
    author='Nour Samir',
    author_email='',
    python_requires='>=3.7',

    classifiers=[
        'Development Status :: Alpha',
        'Environment :: cli',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],

    packages=find_packages(exclude=['tests']),

    install_requires=[
        "Flask",
        "SQLAlchemy"
    ],

    test_suite='unittest.TestCase',
    include_package_data=True,

    entry_points={
        'console_scripts': [
            "run_persons_data_etl = persons_data_etl.main:main",
            "run_app_service = app_service.main:main",
        ],
    },
)