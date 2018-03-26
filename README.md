# ssl_cert_inspector
Python based CLI tool for inspecting properties in SSL certs

```
$python ssl_cert_check.py -h
usage: ssl_cert_check.py [-h] [-i HOST] [-p PORT] [-s SEARCH] [-v]

optional arguments:
  -h, --help  show this help message and exit
  -i HOST     inspect the following target to check ssl.
  -p PORT     port that the host is listening on.
  -s SEARCH   OpenSSL argument to look for in certificate, use "keys" to get
              list of keys to retrieve.
  -v          Enable verbosity/debug.
  ```

Pass it a host to inspect and port it's listening on and it will return available keys for that cert:
```
$python ssl_cert_check.py -i google.com -p 443
Available keys to search for:
 * crlDistributionPoints
 * subjectAltName
 * notBefore
 * caIssuers
 * OCSP
 * serialNumber
 * notAfter
 * version
 * subject
 * issuer
 ```
 
For example notBefore or notAfter for issue date and expiration dates:
````
$python ssl_cert_check.py -i google.com -p 443 -s notBefore
Mar  7 18:50:00 2018 GMT

$python ssl_cert_check.py -i google.com -p 443 -s notAfter
May 30 18:50:00 2018 GMT
````
