#!/usr/bin/env python

import argparse
import datetime
import subprocess
import sys
import ssl
import socket
import logging
import pprint

class Arguments(object):
    def argumentParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', action='store', dest='host', help='inspect the following target to check ssl.')
        parser.add_argument('-p', action='store', default=443, dest='port', help='port that the host is listening on.')
        parser.add_argument('-s', action='store', default='keys', dest='search', help='OpenSSL argument to look for in certificate, use "keys" to get list of keys to retrieve.')
        parser.add_argument('-v', action='store_true', default=False, dest='verbose', help='Enable verbosity/debug.')
        parsedArguments = parser.parse_args()
        host = parsedArguments.host
        port = int(parsedArguments.port)
        search = parsedArguments.search
        verbose = parsedArguments.verbose
        if verbose:
            print "Verbose mode enabled."
        return host, port, search, verbose

    def logMode(self, verbose):
        if verbose:
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
            print "Logger set: DEBUG"
        else:
            logging.basicConfig(stream=sys.stdout, level=logging.WARN)


class Check(object):
    def createConnection(self, host, port):
        address = (host, port)
        sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        sslConnection = sslContext.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=host)
        sslConnection.settimeout(3.0)
        sslConnection.connect((host, port))
        logging.info("Created sslConnection.")
        return sslConnection

    def getPeerCert(self, sslConnection):
        peerCert = sslConnection.getpeercert(binary_form=False)
        logging.info("Retrieved Peer Cert\n %s", peerCert)
        return peerCert

    def parsePeerCert(self, peerCert, parseString):
        pp = pprint.PrettyPrinter(indent=4)
        if parseString == 'keys':
            print "Available keys to search for: "
            for key, value in peerCert.iteritems():
                print " * " + key + " "
            return parseString
        else:
            parsedPeerCert = peerCert[parseString]
        return parsedPeerCert

    def output(self, parsedPeerCert):
        if parsedPeerCert == "keys":
            quit
        else:
            print parsedPeerCert

class Main(object):
    def main(self):
        host, port, search, verbose= Arguments().argumentParser()
        Arguments().logMode(verbose)
        sslConnecton = Check().createConnection(host, port)
        peerCert = Check().getPeerCert(sslConnecton)
        parsedPeerCert = Check().parsePeerCert(peerCert, search)
        Check().output(parsedPeerCert)

Main().main()
