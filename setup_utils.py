from setuptools import setup

packages = ["nlp_utils"]

package_data = {"": ["*"]}

install_requires = [
    "selenium==3.141.0",
    "nltk==3.5",
    "pymystem3==0.2.0",
]


setup_kwargs = {
    "name": "nlp_utils",
    "version": "0.1.0",
    "description": "",
    "long_description": None,
    "author": "alexander.slavutin",
    "author_email": "alexander.slavutin@gmail.com",
    "maintainer": "alexander.slavutin",
    "maintainer_email": "alexander.slavutin@gmail.com",
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.7,<4.0",
}

setup(**setup_kwargs)
