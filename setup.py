from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['sys', 'argparse', 'aocr', 'numpy', 'time', 'glob', 'opencv-python', 'ast', 'json', 'requests', 'flask', 'flask_restful', 'flask_httpauth', 'uuid', 'shutil', 'pillow', 'hashlib', 'io', 'pyppeteer', 'tkinter']
VERSION = '1.0'
try:
    import pypandoc
    README = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    README = open('README.md').read()


setup(
    name='captcha22',
    url='https://github.com/TinusGreen/pip_test',
    download_url='https://github.com/TinusGreen/pip_test/archive/{}.tar.gz'.format(VERSION),
    author='Tinus Green',
    author_email='work@tinusgreen.co.za',
    version=VERSION,
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=('''CAPTCHA Cracking Server and Client based '''
                 '''on Tensorflow, attention-ocr and Flask. '''),
    long_description=README,
    entry_points={
        'console_scripts': ['captcha22=captcha22.__main__'],
    }
)