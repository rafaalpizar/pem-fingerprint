#!/usr/bin/env python3
import subprocess

'''
Tool to extract PEM format certificates from xml comfig
and calculates all the fingerprints

Usage:
cat cert_in_pem_format.txt | python fingerprint.py

Author: Rafael Alpizar Lopez

Version: 1.0

Change Log:
2017-12-06 - File header comment update
'''

import sys

certs = dict()


def process_cert():
    lines = sys.stdin.readlines()
    cert_count = -1
    read_certificate = False
    first_line = False
    last_line = False
    for line in lines:
        if line.find('BEGIN CERTIFICATE')>-1 and not read_certificate:
            cert_count += 1
            read_certificate = True
            first_line = True
        elif line.find('END CERTIFICATE')>-1 and read_certificate:
            last_line = True
            read_certificate = False

        if read_certificate:
            if first_line:
                certs[cert_count] = '-----BEGIN CERTIFICATE-----\n'
                first_line = False
            else:
                certs[cert_count] += line
        if last_line:
            certs[cert_count] += '-----END CERTIFICATE-----\n'
            last_line = False

    for i in certs:
        # DEBUG print certs[i]
        res = subprocess.Popen(['openssl', 'x509', '-noout', '-fingerprint', '-sha1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err= res.communicate(certs[i])
        print(out)
            
    return 0

def main():
    test = process_cert()


if __name__ == '__main__':
    main()
