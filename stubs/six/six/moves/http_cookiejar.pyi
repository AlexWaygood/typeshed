"""HTTP cookie handling for web clients.

This module has (now fairly distant) origins in Gisle Aas' Perl module
HTTP::Cookies, from the libwww-perl library.

Docstrings, comments and debug strings in this code refer to the
attributes of the HTTP cookie system as cookie-attributes, to distinguish
them clearly from Python attributes.

Class diagram (note that BSDDBCookieJar and the MSIE* classes are not
distributed with the Python standard library, but are available from
http://wwwsearch.sf.net/):

                        CookieJar____
                        /     \\      \\
            FileCookieJar      \\      \\
             /    |   \\         \\      \\
 MozillaCookieJar | LWPCookieJar \\      \\
                  |               |      \\
                  |   ---MSIEBase |       \\
                  |  /      |     |        \\
                  | /   MSIEDBCookieJar BSDDBCookieJar
                  |/
               MSIECookieJar

"""

from http.cookiejar import *
