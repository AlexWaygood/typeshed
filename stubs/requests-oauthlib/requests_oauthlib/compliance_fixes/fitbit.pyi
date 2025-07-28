"""
The Fitbit API breaks from the OAuth2 RFC standard by returning an "errors"
object list, rather than a single "error" string. This puts hooks in place so
that oauthlib can process an error in the results from access token and refresh
token responses. This is necessary to prevent getting the generic red herring
MissingTokenError.
"""

from requests_oauthlib import OAuth2Session

def fitbit_compliance_fix(session: OAuth2Session) -> OAuth2Session: ...
