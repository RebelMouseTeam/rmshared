import setuptools


setuptools.setup(
    name='rmshared',
    version='0.2.2',
    author='CordiS',
    author_email='cordis@rebelmouse.com',
    url='https://github.com/RebelMouseTeam/rmshared',
    license='Apache 2.0',
    packages=['rmshared', 'rmshared.content', 'rmshared.content.taxonomy'],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
    ],
)
