"""
=========================
Smart Quotes for Docutils
=========================

Synopsis
========

"SmartyPants" is a free web publishing plug-in for Movable Type, Blosxom, and
BBEdit that easily translates plain ASCII punctuation characters into "smart"
typographic punctuation characters.

``smartquotes.py`` is an adaption of "SmartyPants" to Docutils_.

* Using Unicode instead of HTML entities for typographic punctuation
  characters, it works for any output format that supports Unicode.
* Supports `language specific quote characters`__.

__ https://en.wikipedia.org/wiki/Non-English_usage_of_quotation_marks


Authors
=======

`John Gruber`_ did all of the hard work of writing this software in Perl for
`Movable Type`_ and almost all of this useful documentation.  `Chad Miller`_
ported it to Python to use with Pyblosxom_.
Adapted to Docutils_ by Günter Milde.

Additional Credits
==================

Portions of the SmartyPants original work are based on Brad Choate's nifty
MTRegex plug-in.  `Brad Choate`_ also contributed a few bits of source code to
this plug-in.  Brad Choate is a fine hacker indeed.

`Jeremy Hedley`_ and `Charles Wiltgen`_ deserve mention for exemplary beta
testing of the original SmartyPants.

`Rael Dornfest`_ ported SmartyPants to Blosxom.

.. _Brad Choate: http://bradchoate.com/
.. _Jeremy Hedley: http://antipixel.com/
.. _Charles Wiltgen: http://playbacktime.com/
.. _Rael Dornfest: http://raelity.org/


Copyright and License
=====================

SmartyPants_ license (3-Clause BSD license):

  Copyright (c) 2003 John Gruber (http://daringfireball.net/)
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name "SmartyPants" nor the names of its contributors
    may be used to endorse or promote products derived from this
    software without specific prior written permission.

  This software is provided by the copyright holders and contributors
  "as is" and any express or implied warranties, including, but not
  limited to, the implied warranties of merchantability and fitness for
  a particular purpose are disclaimed. In no event shall the copyright
  owner or contributors be liable for any direct, indirect, incidental,
  special, exemplary, or consequential damages (including, but not
  limited to, procurement of substitute goods or services; loss of use,
  data, or profits; or business interruption) however caused and on any
  theory of liability, whether in contract, strict liability, or tort
  (including negligence or otherwise) arising in any way out of the use
  of this software, even if advised of the possibility of such damage.

smartypants.py license (2-Clause BSD license):

  smartypants.py is a derivative work of SmartyPants.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  This software is provided by the copyright holders and contributors
  "as is" and any express or implied warranties, including, but not
  limited to, the implied warranties of merchantability and fitness for
  a particular purpose are disclaimed. In no event shall the copyright
  owner or contributors be liable for any direct, indirect, incidental,
  special, exemplary, or consequential damages (including, but not
  limited to, procurement of substitute goods or services; loss of use,
  data, or profits; or business interruption) however caused and on any
  theory of liability, whether in contract, strict liability, or tort
  (including negligence or otherwise) arising in any way out of the use
  of this software, even if advised of the possibility of such damage.

.. _John Gruber: http://daringfireball.net/
.. _Chad Miller: http://web.chad.org/

.. _Pyblosxom: http://pyblosxom.bluesock.org/
.. _SmartyPants: http://daringfireball.net/projects/smartypants/
.. _Movable Type: http://www.movabletype.org/
.. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause
.. _Docutils: https://docutils.sourceforge.io/

Description
===========

SmartyPants can perform the following transformations:

- Straight quotes ( " and ' ) into "curly" quote characters
- Backticks-style quotes (\\`\\`like this'') into "curly" quote characters
- Dashes (``--`` and ``---``) into en- and em-dash entities
- Three consecutive dots (``...`` or ``. . .``) into an ellipsis ``…``.

This means you can write, edit, and save your posts using plain old
ASCII straight quotes, plain dashes, and plain dots, but your published
posts (and final HTML output) will appear with smart quotes, em-dashes,
and proper ellipses.

Backslash Escapes
=================

If you need to use literal straight quotes (or plain hyphens and periods),
`smartquotes` accepts the following backslash escape sequences to force
ASCII-punctuation. Mind, that you need two backslashes in "docstrings", as
Python expands them, too.

========  =========
Escape    Character
========  =========
``\\\\``    \\\\
``\\\\"``   \\\\"
``\\\\'``   \\\\'
``\\\\.``   \\\\.
``\\\\-``   \\\\-
``\\\\```   \\\\`
========  =========

This is useful, for example, when you want to use straight quotes as
foot and inch marks: 6\\\\'2\\\\" tall; a 17\\\\" iMac.


Caveats
=======

Why You Might Not Want to Use Smart Quotes in Your Weblog
---------------------------------------------------------

For one thing, you might not care.

Most normal, mentally stable individuals do not take notice of proper
typographic punctuation. Many design and typography nerds, however, break
out in a nasty rash when they encounter, say, a restaurant sign that uses
a straight apostrophe to spell "Joe's".

If you're the sort of person who just doesn't care, you might well want to
continue not caring. Using straight quotes -- and sticking to the 7-bit
ASCII character set in general -- is certainly a simpler way to live.

Even if you *do* care about accurate typography, you still might want to
think twice before educating the quote characters in your weblog. One side
effect of publishing curly quote characters is that it makes your
weblog a bit harder for others to quote from using copy-and-paste. What
happens is that when someone copies text from your blog, the copied text
contains the 8-bit curly quote characters (as well as the 8-bit characters
for em-dashes and ellipses, if you use these options). These characters
are not standard across different text encoding methods, which is why they
need to be encoded as characters.

People copying text from your weblog, however, may not notice that you're
using curly quotes, and they'll go ahead and paste the unencoded 8-bit
characters copied from their browser into an email message or their own
weblog. When pasted as raw "smart quotes", these characters are likely to
get mangled beyond recognition.

That said, my own opinion is that any decent text editor or email client
makes it easy to stupefy smart quote characters into their 7-bit
equivalents, and I don't consider it my problem if you're using an
indecent text editor or email client.


Algorithmic Shortcomings
------------------------

One situation in which quotes will get curled the wrong way is when
apostrophes are used at the start of leading contractions. For example::

  'Twas the night before Christmas.

In the case above, SmartyPants will turn the apostrophe into an opening
secondary quote, when in fact it should be the `RIGHT SINGLE QUOTATION MARK`
character which is also "the preferred character to use for apostrophe"
(Unicode). I don't think this problem can be solved in the general case --
every word processor I've tried gets this wrong as well. In such cases, it's
best to inset the `RIGHT SINGLE QUOTATION MARK` (’) by hand.

In English, the same character is used for apostrophe and  closing secondary
quote (both plain and "smart" ones). For other locales (French, Italean,
Swiss, ...) "smart" secondary closing quotes differ from the curly apostrophe.

   .. class:: language-fr

   Il dit : "C'est 'super' !"

If the apostrophe is used at the end of a word, it cannot be distinguished
from a secondary quote by the algorithm. Therefore, a text like::

   .. class:: language-de-CH

   "Er sagt: 'Ich fass' es nicht.'"

will get a single closing guillemet instead of an apostrophe.

This can be prevented by use use of the `RIGHT SINGLE QUOTATION MARK` in
the source::

   -  "Er sagt: 'Ich fass' es nicht.'"
   +  "Er sagt: 'Ich fass’ es nicht.'"


Version History
===============

1.10    2023-11-18
        - Pre-compile regexps once, not with every call of `educateQuotes()`
          (patch #206 by Chris Sewell). Simplify regexps.

1.9     2022-03-04
        - Code cleanup. Require Python 3.

1.8.1   2017-10-25
        - Use open quote after Unicode whitespace, ZWSP, and ZWNJ.
        - Code cleanup.

1.8:    2017-04-24
        - Command line front-end.

1.7.1:  2017-03-19
        - Update and extend language-dependent quotes.
        - Differentiate apostrophe from single quote.

1.7:    2012-11-19
        - Internationalization: language-dependent quotes.

1.6.1:  2012-11-06
        - Refactor code, code cleanup,
        - `educate_tokens()` generator as interface for Docutils.

1.6:    2010-08-26
        - Adaption to Docutils:
          - Use Unicode instead of HTML entities,
          - Remove code special to pyblosxom.

1.5_1.6: Fri, 27 Jul 2007 07:06:40 -0400
        - Fixed bug where blocks of precious unalterable text was instead
          interpreted.  Thanks to Le Roux and Dirk van Oosterbosch.

1.5_1.5: Sat, 13 Aug 2005 15:50:24 -0400
        - Fix bogus magical quotation when there is no hint that the
          user wants it, e.g., in "21st century".  Thanks to Nathan Hamblen.
        - Be smarter about quotes before terminating numbers in an en-dash'ed
          range.

1.5_1.4: Thu, 10 Feb 2005 20:24:36 -0500
        - Fix a date-processing bug, as reported by jacob childress.
        - Begin a test-suite for ensuring correct output.
        - Removed import of "string", since I didn't really need it.
          (This was my first every Python program.  Sue me!)

1.5_1.3: Wed, 15 Sep 2004 18:25:58 -0400
        - Abort processing if the flavour is in forbidden-list.  Default of
          [ "rss" ]   (Idea of Wolfgang SCHNERRING.)
        - Remove stray virgules from en-dashes.  Patch by Wolfgang SCHNERRING.

1.5_1.2: Mon, 24 May 2004 08:14:54 -0400
        - Some single quotes weren't replaced properly.  Diff-tesuji played
          by Benjamin GEIGER.

1.5_1.1: Sun, 14 Mar 2004 14:38:28 -0500
        - Support upcoming pyblosxom 0.9 plugin verification feature.

1.5_1.0: Tue, 09 Mar 2004 08:08:35 -0500
        - Initial release
"""

