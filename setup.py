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
        'django-antispam @ git+https://github.com/cjh79/django-antispam@a9026d30650e72323fd31384e9a40b9dc6eb4323#egg=django_antispam',
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
