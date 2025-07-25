from typing_extensions import Self

__tracebackhide__: bool

class SnapshotMixin:
    """Snapshot mixin.

    Take a snapshot of a python data structure, store it on disk in JSON format, and automatically
    compare the latest data to the stored data on every test run.

    Functional testing (which snapshot testing falls under) is very much blackbox testing.  When
    something goes wrong, it's hard to pinpoint the issue, because functional tests typically
    provide minimal *isolation* as compared to unit tests.  On the plus side, snapshots typically
    do provide enormous *leverage* as a few well-placed snapshot tests can strongly verify that an
    application is working.  Similar coverage would otherwise require dozens if not hundreds of
    unit tests.

    **On-disk Format**

    Snapshots are stored in a readable JSON format.  For example::

        assert_that({'a': 1, 'b': 2, 'c': 3}).snapshot()

    Would be stored as::

        {
            "a": 1,
            "b": 2,
            "c": 3
        }

    The JSON formatting support most python data structures (dict, list, object, etc), but not custom
    binary data.

    **Updating**

    It's easy to update your snapshots...just delete them all and re-run the test suite to regenerate all snapshots.

    Note:
        Snapshots require Python 3.x
    """

    def snapshot(self, id: str | None = None, path: str = "__snapshots") -> Self:
        """Asserts that val is identical to the on-disk snapshot stored previously.

        On the first run of a test before the snapshot file has been saved, a snapshot is created,
        stored to disk, and the test *always* passes.  But on all subsequent runs, val is compared
        to the on-disk snapshot, and the test fails if they don't match.

        Snapshot artifacts are stored in the ``__snapshots`` directory by default, and should be
        committed to source control alongside any code changes.

        Snapshots are identified by test filename plus line number by default.

        Args:
            id: the item or items expected to be contained
            path: the item or items expected to be contained

        Examples:
            Usage::

                assert_that(None).snapshot()
                assert_that(True).snapshot()
                assert_that(1).snapshot()
                assert_that(123.4).snapshot()
                assert_that('foo').snapshot()
                assert_that([1, 2, 3]).snapshot()
                assert_that({'a': 1, 'b': 2, 'c': 3}).snapshot()
                assert_that({'a', 'b', 'c'}).snapshot()
                assert_that(1 + 2j).snapshot()
                assert_that(someobj).snapshot()

            By default, snapshots are identified by test filename plus line number.  Alternately, you can specify a custom identifier using the ``id`` arg::

                assert_that({'a': 1, 'b': 2, 'c': 3}).snapshot(id='foo-id')


            By default, snapshots are stored in the ``__snapshots`` directory.  Alternately, you can specify a custom path using the ``path`` arg::

                assert_that({'a': 1, 'b': 2, 'c': 3}).snapshot(path='my-custom-folder')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** equal to on-disk snapshot
        """
