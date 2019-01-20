#!/usr/bin/env python

import argparse, datetime, subprocess, sys, ssl, socket, logging, pprint

# Get CLI values and set logging level
class CLI(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', action='store', default="google.com", dest='host',
                            help='inspect the following target to check ssl.')
        parser.add_argument('-p', action='store', default=443, dest='port', help='port that the host is listening on.')
        parser.add_argument('-s', action='store', default='keys', dest='search',
                            help='OpenSSL argument to look for in certificate, use "keys" to get list of keys to retrieve.')
        parser.add_argument('-v', action='store_true', default=False, dest='verbose', help='Enable verbosity/debug.')
        parsedArguments = parser.parse_args()
        self.host = parsedArguments.host
        self.port = int(parsedArguments.port)
        self.search = parsedArguments.search
        self.verbose = parsedArguments.verbose
        if self.host == None:
            print "host undefined use -h or --help"
            sys.exit(1)
        if self.verbose:
            print "Verbose mode enabled."
            print "Logger set: DEBUG"
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        else:
            logging.basicConfig(stream=sys.stdout, level=logging.WARN)

    @property
    def get_host(self):
        logging.info("get_host self.host = %s", self.host)
        return self.host

    @property
    def get_port(self):
        logging.info("get_port self.port =  %s", self.port)
        return self.port

    @property
    def get_search(self):
        logging.info("get_search self.search =  %s", self.search)
        return self.search

    @property
    def get_verbose(self):
        return self.verbose


# Create base SSL connection to address and port
class SSL(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._ssl_sock = self._connector

    @property
    def _connector(self):
        address = (self.host, self.port)
        logging.info("_connector address = %s", address)
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_builder = ssl_context.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=self.host)
        ssl_builder.settimeout(3.0)
        try:
            ssl_builder.connect(address)
            logging.info("Created connection.")
        except:
            logging.error("Failed to create connection.")
            sys.exit(1)
        return ssl_builder

    @property
    def _set_peer_cert(self):
        ssl_connector = self._ssl_sock
        try:
            peer_cert = ssl_connector.getpeercert(binary_form=False)
            logging.info("_set_peer_cert peer_cert = %s", peer_cert)
        except:
            logging.error("_set_peer_cert failed to retrieve peer_cert %s", peer_cert)
            sys.exit(1)
        return peer_cert

    def get_peer_cert_values(self, requested_value):
        peer_cert = self._set_peer_cert
        pp = pprint.PrettyPrinter(indent=4)
        if requested_value == 'keys':
            print "Available keys to search for: "
            for key, value in peer_cert.iteritems():
                print " * " + key + " "
            return requested_value
        else:
            parsed_peer_cert = peer_cert[requested_value]
        return parsed_peer_cert


if __name__ == '__main__':
    cli = CLI()
    ssl = SSL(cli.get_host, cli.get_port)
    print ssl.get_peer_cert_values(cli.get_search)