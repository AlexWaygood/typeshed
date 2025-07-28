"""HTTP server classes.

Note: BaseHTTPRequestHandler doesn't implement any HTTP request; see
SimpleHTTPRequestHandler for simple implementations of GET, HEAD and POST,
and (deprecated) CGIHTTPRequestHandler for CGI scripts.

It does, however, optionally implement HTTP/1.1 persistent connections.

Notes on CGIHTTPRequestHandler
------------------------------

This class is deprecated. It implements GET and POST requests to cgi-bin scripts.

If the os.fork() function is not present (Windows), subprocess.Popen() is used,
with slightly altered but never documented semantics.  Use from a threaded
process is likely to trigger a warning at os.fork() time.

In all cases, the implementation is intentionally naive -- all
requests are executed synchronously.

SECURITY WARNING: DON'T USE THIS CODE UNLESS YOU ARE INSIDE A FIREWALL
-- it may execute arbitrary Python code or external programs.

Note that status code 200 is sent prior to execution of a CGI script, so
scripts cannot send other status codes such as 302 (redirect).

XXX To do:

- log requests even later (to capture byte count)
- log user-agent header and other interesting goodies
- send error log to separate file
"""

from http.server import *