from collections.abc import Generator, Iterable
from re import Pattern
from typing import ClassVar, Final, Literal

options: Final[str]

class smartchars:
    """Smart quotes and dashes"""

    endash: ClassVar[str]
    emdash: ClassVar[str]
    ellipsis: ClassVar[str]
    apostrophe: ClassVar[str]
    quotes: ClassVar[dict[str, str | tuple[str, str, str, str]]]
    language: str
    def __init__(self, language: str = "en") -> None: ...

class RegularExpressions:
    START_SINGLE: ClassVar[Pattern[str]]
    START_DOUBLE: ClassVar[Pattern[str]]
    ADJACENT_1: ClassVar[Pattern[str]]
    ADJACENT_2: ClassVar[Pattern[str]]
    OPEN_SINGLE: ClassVar[Pattern[str]]
    OPEN_DOUBLE: ClassVar[Pattern[str]]
    DECADE: ClassVar[Pattern[str]]
    APOSTROPHE: ClassVar[Pattern[str]]
    OPENING_SECONDARY: ClassVar[Pattern[str]]
    CLOSING_SECONDARY: ClassVar[Pattern[str]]
    OPENING_PRIMARY: ClassVar[Pattern[str]]
    CLOSING_PRIMARY: ClassVar[Pattern[str]]

