"""passlib.pwd -- password generation helpers"""

import random
from abc import abstractmethod
from collections.abc import Callable, Iterator, MutableMapping, Sequence
from typing import Any, Final, Literal, overload
from typing_extensions import Self, TypeAlias

class SequenceGenerator:
    """
    Base class used by word & phrase generators.

    These objects take a series of options, corresponding
    to those of the :func:`generate` function.
    They act as callables which can be used to generate a password
    or a list of 1+ passwords. They also expose some read-only
    informational attributes.

    Parameters
    ----------
    :param entropy:
        Optionally specify the amount of entropy the resulting passwords
        should contain (as measured with respect to the generator itself).
        This will be used to auto-calculate the required password size.

    :param length:
        Optionally specify the length of password to generate,
        measured as count of whatever symbols the subclass uses (characters or words).
        Note if ``entropy`` requires a larger minimum length,
        that will be used instead.

    :param rng:
        Optionally provide a custom RNG source to use.
        Should be an instance of :class:`random.Random`,
        defaults to :class:`random.SystemRandom`.

    Attributes
    ----------
    .. autoattribute:: length
    .. autoattribute:: symbol_count
    .. autoattribute:: entropy_per_symbol
    .. autoattribute:: entropy

    Subclassing
    -----------
    Subclasses must implement the ``.__next__()`` method,
    and set ``.symbol_count`` before calling base ``__init__`` method.
    """

    length: int | None
    requested_entropy: str
    rng: random.Random
    @property
    @abstractmethod
    def symbol_count(self) -> int:
        """The type of the None singleton."""

    def __init__(self, entropy: int | None = None, length: int | None = None, rng: random.Random | None = None) -> None: ...
    @property
    def entropy_per_symbol(self) -> float:
        """
        Average entropy per symbol (assuming all symbols have equal probability)
        """

    @property
    def entropy(self) -> float:
        """
        Effective entropy of generated passwords.

        This value will always be a multiple of :attr:`entropy_per_symbol`.
        If entropy is specified in constructor, :attr:`length` will be chosen so
        so that this value is the smallest multiple >= :attr:`requested_entropy`.
        """

    def __next__(self) -> str:
        """main generation function, should create one password/phrase"""

    @overload
    def __call__(self, returns: None = None) -> str:
        """
        frontend used by genword() / genphrase() to create passwords
        """

    @overload
    def __call__(self, returns: int) -> list[str]: ...
    @overload
    def __call__(self, returns: Callable[[Any], Iterator[Any]]) -> Iterator[str]: ...  # "returns" must be the "iter" builtin
    def __iter__(self) -> Self: ...

_Charset: TypeAlias = Literal["ascii_72", "ascii_62", "ascii_50", "hex"]
default_charsets: Final[dict[_Charset, str]]

class WordGenerator(SequenceGenerator):
    """
    Class which generates passwords by randomly choosing from a string of unique characters.

    Parameters
    ----------
    :param chars:
        custom character string to draw from.

    :param charset:
        predefined charset to draw from.

    :param \\*\\*kwds:
        all other keywords passed to the :class:`SequenceGenerator` parent class.

    Attributes
    ----------
    .. autoattribute:: chars
    .. autoattribute:: charset
    .. autoattribute:: default_charsets
    """

    charset: _Charset
    chars: str | bytes | None
    def __init__(
        self,
        chars: str | bytes | None = None,
        charset: _Charset | None = None,
        *,
        entropy: int | None = None,
        length: int | None = None,
        rng: random.Random | None = None,
    ) -> None: ...
    @property
    def symbol_count(self) -> int: ...

