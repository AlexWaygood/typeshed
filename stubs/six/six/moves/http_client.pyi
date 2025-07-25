"""HTTP/1.1 client library

<intro stuff goes here>
<other stuff, too>

HTTPConnection goes through a number of "states", which define when a client
may legally make another request or fetch the response for a particular
request. This diagram details these state transitions:

    (null)
      |
      | HTTPConnection()
      v
    Idle
      |
      | putrequest()
      v
    Request-started
      |
      | ( putheader() )*  endheaders()
      v
    Request-sent
      |\\_____________________________
      |                              | getresponse() raises
      | response = getresponse()     | ConnectionError
      v                              v
    Unread-response                Idle
    [Response-headers-read]
      |\\____________________
      |                     |
      | response.read()     | putrequest()
      v                     v
    Idle                  Req-started-unread-response
                     ______/|
                   /        |
   response.read() |        | ( putheader() )*  endheaders()
                   v        v
       Request-started    Req-sent-unread-response
                            |
                            | response.read()
                            v
                          Request-sent

This diagram presents the following rules:
  -- a second request may not be started until {response-headers-read}
  -- a response [object] cannot be retrieved until {request-sent}
  -- there is no differentiation between an unread response body and a
     partially read response body

Note: this enforcement is applied by the HTTPConnection class. The
      HTTPResponse class does not enforce this state machine, which
      implies sophisticated clients may accelerate the request/response
      pipeline. Caution should be taken, though: accelerating the states
      beyond the above pattern may imply knowledge of the server's
      connection-close behavior for certain requests. For example, it
      is impossible to tell whether the server will close the connection
      UNTIL the response headers have been read; this means that further
      requests cannot be placed into the pipeline until it is known that
      the server will NOT be closing the connection.

Logical State                  __state            __response
-------------                  -------            ----------
Idle                           _CS_IDLE           None
Request-started                _CS_REQ_STARTED    None
Request-sent                   _CS_REQ_SENT       None
Unread-response                _CS_IDLE           <response_class>
Req-started-unread-response    _CS_REQ_STARTED    <response_class>
Req-sent-unread-response       _CS_REQ_SENT       <response_class>
"""

# Many definitions are not included in http.client.__all__
from http.client import *
from http.client import (
    ACCEPTED as ACCEPTED,
    BAD_GATEWAY as BAD_GATEWAY,
    BAD_REQUEST as BAD_REQUEST,
    CONFLICT as CONFLICT,
    CONTINUE as CONTINUE,
    CREATED as CREATED,
    EXPECTATION_FAILED as EXPECTATION_FAILED,
    FAILED_DEPENDENCY as FAILED_DEPENDENCY,
    FORBIDDEN as FORBIDDEN,
    FOUND as FOUND,
    GATEWAY_TIMEOUT as GATEWAY_TIMEOUT,
    GONE as GONE,
    HTTP_PORT as HTTP_PORT,
    HTTP_VERSION_NOT_SUPPORTED as HTTP_VERSION_NOT_SUPPORTED,
    HTTPS_PORT as HTTPS_PORT,
    IM_USED as IM_USED,
    INSUFFICIENT_STORAGE as INSUFFICIENT_STORAGE,
    INTERNAL_SERVER_ERROR as INTERNAL_SERVER_ERROR,
    LENGTH_REQUIRED as LENGTH_REQUIRED,
    LOCKED as LOCKED,
    METHOD_NOT_ALLOWED as METHOD_NOT_ALLOWED,
    MOVED_PERMANENTLY as MOVED_PERMANENTLY,
    MULTI_STATUS as MULTI_STATUS,
    MULTIPLE_CHOICES as MULTIPLE_CHOICES,
    NETWORK_AUTHENTICATION_REQUIRED as NETWORK_AUTHENTICATION_REQUIRED,
    NO_CONTENT as NO_CONTENT,
    NON_AUTHORITATIVE_INFORMATION as NON_AUTHORITATIVE_INFORMATION,
    NOT_ACCEPTABLE as NOT_ACCEPTABLE,
    NOT_EXTENDED as NOT_EXTENDED,
    NOT_FOUND as NOT_FOUND,
    NOT_IMPLEMENTED as NOT_IMPLEMENTED,
    NOT_MODIFIED as NOT_MODIFIED,
    OK as OK,
    PARTIAL_CONTENT as PARTIAL_CONTENT,
    PAYMENT_REQUIRED as PAYMENT_REQUIRED,
    PRECONDITION_FAILED as PRECONDITION_FAILED,
    PRECONDITION_REQUIRED as PRECONDITION_REQUIRED,
    PROCESSING as PROCESSING,
    PROXY_AUTHENTICATION_REQUIRED as PROXY_AUTHENTICATION_REQUIRED,
    REQUEST_ENTITY_TOO_LARGE as REQUEST_ENTITY_TOO_LARGE,
    REQUEST_HEADER_FIELDS_TOO_LARGE as REQUEST_HEADER_FIELDS_TOO_LARGE,
    REQUEST_TIMEOUT as REQUEST_TIMEOUT,
    REQUEST_URI_TOO_LONG as REQUEST_URI_TOO_LONG,
    REQUESTED_RANGE_NOT_SATISFIABLE as REQUESTED_RANGE_NOT_SATISFIABLE,
    RESET_CONTENT as RESET_CONTENT,
    SEE_OTHER as SEE_OTHER,
    SERVICE_UNAVAILABLE as SERVICE_UNAVAILABLE,
    SWITCHING_PROTOCOLS as SWITCHING_PROTOCOLS,
    TEMPORARY_REDIRECT as TEMPORARY_REDIRECT,
    TOO_MANY_REQUESTS as TOO_MANY_REQUESTS,
    UNAUTHORIZED as UNAUTHORIZED,
    UNPROCESSABLE_ENTITY as UNPROCESSABLE_ENTITY,
    UNSUPPORTED_MEDIA_TYPE as UNSUPPORTED_MEDIA_TYPE,
    UPGRADE_REQUIRED as UPGRADE_REQUIRED,
    USE_PROXY as USE_PROXY,
    HTTPMessage as HTTPMessage,
    parse_headers as parse_headers,
)
