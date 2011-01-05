from setuptools import setup, find_packages

version = __import__('django_commands').__version__

setup(
    name = 'django-commands',
    version = version,
    description="Database and cache management command extensions for the Django web framework",
    author="Mart Sõmermaa",
    author_email="mrts.pydev at gmail dot com",
    url="http://github.com/mrts/django-commands",
    license="MIT",
    packages=find_packages(exclude=['tests']),
)