@overload
def genword(
    entropy: int | None = None,
    length: int | None = None,
    returns: None = None,
    *,
    chars: str | None = None,
    charset: _Charset | None = None,
    rng: random.Random | None = None,
) -> str:
    """Generate one or more random passwords.

    This function uses :mod:`random.SystemRandom` to generate
    one or more passwords using various character sets.
    The complexity of the password can be specified
    by size, or by the desired amount of entropy.

    Usage Example::

        >>> # generate a random alphanumeric string with 48 bits of entropy (the default)
        >>> from passlib import pwd
        >>> pwd.genword()
        'DnBHvDjMK6'

        >>> # generate a random hexadecimal string with 52 bits of entropy
        >>> pwd.genword(entropy=52, charset="hex")
        '310f1a7ac793f'

    :param entropy:
        Strength of resulting password, measured in 'guessing entropy' bits.
        An appropriate **length** value will be calculated
        based on the requested entropy amount, and the size of the character set.

        This can be a positive integer, or one of the following preset
        strings: ``"weak"`` (24), ``"fair"`` (36),
        ``"strong"`` (48), and ``"secure"`` (56).

        If neither this or **length** is specified, **entropy** will default
        to ``"strong"`` (48).

    :param length:
        Size of resulting password, measured in characters.
        If omitted, the size is auto-calculated based on the **entropy** parameter.

        If both **entropy** and **length** are specified,
        the stronger value will be used.

    :param returns:
        Controls what this function returns:

        * If ``None`` (the default), this function will generate a single password.
        * If an integer, this function will return a list containing that many passwords.
        * If the ``iter`` constant, will return an iterator that yields passwords.

    :param chars:

        Optionally specify custom string of characters to use when randomly
        generating a password. This option cannot be combined with **charset**.

    :param charset:

        The predefined character set to draw from (if not specified by **chars**).
        There are currently four presets available:

        * ``"ascii_62"`` (the default) -- all digits and ascii upper & lowercase letters.
          Provides ~5.95 entropy per character.

        * ``"ascii_50"`` -- subset which excludes visually similar characters
          (``1IiLl0Oo5S8B``). Provides ~5.64 entropy per character.

        * ``"ascii_72"`` -- all digits and ascii upper & lowercase letters,
          as well as some punctuation. Provides ~6.17 entropy per character.

        * ``"hex"`` -- Lower case hexadecimal.  Providers 4 bits of entropy per character.

    :returns:
        :class:`!unicode` string containing randomly generated password;
        or list of 1+ passwords if :samp:`returns={int}` is specified.
    """

@overload
def genword(
    returns: int,
    entropy: int | None = None,
    length: int | None = None,
    *,
    chars: str | None = None,
    charset: _Charset | None = None,
    rng: random.Random | None = None,
) -> list[str]: ...
@overload
def genword(
    returns: Callable[[Any], Iterator[Any]],
    entropy: int | None = None,
    length: int | None = None,
    *,
    chars: str | None = None,
    charset: _Charset | None = None,
    rng: random.Random | None = None,
) -> Iterator[str]: ...

class WordsetDict(MutableMapping[Any, Any]):
    """
    Special mapping used to store dictionary of wordsets.
    Different from a regular dict in that some wordsets
    may be lazy-loaded from an asset path.
    """

    paths: dict[str, str] | None
    def __init__(self, *args, **kwds) -> None: ...
    def __getitem__(self, key: str) -> tuple[str | bytes, ...]: ...
    def set_path(self, key: str, path: str) -> None:
        """
        set asset path to lazy-load wordset from.
        """

    def __setitem__(self, key: str, value: tuple[str | bytes, ...]) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...

default_wordsets: WordsetDict
_Wordset: TypeAlias = Literal["eff_long", "eff_short", "eff_prefixed", "bip39"]

class PhraseGenerator(SequenceGenerator):
    """class which generates passphrases by randomly choosing
    from a list of unique words.

    :param wordset:
        wordset to draw from.
    :param preset:
        name of preset wordlist to use instead of ``wordset``.
    :param spaces:
        whether to insert spaces between words in output (defaults to ``True``).
    :param \\*\\*kwds:
        all other keywords passed to the :class:`SequenceGenerator` parent class.

    .. autoattribute:: wordset
    """

    wordset: _Wordset
    words: Sequence[str | bytes] | None
    sep: str | None
    def __init__(
        self,
        wordset: _Wordset | None = None,
        words: Sequence[str | bytes] | None = None,
        sep: str | bytes | None = None,
        *,
        entropy: int | None = None,
        length: int | None = None,
        rng: random.Random | None = None,
    ) -> None: ...
    @property
    def symbol_count(self) -> int: ...

