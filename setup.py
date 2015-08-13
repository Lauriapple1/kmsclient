from distutils.core import setup

setup(
    name='kmsclient',
    packages=['kmsclient'],
    version='0.1',
    description='For encrypting and decrypting using a specific key from amazons kms',
    author='Mark Kelly',
    author_email='mkelly28@tcd.ie',
    url='https://github.com/zalando/kmsclient',
    download_url='https://github.com/zalando/kmsclient/tarball/0.1',
    keywords=['kms', 'aws', 'key', 'management', 'system', 'client', 'encryption'],
    classifiers=[],
    entry_points={'console_scripts': 'kmsclient = kmsclient.cli:main'},
    install_requires=['clickclick', 'pyperclip', 'boto3'],
    license='Apache License 2.0'
)
