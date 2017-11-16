import logging

from certbot import interfaces

# import zope.component
import zope.interface

from certbot.plugins import dns_common
from cloudnsapi.api import Api as _cloudnsapi


ACCOUNT_URL = 'https://www.cloudns.net/api-settings/'

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    description = 'Obtain certificates using a DNS TXT record (if you are using ClouDNS for DNS).'
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.records = {}

    @classmethod
    def add_parser_arguments(cls, add): # pylint: disable=missing-docstring
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=30)
        add('credentials', help='ClouDNS credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the ClouDNS API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'ClouDNS credentials INI file',
            {
                'auth-id': 'auth-id for ClouDNS account, obtained from {0}'.format(ACCOUNT_URL),
                'password': 'Password for CloudDNS api user, obtained from {0}'.format(ACCOUNT_URL)
            }
        )
    def _perform(self, domain, validation_name, validation):

        zones = self._get_cloudns_client().list_zones()

        match = {'name': ''}
        for zone in zones:
            if zone['zone'] != 'domain':
                continue
            pos = domain.find(zone['name'])
            logger.debug("Trying to match zone: %s", repr(zone))
            if pos != -1:
                # this is the zone
                logger.debug("Got a match: {}".format(repr(zone)))
                if match['name']:
                    if match['priority'] > pos:
                        match = {'name': zone['name'], 'priority': pos}
                else:
                    match = {'name': zone['name'], 'priority': pos}
        if not match['name']:
            return False
        zonename = match['name']
        logger.debug("Matched domain name: %s", zonename)

        recordname = validation_name.replace(zonename, '')[:-1]

        logger.debug("Record: %s", recordname)

        response = self._get_cloudns_client().add_record(zonename,
                                                         'TXT', recordname, validation, ttl=60)

        if response['status'] != 'Success':
            return False

        self.records[validation_name] = {'id': response['data']['id'], 'zone': zonename}

    def _cleanup(self, domain, validation_name, validation):
        logger.debug("performing cleanup for %s", validation_name)
        response = self._get_cloudns_client().delete_record(self.records[validation_name]['zone'],
                                                            self.records[validation_name]['id']
                                                           )
        logger.debug("Response: %s", repr(response))

    def _get_cloudns_client(self):
        return _cloudnsapi(self.credentials.conf('auth-id'),
                           self.credentials.conf('password'),
                           True
                          )
