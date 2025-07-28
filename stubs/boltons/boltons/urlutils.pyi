""":mod:`urlutils` is a module dedicated to one of software's most
versatile, well-aged, and beloved data structures: the URL, also known
as the `Uniform Resource Locator`_.

Among other things, this module is a full reimplementation of URLs,
without any reliance on the :mod:`urlparse` or :mod:`urllib` standard
library modules. The centerpiece and top-level interface of urlutils
is the :class:`URL` type. Also featured is the :func:`find_all_links`
convenience function. Some low-level functions and constants are also
below.

The implementations in this module are based heavily on `RFC 3986`_ and
`RFC 3987`_, and incorporates details from several other RFCs and `W3C
documents`_.

.. _Uniform Resource Locator: https://en.wikipedia.org/wiki/Uniform_Resource_Locator
.. _RFC 3986: https://tools.ietf.org/html/rfc3986
.. _RFC 3987: https://tools.ietf.org/html/rfc3987
.. _W3C documents: https://www.w3.org/TR/uri-clarification/

"""

from _typeshed import Incomplete

from boltons.dictutils import OrderedMultiDict

SCHEME_PORT_MAP: Incomplete
NO_NETLOC_SCHEMES: Incomplete

class URLParseError(ValueError):
    """Exception inheriting from :exc:`ValueError`, raised when failing to
    parse a URL. Mostly raised on invalid ports and IPv6 addresses.
    """

DEFAULT_ENCODING: str

def to_unicode(obj: object) -> str: ...
def find_all_links(text, with_text: bool = False, default_scheme: str = "https", schemes=()):
    """This function uses heuristics to searches plain text for strings
    that look like URLs, returning a :class:`list` of :class:`URL`
    objects. It supports limiting the accepted schemes, and returning
    interleaved text as well.

    >>> find_all_links('Visit https://boltons.rtfd.org!')
    [URL(u'https://boltons.rtfd.org')]
    >>> find_all_links('Visit https://boltons.rtfd.org!', with_text=True)
    [u'Visit ', URL(u'https://boltons.rtfd.org'), u'!']

    Args:
       text (str): The text to search.

       with_text (bool): Whether or not to interleave plaintext blocks
          with the returned URL objects. Having all tokens can be
          useful for transforming the text, e.g., replacing links with
          HTML equivalents. Defaults to ``False``.

       default_scheme (str): Many URLs are written without the scheme
          component. This function can match a reasonable subset of
          those, provided *default_scheme* is set to a string. Set to
          ``False`` to disable matching scheme-less URLs. Defaults to
          ``'https'``.

       schemes (list): A list of strings that a URL's scheme must
          match in order to be included in the results. Defaults to
          empty, which matches all schemes.

    .. note:: Currently this function does not support finding IPv6
      addresses or URLs with netloc-less schemes, like mailto.

    """

def quote_path_part(text, full_quote: bool = True):
    """
    Percent-encode a single segment of a URL path.
    """

def quote_query_part(text, full_quote: bool = True):
    """
    Percent-encode a single query string key or value.
    """

def quote_fragment_part(text, full_quote: bool = True):
    """Quote the fragment part of the URL. Fragments don't have
    subdelimiters, so the whole URL fragment can be passed.
    """

def quote_userinfo_part(text, full_quote: bool = True):
    """Quote special characters in either the username or password
    section of the URL. Note that userinfo in URLs is considered
    deprecated in many circles (especially browsers), and support for
    percent-encoded userinfo can be spotty.
    """

def unquote(string, encoding: str = "utf-8", errors: str = "replace"):
    """Percent-decode a string, by replacing %xx escapes with their
    single-character equivalent. The optional *encoding* and *errors*
    parameters specify how to decode percent-encoded sequences into
    Unicode characters, as accepted by the :meth:`bytes.decode()` method.  By
    default, percent-encoded sequences are decoded with UTF-8, and
    invalid sequences are replaced by a placeholder character.

    >>> unquote(u'abc%20def')
    u'abc def'
    """

