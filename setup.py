from setuptools import setup

setup(
    name='ibbynotes',
    version='1.0',
    description='An IB compatible, 8 (modifiable) day cycle calendar written in python.',
    author='CookieUzen',
    author_email='uzen.huang@gmail.com',
    package='ibbycal',
    install_requires=['ics', 'arrow', 'pyyaml'],
)
