#!/usr/bin/env python3
'''
Helper script to encrypt and decrypt data using amazon kms
'''

import boto3
import base64
import click

try:
    import pyperclip
except:
    pyperclip = None

def awsKmsClient(region_name, aws_access_key, aws_secret_key):
    return boto3.client(service_name='kms', region_name=region_name,
                        aws_secret_access_key=aws_access_key,
                        aws_access_key_id=aws_secret_key
                        )

@click.group()
def cli():
    pass

@cli.command()
@click.argument('to_encrypt')
@click.argument('region')
@click.argument('key_id')
@click.option('-ak', '--aws-access-key', help='AWS access key')
@click.option('-sk', '--aws-secret-key', help='AWS secret key')
@click.option('-c', '--clip', is_flag=True, help='Copy encrypted value into clipboard', default=False)
def encrypt(to_encrypt, region, key_id, aws_access_key, aws_secret_key, clip):
    print('encrypting ' + to_encrypt + ' with region ' + region + ' and key_id ' + key_id + ' ...')
    encrypted = aws_encrypt(region, key_id, to_encrypt, aws_access_key, aws_secret_key)
    print(encrypted)

    if clip:
        if pyperclip is not None:
            pyperclip.copy(encrypted)

def aws_encrypt(region, key_id, to_encrypt, aws_access_key, aws_secret_key):
    client = awsKmsClient(region, aws_access_key, aws_secret_key)
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=to_encrypt
    )
    return str(base64.b64encode(response['CiphertextBlob']), "UTF-8")

@cli.command()
@click.argument('to_decrypt')
@click.argument('region')
@click.option('-ak', '--aws-access-key', help='AWS access key')
@click.option('-sk', '--aws-secret-key', help='AWS secret key')
@click.option('-c', '--clip', is_flag=True, help='Copy decrypted value into clipboard', default=False)
def decrypt(to_decrypt, region, aws_access_key, aws_secret_key, clip):
    print('decrypting ' + to_decrypt + ' with region ' + region + ' ...')
    decrypted = aws_decrypt(bytes(to_decrypt, "UTF-8"), region, aws_access_key, aws_secret_key)
    print(decrypted)

    if clip:
        if pyperclip is not None:
            pyperclip.copy(decrypted)

def aws_decrypt(to_decrypt, region, aws_access_key, aws_secret_key):
    client = awsKmsClient(region, aws_access_key, aws_secret_key)
    response = client.decrypt(
        CiphertextBlob=base64.b64decode(to_decrypt)
    )
    return str(response['Plaintext'], "UTF-8")


def main():
    cli()

if __name__ == '__main__':
    main()
