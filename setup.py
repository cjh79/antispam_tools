from setuptools import setup, find_packages

setup(
    name='antispam',
    version='1.0',
    url='https://github.com/cjh79/antispam',
    description='Anti-spam forms for Unleashed LLC.',
    keywords=[],

    long_description='',

    author='Christopher Hawes',
    author_email='chrishawes@gmail.com',
    maintainer='Christopher Hawes',
    maintainer_email='chrishawes@gmail.com',

    install_requires=[
        'django',
        # NOTE: this does not seem to work. It seems to still be installing the pypi version of django-antispam, which
        # has a bug (converts a datetime to an int, which breaks tests).
        'django-antispam @ git+https://github.com/mixkorshun/django-antispam@ad9ffbc8950f41f71efb3501bc545a588c8991a4#egg=django_antispam',
    ],
    tests_require=[
        'factory_boy',
        'vcrpy',
        'mock',
    ],

    packages=find_packages(exclude=['tests.*', 'tests']),

    test_suite = "runtests.runtests",

    classifiers=[],
)