def unquote_to_bytes(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""

def register_scheme(text, uses_netloc=None, default_port=None) -> None:
    """Registers new scheme information, resulting in correct port and
    slash behavior from the URL object. There are dozens of standard
    schemes preregistered, so this function is mostly meant for
    proprietary internal customizations or stopgaps on missing
    standards information. If a scheme seems to be missing, please
    `file an issue`_!

    Args:
        text (str): Text representing the scheme.
           (the 'http' in 'http://hatnote.com')
        uses_netloc (bool): Does the scheme support specifying a
           network host? For instance, "http" does, "mailto" does not.
        default_port (int): The default port, if any, for netloc-using
           schemes.

    .. _file an issue: https://github.com/mahmoud/boltons/issues
    """

def resolve_path_parts(path_parts):
    """Normalize the URL path by resolving segments of '.' and '..',
    resulting in a dot-free path.  See RFC 3986 section 5.2.4, Remove
    Dot Segments.
    """

class cachedproperty:
    """The ``cachedproperty`` is used similar to :class:`property`, except
    that the wrapped method is only called once. This is commonly used
    to implement lazy attributes.

    After the property has been accessed, the value is stored on the
    instance itself, using the same name as the cachedproperty. This
    allows the cache to be cleared with :func:`delattr`, or through
    manipulating the object's ``__dict__``.
    """

    __doc__: Incomplete
    func: Incomplete
    def __init__(self, func) -> None: ...
    def __get__(self, obj, objtype=None): ...

class URL:
    """The URL is one of the most ubiquitous data structures in the
    virtual and physical landscape. From blogs to billboards, URLs are
    so common, that it's easy to overlook their complexity and
    power.

    There are 8 parts of a URL, each with its own semantics and
    special characters:

      * :attr:`~URL.scheme`
      * :attr:`~URL.username`
      * :attr:`~URL.password`
      * :attr:`~URL.host`
      * :attr:`~URL.port`
      * :attr:`~URL.path`
      * :attr:`~URL.query_params` (query string parameters)
      * :attr:`~URL.fragment`

    Each is exposed as an attribute on the URL object. RFC 3986 offers
    this brief structural summary of the main URL components::

        foo://user:pass@example.com:8042/over/there?name=ferret#nose
        \\_/   \\_______/ \\_________/ \\__/\\_________/ \\_________/ \\__/
         |        |          |        |      |           |        |
       scheme  userinfo     host     port   path       query   fragment

    And here's how that example can be manipulated with the URL type:

    >>> url = URL('foo://example.com:8042/over/there?name=ferret#nose')
    >>> print(url.host)
    example.com
    >>> print(url.get_authority())
    example.com:8042
    >>> print(url.qp['name'])  # qp is a synonym for query_params
    ferret

    URL's approach to encoding is that inputs are decoded as much as
    possible, and data remains in this decoded state until re-encoded
    using the :meth:`~URL.to_text()` method. In this way, it's similar
    to Python's current approach of encouraging immediate decoding of
    bytes to text.

    Note that URL instances are mutable objects. If an immutable
    representation of the URL is desired, the string from
    :meth:`~URL.to_text()` may be used. For an immutable, but
    almost-as-featureful, URL object, check out the `hyperlink
    package`_.

    .. _hyperlink package: https://github.com/mahmoud/hyperlink

    """

    scheme: Incomplete
    username: Incomplete
    password: Incomplete
    family: Incomplete
    host: Incomplete
    port: Incomplete
    path_parts: Incomplete
    fragment: Incomplete
    def __init__(self, url: str = "") -> None: ...
    @classmethod
    def from_parts(
        cls, scheme=None, host=None, path_parts=(), query_params=(), fragment: str = "", port=None, username=None, password=None
    ):
        """Build a new URL from parts. Note that the respective arguments are
        not in the order they would appear in a URL:

        Args:
           scheme (str): The scheme of a URL, e.g., 'http'
           host (str): The host string, e.g., 'hatnote.com'
           path_parts (tuple): The individual text segments of the
             path, e.g., ('post', '123')
           query_params (dict): An OMD, dict, or list of (key, value)
             pairs representing the keys and values of the URL's query
             parameters.
           fragment (str): The fragment of the URL, e.g., 'anchor1'
           port (int): The integer port of URL, automatic defaults are
             available for registered schemes.
           username (str): The username for the userinfo part of the URL.
           password (str): The password for the userinfo part of the URL.

        Note that this method does relatively little
        validation. :meth:`URL.to_text()` should be used to check if
        any errors are produced while composing the final textual URL.
        """
    query_params: Incomplete
    qp: Incomplete
    @property
    def path(self):
        """The URL's path, in text form."""

    @path.setter
    def path(self, path_text) -> None: ...
    @property
    def uses_netloc(self):
        """Whether or not a URL uses :code:`:` or :code:`://` to separate the
        scheme from the rest of the URL depends on the scheme's own
        standard definition. There is no way to infer this behavior
        from other parts of the URL. A scheme either supports network
        locations or it does not.

        The URL type's approach to this is to check for explicitly
        registered schemes, with common schemes like HTTP
        preregistered. This is the same approach taken by
        :mod:`urlparse`.

        URL adds two additional heuristics if the scheme as a whole is
        not registered. First, it attempts to check the subpart of the
        scheme after the last ``+`` character. This adds intuitive
        behavior for schemes like ``git+ssh``. Second, if a URL with
        an unrecognized scheme is loaded, it will maintain the
        separator it sees.

        >>> print(URL('fakescheme://test.com').to_text())
        fakescheme://test.com
        >>> print(URL('mockscheme:hello:world').to_text())
        mockscheme:hello:world

        """

    @property
    def default_port(self):
        """Return the default port for the currently-set scheme. Returns
        ``None`` if the scheme is unrecognized. See
        :func:`register_scheme` above. If :attr:`~URL.port` matches
        this value, no port is emitted in the output of
        :meth:`~URL.to_text()`.

        Applies the same '+' heuristic detailed in :meth:`URL.uses_netloc`.
        """

    def normalize(self, with_case: bool = True) -> None:
        """Resolve any "." and ".." references in the path, as well as
        normalize scheme and host casing. To turn off case
        normalization, pass ``with_case=False``.

        More information can be found in `Section 6.2.2 of RFC 3986`_.

        .. _Section 6.2.2 of RFC 3986: https://tools.ietf.org/html/rfc3986#section-6.2.2
        """

    def navigate(self, dest):
        """Factory method that returns a _new_ :class:`URL` based on a given
        destination, *dest*. Useful for navigating those relative
        links with ease.

        The newly created :class:`URL` is normalized before being returned.

        >>> url = URL('http://boltons.readthedocs.io')
        >>> url.navigate('en/latest/')
        URL(u'http://boltons.readthedocs.io/en/latest/')

        Args:
           dest (str): A string or URL object representing the destination

        More information can be found in `Section 5 of RFC 3986`_.

        .. _Section 5 of RFC 3986: https://tools.ietf.org/html/rfc3986#section-5
        """

    def get_authority(self, full_quote: bool = False, with_userinfo: bool = False):
        """Used by URL schemes that have a network location,
        :meth:`~URL.get_authority` combines :attr:`username`,
        :attr:`password`, :attr:`host`, and :attr:`port` into one
        string, the *authority*, that is used for
        connecting to a network-accessible resource.

        Used internally by :meth:`~URL.to_text()` and can be useful
        for labeling connections.

        >>> url = URL('ftp://user@ftp.debian.org:2121/debian/README')
        >>> print(url.get_authority())
        ftp.debian.org:2121
        >>> print(url.get_authority(with_userinfo=True))
        user@ftp.debian.org:2121

        Args:
           full_quote (bool): Whether or not to apply IDNA encoding.
              Defaults to ``False``.
           with_userinfo (bool): Whether or not to include username
              and password, technically part of the
              authority. Defaults to ``False``.

        """

    def to_text(self, full_quote: bool = False):
        """Render a string representing the current state of the URL
        object.

        >>> url = URL('http://listen.hatnote.com')
        >>> url.fragment = 'en'
        >>> print(url.to_text())
        http://listen.hatnote.com#en

        By setting the *full_quote* flag, the URL can either be fully
        quoted or minimally quoted. The most common characteristic of
        an encoded-URL is the presence of percent-encoded text (e.g.,
        %60).  Unquoted URLs are more readable and suitable
        for display, whereas fully-quoted URLs are more conservative
        and generally necessary for sending over the network.
        """

    def __unicode__(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...

def parse_host(host):
    """Low-level function used to parse the host portion of a URL.

    Returns a tuple of (family, host) where *family* is a
    :mod:`socket` module constant or ``None``, and host is a string.

    >>> parse_host('googlewebsite.com') == (None, 'googlewebsite.com')
    True
    >>> parse_host('[::1]') == (socket.AF_INET6, '::1')
    True
    >>> parse_host('192.168.1.1') == (socket.AF_INET, '192.168.1.1')
    True

    Odd doctest formatting above due to py3's switch from int to enums
    for :mod:`socket` constants.

    """

def parse_url(url_text):
    """Used to parse the text for a single URL into a dictionary, used
    internally by the :class:`URL` type.

    Note that "URL" has a very narrow, standards-based
    definition. While :func:`parse_url` may raise
    :class:`URLParseError` under a very limited number of conditions,
    such as non-integer port, a surprising number of strings are
    technically valid URLs. For instance, the text ``"url"`` is a
    valid URL, because it is a relative path.

    In short, do not expect this function to validate form inputs or
    other more colloquial usages of URLs.

    >>> res = parse_url('http://127.0.0.1:3000/?a=1')
    >>> sorted(res.keys())  # res is a basic dictionary
    ['_netloc_sep', 'authority', 'family', 'fragment', 'host', 'password', 'path', 'port', 'query', 'scheme', 'username']
    """

DEFAULT_PARSED_URL: Incomplete

def parse_qsl(qs, keep_blank_values: bool = True, encoding="utf8"):
    """
    Converts a query string into a list of (key, value) pairs.
    """

PREV: Incomplete
NEXT: Incomplete
KEY: Incomplete
VALUE: Incomplete
SPREV: Incomplete
SNEXT: Incomplete

OMD = OrderedMultiDict

class QueryParamDict(OrderedMultiDict[Incomplete, Incomplete]):
    """A subclass of :class:`~dictutils.OrderedMultiDict` specialized for
    representing query string values. Everything is fully unquoted on
    load and all parsed keys and values are strings by default.

    As the name suggests, multiple values are supported and insertion
    order is preserved.

    >>> qp = QueryParamDict.from_text(u'key=val1&key=val2&utm_source=rtd')
    >>> qp.getlist('key')
    [u'val1', u'val2']
    >>> qp['key']
    u'val2'
    >>> qp.add('key', 'val3')
    >>> qp.to_text()
    'key=val1&key=val2&utm_source=rtd&key=val3'

    See :class:`~dictutils.OrderedMultiDict` for more API features.
    """

    @classmethod
    def from_text(cls, query_string):
        """
        Parse *query_string* and return a new :class:`QueryParamDict`.
        """

    def to_text(self, full_quote: bool = False):
        """
        Render and return a query string.

        Args:
           full_quote (bool): Whether or not to percent-quote special
              characters or leave them decoded for readability.
        """