regexes: RegularExpressions
default_smartypants_attr: Final = "1"

def smartyPants(text: str, attr="1", language: str = "en") -> str:
    """Main function for "traditional" use."""

def educate_tokens(text_tokens: Iterable[tuple[str, str]], attr="1", language: str = "en") -> Generator[str]:
    """Return iterator that "educates" the items of `text_tokens`."""

def educateQuotes(text: str, language: str = "en") -> str:
    """
    Parameter:  - text string (unicode or bytes).
                - language (`BCP 47` language tag.)
    Returns:    The `text`, with "educated" curly quote characters.

    Example input:  "Isn't this fun?"
    Example output: “Isn’t this fun?“
    """

def educateBackticks(text: str, language: str = "en") -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with ``backticks'' -style double quotes
                translated into HTML curly quote entities.
    Example input:  ``Isn't this fun?''
    Example output: “Isn't this fun?“
    """

def educateSingleBackticks(text: str, language: str = "en") -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with `backticks' -style single quotes
                translated into HTML curly quote entities.

    Example input:  `Isn't this fun?'
    Example output: ‘Isn’t this fun?’
    """

def educateDashes(text: str) -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an em-dash character.
    """

def educateDashesOldSchool(text: str) -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an en-dash character, and each "---" translated to
                an em-dash character.
    """

def educateDashesOldSchoolInverted(text: str) -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an em-dash character, and each "---" translated to
                an en-dash character. Two reasons why: First, unlike the
                en- and em-dash syntax supported by
                EducateDashesOldSchool(), it's compatible with existing
                entries written before SmartyPants 1.1, back when "--" was
                only used for em-dashes.  Second, em-dashes are more
                common than en-dashes, and so it sort of makes sense that
                the shortcut should be shorter to type. (Thanks to Aaron
                Swartz for the idea.)
    """

def educateEllipses(text: str) -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "..." translated to
                an ellipsis character.

    Example input:  Huh...?
    Example output: Huh…?
    """

def stupefyEntities(text: str, language: str = "en") -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each SmartyPants character translated to
                its ASCII counterpart.

    Example input:  “Hello — world.”
    Example output: "Hello -- world."
    """

def processEscapes(text: str, restore: bool = False) -> str:
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with after processing the following backslash
                escape sequences. This is useful if you want to force a "dumb"
                quote or other character to appear.

                Escape  Value
                ------  -----
                \\\\      &#92;
                \\"      &#34;
                \\'      &#39;
                \\.      &#46;
                \\-      &#45;
                \\`      &#96;
    """

def tokenize(text: str) -> Generator[tuple[Literal["tag", "text"], str]]:
    """
    Parameter:  String containing HTML markup.
    Returns:    An iterator that yields the tokens comprising the input
                string. Each token is either a tag (possibly with nested,
                tags contained therein, such as <a href="<MTFoo>">, or a
                run of text between tags. Each yielded element is a
                two-element tuple; the first is either 'tag' or 'text';
                the second is the actual value.

    Based on the _tokenize() subroutine from Brad Choate's MTRegex plugin.
    """
