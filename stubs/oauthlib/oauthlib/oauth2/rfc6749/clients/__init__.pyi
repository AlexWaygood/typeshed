"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming OAuth 2.0 RFC6749.
"""

from .backend_application import BackendApplicationClient as BackendApplicationClient
from .base import AUTH_HEADER as AUTH_HEADER, BODY as BODY, URI_QUERY as URI_QUERY, Client as Client
from .legacy_application import LegacyApplicationClient as LegacyApplicationClient
from .mobile_application import MobileApplicationClient as MobileApplicationClient
from .service_application import ServiceApplicationClient as ServiceApplicationClient
from .web_application import WebApplicationClient as WebApplicationClient
