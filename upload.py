import importlib
import requests
import sys
import os


def upload_package():
    username, password = sys.argv[1], sys.argv[2]
    os.system('python setup.py sdist bdist_wheel')
    os.system(f'twine upload dist/* -u {username} -p {password}')
    sys.exit(0)


res = requests.get('https://badge.fury.io/py/likeshell')
url = res.url.strip('/').split('/')
current_version = url[-1].split('.')


version = importlib.import_module('likeshell.__version__').__version__.split('.')

if current_version[0] < version[0]:
    upload_package()

if current_version[1] < version[1]:
    upload_package()

if current_version[2] < version[2]:
    upload_package()

print('No release.')