@overload
def genphrase(
    entropy: int | None = None,
    length: int | None = None,
    returns: None = None,
    *,
    wordset: _Wordset | None = None,
    words: Sequence[str | bytes] | None = None,
    sep: str | bytes | None = None,
    rng: random.Random | None = None,
) -> str:
    """Generate one or more random password / passphrases.

    This function uses :mod:`random.SystemRandom` to generate
    one or more passwords; it can be configured to generate
    alphanumeric passwords, or full english phrases.
    The complexity of the password can be specified
    by size, or by the desired amount of entropy.

    Usage Example::

        >>> # generate random phrase with 48 bits of entropy
        >>> from passlib import pwd
        >>> pwd.genphrase()
        'gangly robbing salt shove'

        >>> # generate a random phrase with 52 bits of entropy
        >>> # using a particular wordset
        >>> pwd.genword(entropy=52, wordset="bip39")
        'wheat dilemma reward rescue diary'

    :param entropy:
        Strength of resulting password, measured in 'guessing entropy' bits.
        An appropriate **length** value will be calculated
        based on the requested entropy amount, and the size of the word set.

        This can be a positive integer, or one of the following preset
        strings: ``"weak"`` (24), ``"fair"`` (36),
        ``"strong"`` (48), and ``"secure"`` (56).

        If neither this or **length** is specified, **entropy** will default
        to ``"strong"`` (48).

    :param length:
        Length of resulting password, measured in words.
        If omitted, the size is auto-calculated based on the **entropy** parameter.

        If both **entropy** and **length** are specified,
        the stronger value will be used.

    :param returns:
        Controls what this function returns:

        * If ``None`` (the default), this function will generate a single password.
        * If an integer, this function will return a list containing that many passwords.
        * If the ``iter`` builtin, will return an iterator that yields passwords.

    :param words:

        Optionally specifies a list/set of words to use when randomly generating a passphrase.
        This option cannot be combined with **wordset**.

    :param wordset:

        The predefined word set to draw from (if not specified by **words**).
        There are currently four presets available:

        ``"eff_long"`` (the default)

            Wordset containing 7776 english words of ~7 letters.
            Constructed by the EFF, it offers ~12.9 bits of entropy per word.

            This wordset (and the other ``"eff_"`` wordsets)
            were `created by the EFF <https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases>`_
            to aid in generating passwords.  See their announcement page
            for more details about the design & properties of these wordsets.

        ``"eff_short"``

            Wordset containing 1296 english words of ~4.5 letters.
            Constructed by the EFF, it offers ~10.3 bits of entropy per word.

        ``"eff_prefixed"``

            Wordset containing 1296 english words of ~8 letters,
            selected so that they each have a unique 3-character prefix.
            Constructed by the EFF, it offers ~10.3 bits of entropy per word.

        ``"bip39"``

            Wordset of 2048 english words of ~5 letters,
            selected so that they each have a unique 4-character prefix.
            Published as part of Bitcoin's `BIP 39 <https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt>`_,
            this wordset has exactly 11 bits of entropy per word.

            This list offers words that are typically shorter than ``"eff_long"``
            (at the cost of slightly less entropy); and much shorter than
            ``"eff_prefixed"`` (at the cost of a longer unique prefix).

    :param sep:
        Optional separator to use when joining words.
        Defaults to ``" "`` (a space), but can be an empty string, a hyphen, etc.

    :returns:
        :class:`!unicode` string containing randomly generated passphrase;
        or list of 1+ passphrases if :samp:`returns={int}` is specified.
    """

@overload
def genphrase(
    returns: int,
    entropy: int | None = None,
    length: int | None = None,
    *,
    wordset: _Wordset | None = None,
    words: Sequence[str | bytes] | None = None,
    sep: str | bytes | None = None,
    rng: random.Random | None = None,
) -> list[str]: ...
@overload
def genphrase(
    returns: Callable[[Any], Iterator[Any]],
    entropy: int | None = None,
    length: int | None = None,
    *,
    wordset: _Wordset | None = None,
    words: Sequence[str | bytes] | None = None,
    sep: str | bytes | None = None,
    rng: random.Random | None = None,
) -> Iterator[str]: ...

__all__ = ["genword", "default_charsets", "genphrase", "default_wordsets"]
