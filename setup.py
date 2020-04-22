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
        'django-antispam',
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