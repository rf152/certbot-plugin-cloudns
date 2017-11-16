# certbot-plugin-cloudns

A plugin for Certbot that uses ClouDNS to validate domain ownership

Usage is: `certbot --authenticator certbot-plugin-cloudns:dns-cloudns --certbot-plugin-cloudns:dns-cloudns-credentials /path/to/credentials.ini -d www.example.com certonly`

The contents of credentials.ini should be:

```
certbot_plugin_cloudns:dns_cloudns_auth_id=<auth-id>
certbot_plugin_cloudns:dns_cloudns_password=<auth-password>
```