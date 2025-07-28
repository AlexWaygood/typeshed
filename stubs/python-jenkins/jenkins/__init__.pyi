"""
.. module:: jenkins
    :platform: Unix, Windows
    :synopsis: Python API to interact with Jenkins
    :noindex:

See examples at :doc:`examples`
"""

from _typeshed import Incomplete
from collections.abc import Mapping, MutableMapping, Sequence
from re import Pattern
from typing import Any, Final, Literal, overload
from typing_extensions import TypeAlias

import requests
from requests.models import Request, Response
from requests.sessions import _Auth

LAUNCHER_SSH: Final[str]
LAUNCHER_COMMAND: Final[str]
LAUNCHER_JNLP: Final[str]
LAUNCHER_WINDOWS_SERVICE: Final[str]
DEFAULT_HEADERS: Final[dict[str, str]]
DEFAULT_TIMEOUT: Final[float]
INFO: Final[str]
PLUGIN_INFO: Final[str]
CRUMB_URL: Final[str]
WHOAMI_URL: Final[str]
JOBS_QUERY: Final[str]
JOBS_QUERY_TREE: Final[str]
JOB_INFO: Final[str]
JOB_NAME: Final[str]
ALL_BUILDS: Final[str]
Q_INFO: Final[str]
Q_ITEM: Final[str]
CANCEL_QUEUE: Final[str]
CREATE_JOB: Final[str]
CONFIG_JOB: Final[str]
DELETE_JOB: Final[str]
ENABLE_JOB: Final[str]
DISABLE_JOB: Final[str]
CHECK_JENKINSFILE_SYNTAX: Final[str]
SET_JOB_BUILD_NUMBER: Final[str]
COPY_JOB: Final[str]
RENAME_JOB: Final[str]
BUILD_JOB: Final[str]
STOP_BUILD: Final[str]
BUILD_WITH_PARAMS_JOB: Final[str]
BUILD_INFO: Final[str]
BUILD_CONSOLE_OUTPUT: Final[str]
BUILD_ENV_VARS: Final[str]
BUILD_TEST_REPORT: Final[str]
BUILD_ARTIFACT: Final[str]
BUILD_STAGES: Final[str]
DELETE_BUILD: Final[str]
WIPEOUT_JOB_WORKSPACE: Final[str]
NODE_LIST: Final[str]
CREATE_NODE: Final[str]
DELETE_NODE: Final[str]
NODE_INFO: Final[str]
NODE_TYPE: Final[str]
TOGGLE_OFFLINE: Final[str]
CONFIG_NODE: Final[str]
VIEW_NAME: Final[str]
VIEW_JOBS: Final[str]
CREATE_VIEW: Final[str]
CONFIG_VIEW: Final[str]
DELETE_VIEW: Final[str]
SCRIPT_TEXT: Final[str]
NODE_SCRIPT_TEXT: Final[str]
PROMOTION_NAME: Final[str]
PROMOTION_INFO: Final[str]
DELETE_PROMOTION: Final[str]
CREATE_PROMOTION: Final[str]
CONFIG_PROMOTION: Final[str]
LIST_CREDENTIALS: Final[str]
CREATE_CREDENTIAL: Final[str]
CONFIG_CREDENTIAL: Final[str]
CREDENTIAL_INFO: Final[str]
QUIET_DOWN: Final[str]
EMPTY_CONFIG_XML: Final[str]
EMPTY_FOLDER_XML: Final[str]
RECONFIG_XML: Final[str]
EMPTY_VIEW_CONFIG_XML: Final[str]
EMPTY_PROMO_CONFIG_XML: Final[str]
PROMO_RECONFIG_XML: Final[str]

class JenkinsException(Exception):
    """General exception type for jenkins-API-related failures."""

class NotFoundException(JenkinsException):
    """A special exception to call out the case of receiving a 404."""

class EmptyResponseException(JenkinsException):
    """A special exception to call out the case receiving an empty response."""

class BadHTTPException(JenkinsException):
    """A special exception to call out the case of a broken HTTP response."""

class TimeoutException(JenkinsException):
    """A special exception to call out in the case of a socket timeout."""

class WrappedSession(requests.Session):
    """A wrapper for requests.Session to override 'verify' property, ignoring REQUESTS_CA_BUNDLE environment variable.

    This is a workaround for https://github.com/psf/requests/issues/3829 (will be fixed in requests 3.0.0)
    """

    # merge_environment_settings wraps requests.Session.merge_environment_settings
    # w/o changing the type signature
    ...

_JSONValue: TypeAlias = Any  # too many possibilities to express
_JSON: TypeAlias = dict[str, _JSONValue]

class Jenkins:
    server: str
    auth: _Auth | None
    crumb: Mapping[str, Incomplete] | bool | Incomplete
    timeout: int
    def __init__(self, url: str, username: str | None = None, password: str | None = None, timeout: int = ...) -> None:
        """Create handle to Jenkins instance.

        All methods will raise :class:`JenkinsException` on failure.

        :param url: URL of Jenkins server, ``str``
        :param username: Server username, ``str``
        :param password: Server password, ``str``
        :param timeout: Server connection timeout in secs (default: not set), ``int``
        """

    def maybe_add_crumb(self, req: Request) -> None: ...
    def get_job_info(self, name: str, depth: int = 0, fetch_all_builds: bool = False) -> _JSON:
        """Get job information dictionary.

        :param name: Job name, ``str``
        :param depth: JSON depth, ``int``
        :param fetch_all_builds: If true, all builds will be retrieved
                                 from Jenkins. Otherwise, Jenkins will
                                 only return the most recent 100
                                 builds. This comes at the expense of
                                 an additional API call which may
                                 return significant amounts of
                                 data. ``bool``
        :returns: dictionary of job information
        """

    def get_job_info_regex(
        self, pattern: str | Pattern[str], depth: int = 0, folder_depth: int = 0, folder_depth_per_request: int = 10
    ) -> list[_JSON]:
        """Get a list of jobs information that contain names which match the
           regex pattern.

        :param pattern: regex pattern, ``str``
        :param depth: JSON depth, ``int``
        :param folder_depth: folder level depth to search ``int``
        :param folder_depth_per_request: Number of levels to fetch at once,
            ``int``. See :func:`get_all_jobs`.
        :returns: List of jobs info, ``list``
        """

    def get_job_name(self, name: str) -> str | None:
        """Return the name of a job using the API.

        That is roughly an identity method which can be used to quickly verify
        a job exists or is accessible without causing too much stress on the
        server side.

        :param name: Job name, ``str``
        :returns: Name of job or None
        """

    def debug_job_info(self, job_name: str) -> None:
        """Print out job info in more readable format."""

    def jenkins_open(self, req: Request, add_crumb: bool = True, resolve_auth: bool = True) -> str:
        """Return the HTTP response body from a ``requests.Request``.

        :returns: ``str``
        """

    def jenkins_open_stream(self, req: Request, add_crumb: bool = True, resolve_auth: bool = True) -> Response:
        """Return the HTTP response body from a ``requests.Request``.

        :returns: ``stream``
        """

    def jenkins_request(
        self, req: Request, add_crumb: bool = True, resolve_auth: bool = True, stream: bool | None = None
    ) -> Response:
        """Utility routine for opening an HTTP request to a Jenkins server.

        :param req: A ``requests.Request`` to submit.
        :param add_crumb: If True, try to add a crumb header to this ``req``
                          before submitting. Defaults to ``True``.
        :param resolve_auth: If True, maybe add authentication. Defaults to
                             ``True``.
        :param stream: If True, return a stream
        :returns: A ``requests.Response`` object.
        """

    def get_queue_item(self, number: int, depth: int = 0) -> _JSON:
        """Get information about a queued item (to-be-created job).

        The returned dict will have a "why" key if the queued item is still
        waiting for an executor.

        The returned dict will have an "executable" key if the queued item is
        running on an executor, or has completed running. Use this to
        determine the job number / URL.

        :param name: queue number, ``int``
        :returns: dictionary of queued information, ``dict``
        """

    def get_build_info(self, name: str, number: int, depth: int = 0) -> _JSON:
        """Get build information dictionary.

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :param depth: JSON depth, ``int``
        :returns: dictionary of build information, ``dict``

        Example::

            >>> next_build_number = server.get_job_info('build_name')['nextBuildNumber']
            >>> output = server.build_job('build_name')
            >>> from time import sleep; sleep(10)
            >>> build_info = server.get_build_info('build_name', next_build_number)
            >>> print(build_info)
            {u'building': False, u'changeSet': {u'items': [{u'date': u'2011-12-19T18:01:52.540557Z', u'msg': u'test', u'revision': 66, u'user': u'unknown', u'paths': [{u'editType': u'edit', u'file': u'/branches/demo/index.html'}]}], u'kind': u'svn', u'revisions': [{u'module': u'http://eaas-svn01.i3.level3.com/eaas', u'revision': 66}]}, u'builtOn': u'', u'description': None, u'artifacts': [{u'relativePath': u'dist/eaas-87-2011-12-19_18-01-57.war', u'displayPath': u'eaas-87-2011-12-19_18-01-57.war', u'fileName': u'eaas-87-2011-12-19_18-01-57.war'}, {u'relativePath': u'dist/eaas-87-2011-12-19_18-01-57.war.zip', u'displayPath': u'eaas-87-2011-12-19_18-01-57.war.zip', u'fileName': u'eaas-87-2011-12-19_18-01-57.war.zip'}], u'timestamp': 1324317717000, u'number': 87, u'actions': [{u'parameters': [{u'name': u'SERVICE_NAME', u'value': u'eaas'}, {u'name': u'PROJECT_NAME', u'value': u'demo'}]}, {u'causes': [{u'userName': u'anonymous', u'shortDescription': u'Started by user anonymous'}]}, {}, {}, {}], u'id': u'2011-12-19_18-01-57', u'keepLog': False, u'url': u'http://eaas-jenkins01.i3.level3.com:9080/job/build_war/87/', u'culprits': [{u'absoluteUrl': u'http://eaas-jenkins01.i3.level3.com:9080/user/unknown', u'fullName': u'unknown'}], u'result': u'SUCCESS', u'duration': 8826, u'fullDisplayName': u'build_war #87'}
        """

    def get_build_env_vars(self, name: str, number: int, depth: int = 0) -> _JSON | None:
        """Get build environment variables.

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :param depth: JSON depth, ``int``
        :returns: dictionary of build env vars, ``dict`` or None for workflow jobs,
            or if InjectEnvVars plugin not installed
        """

    def get_build_test_report(self, name: str, number: int, depth: int = 0) -> _JSON | None:
        """Get test results report.

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :returns: dictionary of test report results, ``dict`` or None if there is no Test Report
        """

    def get_build_artifact(self, name: str, number: int, artifact: str) -> _JSON:
        """Get artifacts from job

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :param artifact: Artifact relative path, ``str``
        :returns: artifact to download, ``dict``
        """

    def get_build_artifact_as_bytes(self, name: str, number: int, artifact: str) -> bytes:
        """Get artifacts from job

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :param artifact: Artifact relative path, ``str``
        :returns: artifact to download, ``bytes``
        """

    def get_build_stages(self, name: str, number: int) -> _JSON:
        """Get stages info from job

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :returns: dictionary of stages in the job, ``dict``
        """

    def get_queue_info(self) -> _JSON:
        """:returns: list of job dictionaries, ``[dict]``

        Example::
            >>> queue_info = server.get_queue_info()
            >>> print(queue_info[0])
            {u'task': {u'url': u'http://your_url/job/my_job/', u'color': u'aborted_anime', u'name': u'my_job'}, u'stuck': False, u'actions': [{u'causes': [{u'shortDescription': u'Started by timer'}]}], u'buildable': False, u'params': u'', u'buildableStartMilliseconds': 1315087293316, u'why': u'Build #2,532 is already in progress (ETA:10 min)', u'blocked': True}
        """

    def cancel_queue(self, id: int) -> None:
        """Cancel a queued build.

        :param id: Jenkins job id number for the build, ``int``
        """

    def get_info(self, item: str = "", query: str | None = None) -> _JSON:
        """Get information on this Master or item on Master.

        This information includes job list and view information and can be
        used to retreive information on items such as job folders.

        :param item: item to get information about on this Master
        :param query: xpath to extract information about on this Master
        :returns: dictionary of information about Master or item, ``dict``

        Example::

            >>> info = server.get_info()
            >>> jobs = info['jobs']
            >>> print(jobs[0])
            {u'url': u'http://your_url_here/job/my_job/', u'color': u'blue',
            u'name': u'my_job'}

        """

    def get_whoami(self, depth: int = 0) -> _JSON:
        """Get information about the user account that authenticated to
        Jenkins. This is a simple way to verify that your credentials are
        correct.

        :returns: Information about the current user ``dict``

        Example::

            >>> me = server.get_whoami()
            >>> print me['fullName']
            >>> 'John'

        """

    def get_version(self) -> str:
        """Get the version of this Master.

        :returns: This master's version number ``str``

        Example::

            >>> info = server.get_version()
            >>> print info
            >>> 1.541

        """

    def get_plugins_info(self, depth: int = 2) -> _JSON:
        """Get all installed plugins information on this Master.

        This method retrieves information about each plugin that is installed
        on master returning the raw plugin data in a JSON format.

        .. deprecated:: 0.4.9
           Use :func:`get_plugins` instead.

        :param depth: JSON depth, ``int``
        :returns: info on all plugins ``[dict]``

        Example::

            >>> info = server.get_plugins_info()
            >>> print(info)
            [{u'backupVersion': None, u'version': u'0.0.4', u'deleted': False,
            u'supportsDynamicLoad': u'MAYBE', u'hasUpdate': True,
            u'enabled': True, u'pinned': False, u'downgradable': False,
            u'dependencies': [], u'url':
            u'http://wiki.jenkins-ci.org/display/JENKINS/Gearman+Plugin',
            u'longName': u'Gearman Plugin', u'active': True, u'shortName':
            u'gearman-plugin', u'bundled': False}, ..]

        """

    def get_plugin_info(self, name: str, depth: int = 2) -> _JSON:
        """Get an installed plugin information on this Master.

        This method retrieves information about a specific plugin and returns
        the raw plugin data in a JSON format.
        The passed in plugin name (short or long) must be an exact match.

        .. note:: Calling this method will query Jenkins fresh for the
            information for all plugins on each call. If you need to retrieve
            information for multiple plugins it's recommended to use
            :func:`get_plugins` instead, which will return a multi key
            dictionary that can be accessed via either the short or long name
            of the plugin.

        :param name: Name (short or long) of plugin, ``str``
        :param depth: JSON depth, ``int``
        :returns: a specific plugin ``dict``

        Example::

            >>> info = server.get_plugin_info("Gearman Plugin")
            >>> print(info)
            {u'backupVersion': None, u'version': u'0.0.4', u'deleted': False,
            u'supportsDynamicLoad': u'MAYBE', u'hasUpdate': True,
            u'enabled': True, u'pinned': False, u'downgradable': False,
            u'dependencies': [], u'url':
            u'http://wiki.jenkins-ci.org/display/JENKINS/Gearman+Plugin',
            u'longName': u'Gearman Plugin', u'active': True, u'shortName':
            u'gearman-plugin', u'bundled': False}

        """

    def get_plugins(self, depth: int = 2) -> _JSON:
        """Return plugins info using helper class for version comparison

        This method retrieves information about all the installed plugins and
        uses a Plugin helper class to simplify version comparison. Also uses
        a multi key dict to allow retrieval via either short or long names.

        When printing/dumping the data, the version will transparently return
        a unicode string, which is exactly what was previously returned by the
        API.

        :param depth: JSON depth, ``int``
        :returns: info on all plugins ``[dict]``

        Example::

            >>> j = Jenkins()
            >>> info = j.get_plugins()
            >>> print(info)
            {('gearman-plugin', 'Gearman Plugin'):
              {u'backupVersion': None, u'version': u'0.0.4',
               u'deleted': False, u'supportsDynamicLoad': u'MAYBE',
               u'hasUpdate': True, u'enabled': True, u'pinned': False,
               u'downgradable': False, u'dependencies': [], u'url':
               u'http://wiki.jenkins-ci.org/display/JENKINS/Gearman+Plugin',
               u'longName': u'Gearman Plugin', u'active': True, u'shortName':
               u'gearman-plugin', u'bundled': False}, ...}

        """

    def get_jobs(
        self, folder_depth: int = 0, folder_depth_per_request: int = 10, view_name: str | None = None
    ) -> list[dict[str, str]]:
        """Get list of jobs.

        Each job is a dictionary with 'name', 'url', 'color' and 'fullname'
        keys.

        If the ``view_name`` parameter is present, the list of
        jobs will be limited to only those configured in the
        specified view. In this case, the job dictionary 'fullname' key
        would be equal to the job name.

        :param folder_depth: Number of levels to search, ``int``. By default
            0, which will limit search to toplevel. None disables the limit.
        :param folder_depth_per_request: Number of levels to fetch at once,
            ``int``. See :func:`get_all_jobs`.
        :param view_name: Name of a Jenkins view for which to
            retrieve jobs, ``str``. By default, the job list is
            not limited to a specific view.
        :returns: list of jobs, ``[{str: str, str: str, str: str, str: str}]``

        Example::

            >>> jobs = server.get_jobs()
            >>> print(jobs)
            [{
                u'name': u'all_tests',
                u'url': u'http://your_url.here/job/all_tests/',
                u'color': u'blue',
                u'fullname': u'all_tests'
            }]

        """

    def get_all_jobs(self, folder_depth: int | None = None, folder_depth_per_request: int = 10) -> list[dict[str, str]]:
        """Get list of all jobs recursively to the given folder depth.

        Each job is a dictionary with 'name', 'url', 'color' and 'fullname'
        keys.

        :param folder_depth: Number of levels to search, ``int``. By default
            None, which will search all levels. 0 limits to toplevel.
        :param folder_depth_per_request: Number of levels to fetch at once,
            ``int``. By default 10, which is usually enough to fetch all jobs
            using a single request and still easily fits into an HTTP request.
        :returns: list of jobs, ``[ { str: str} ]``

        .. note::

            On instances with many folders it would not be efficient to fetch
            each folder separately, hence `folder_depth_per_request` levels
            are fetched at once using the ``tree`` query parameter::

                ?tree=jobs[url,color,name,jobs[...,jobs[...,jobs[...,jobs]]]]

            If there are more folder levels than the query asks for, Jenkins
            returns empty [#]_ objects at the deepest level::

                {"name": "folder", "url": "...", "jobs": [{}, {}, ...]}

            This makes it possible to detect when additional requests are
            needed.

            .. [#] Actually recent Jenkins includes a ``_class`` field
                everywhere, but it's missing the requested fields.
        """

    def copy_job(self, from_name: str, to_name: str) -> None:
        """Copy a Jenkins job.

        Will raise an exception whenever the source and destination folder
        for this jobs won't be the same.

        :param from_name: Name of Jenkins job to copy from, ``str``
        :param to_name: Name of Jenkins job to copy to, ``str``
        :throws: :class:`JenkinsException` whenever the source and destination
            folder are not the same
        """

    def rename_job(self, from_name: str, to_name: str) -> None:
        """Rename an existing Jenkins job

        Will raise an exception whenever the source and destination folder
        for this jobs won't be the same.

        :param from_name: Name of Jenkins job to rename, ``str``
        :param to_name: New Jenkins job name, ``str``
        :throws: :class:`JenkinsException` whenever the source and destination
            folder are not the same
        """

    def delete_job(self, name: str) -> None:
        """Delete Jenkins job permanently.

        :param name: Name of Jenkins job, ``str``
        """

    def enable_job(self, name: str) -> None:
        """Enable Jenkins job.

        :param name: Name of Jenkins job, ``str``
        """

    def disable_job(self, name: str) -> None:
        """Disable Jenkins job.

        To re-enable, call :meth:`Jenkins.enable_job`.

        :param name: Name of Jenkins job, ``str``
        """

    def set_next_build_number(self, name: str, number: int) -> None:
        """Set a job's next build number.

        The current next build number is contained within the job
        information retrieved using :meth:`Jenkins.get_job_info`.  If
        the specified next build number is less than the last build
        number, Jenkins will ignore the request.

        Note that the `Next Build Number Plugin
        <https://wiki.jenkins-ci.org/display/JENKINS/Next+Build+Number+Plugin>`_
        must be installed to enable this functionality.

        :param name: Name of Jenkins job, ``str``
        :param number: Next build number to set, ``int``

        Example::

            >>> next_bn = server.get_job_info('job_name')['nextBuildNumber']
            >>> server.set_next_build_number('job_name', next_bn + 50)
        """

    def job_exists(self, name: str) -> bool:
        """Check whether a job exists

        :param name: Name of Jenkins job, ``str``
        :returns: ``True`` if Jenkins job exists
        """

    def jobs_count(self) -> int:
        """Get the number of jobs on the Jenkins server

        :returns: Total number of jobs, ``int``
        """

    def assert_job_exists(self, name: str, exception_message: str = "job[%s] does not exist") -> None:
        """Raise an exception if a job does not exist

        :param name: Name of Jenkins job, ``str``
        :param exception_message: Message to use for the exception. Formatted
                                  with ``name``
        :throws: :class:`JenkinsException` whenever the job does not exist
        """

    def create_folder(self, folder_name: str, ignore_failures: bool = False) -> None:
        """Create a new Jenkins folder

        :param folder_name: Name of Jenkins Folder, ``str``
        :param ignore_failures: if True, don't raise if it was not possible to create the folder, ``bool``
        """

    def upsert_job(self, name: str, config_xml: str) -> None:
        """Create a new Jenkins job or reconfigures it if it exists

        :param name: Name of Jenkins job, ``str``
        :param config_xml: config file text, ``str``
        """

    def check_jenkinsfile_syntax(self, jenkinsfile: str) -> list[str]:
        """Checks if a Pipeline Jenkinsfile has a valid syntax

        :param jenkinsfile: Jenkinsfile text, ``str``
        :returns: List of errors in the Jenkinsfile. Empty list if no errors.
        """

    def create_job(self, name: str, config_xml: str) -> None:
        """Create a new Jenkins job

        :param name: Name of Jenkins job, ``str``
        :param config_xml: config file text, ``str``
        """

    def get_job_config(self, name: str) -> str:
        """Get configuration of existing Jenkins job.

        :param name: Name of Jenkins job, ``str``
        :returns: job configuration (XML format)
        """

    def reconfig_job(self, name: str, config_xml: str) -> None:
        """Change configuration of existing Jenkins job.

        To create a new job, see :meth:`Jenkins.create_job`.

        :param name: Name of Jenkins job, ``str``
        :param config_xml: New XML configuration, ``str``
        """

    @overload
    def build_job_url(
        self,
        name: str,
        parameters: Mapping[str, Incomplete] | Sequence[tuple[str, Incomplete]] | None = None,
        token: Literal[""] | None = None,
    ) -> str:
        """Get URL to trigger build job.

        Authenticated setups may require configuring a token on the server
        side.

        Use ``list of two membered tuples`` to supply parameters with multi
        select options.

        :param name: Name of Jenkins job, ``str``
        :param parameters: parameters for job, or None., ``dict`` or
            ``list of two membered tuples``
        :param token: (optional) token for building job, ``str``
        :returns: URL for building job
        """

    @overload
    def build_job_url(
        self, name: str, parameters: dict[str, Incomplete] | list[tuple[str, Incomplete]] | None, token: str
    ) -> str: ...
    @overload
    def build_job_url(
        self, name: str, parameters: dict[str, Incomplete] | list[tuple[str, Incomplete]] | None = None, *, token: str
    ) -> str: ...
    @overload
    def build_job(
        self,
        name: str,
        parameters: Mapping[str, Incomplete] | Sequence[tuple[str, Incomplete]] | None = None,
        token: Literal[""] | None = None,
    ) -> int:
        """Trigger build job.

        This method returns a queue item number that you can pass to
        :meth:`Jenkins.get_queue_item`. Note that this queue number is only
        valid for about five minutes after the job completes, so you should
        get/poll the queue information as soon as possible to determine the
        job's URL.

        :param name: name of job
        :param parameters: parameters for job, or ``None``, ``dict``
        :param token: Jenkins API token
        :returns: ``int`` queue item
        """

    @overload
    def build_job(
        self, name: str, parameters: dict[str, Incomplete] | list[tuple[str, Incomplete]] | None, token: str
    ) -> int: ...
    @overload
    def build_job(
        self, name: str, parameters: dict[str, Incomplete] | list[tuple[str, Incomplete]] | None = None, *, token: str
    ) -> int: ...
    def run_script(self, script: str, node: str | None = None) -> str:
        """Execute a groovy script on the jenkins master or on a node if
        specified..

        :param script: The groovy script, ``string``
        :param node: Node to run the script on, defaults to None (master).
        :returns: The result of the script run.

        Example::
            >>> info = server.run_script("println(Jenkins.instance.pluginManager.plugins)")
            >>> print(info)
            u'[Plugin:windows-slaves, Plugin:ssh-slaves, Plugin:translation,
            Plugin:cvs, Plugin:nodelabelparameter, Plugin:external-monitor-job,
            Plugin:mailer, Plugin:jquery, Plugin:antisamy-markup-formatter,
            Plugin:maven-plugin, Plugin:pam-auth]'
        """

    def install_plugin(self, name: str, include_dependencies: bool = True) -> bool:
        """Install a plugin and its dependencies from the Jenkins public
        repository at http://repo.jenkins-ci.org/repo/org/jenkins-ci/plugins

        :param name: The plugin short name, ``string``
        :param include_dependencies: Install the plugin's dependencies, ``bool``
        :returns: Whether a Jenkins restart is required, ``bool``

        Example::
            >>> info = server.install_plugin("jabber")
            >>> print(info)
            True
        """

    def stop_build(self, name: str, number: int) -> None:
        """Stop a running Jenkins build.

        :param name: Name of Jenkins job, ``str``
        :param number: Jenkins build number for the job, ``int``
        """

    def delete_build(self, name: str, number: int) -> None:
        """Delete a Jenkins build.

        :param name: Name of Jenkins job, ``str``
        :param number: Jenkins build number for the job, ``int``
        """

    def wipeout_job_workspace(self, name: str) -> None:
        """Wipe out workspace for given Jenkins job.

        :param name: Name of Jenkins job, ``str``
        """

    def get_running_builds(self) -> list[_JSON]:
        """Return list of running builds.

        Each build is a dict with keys 'name', 'number', 'url', 'node',
        and 'executor'.

        :returns: List of builds,
          ``[ { str: str, str: int, str:str, str: str, str: int} ]``

        Example::
            >>> builds = server.get_running_builds()
            >>> print(builds)
            [{'node': 'foo-slave', 'url': 'https://localhost/job/test/15/',
              'executor': 0, 'name': 'test', 'number': 15}]
        """

    def get_nodes(self, depth: int = 0) -> list[_JSON]:
        """Get a list of nodes connected to the Master

        Each node is a dict with keys 'name' and 'offline'

        :returns: List of nodes, ``[ { str: str, str: bool} ]``
        """

    def get_node_info(self, name: str, depth: int = 0) -> _JSON:
        """Get node information dictionary

        :param name: Node name, ``str``
        :param depth: JSON depth, ``int``
        :returns: Dictionary of node info, ``dict``
        """

    def node_exists(self, name: str) -> bool:
        """Check whether a node exists

        :param name: Name of Jenkins node, ``str``
        :returns: ``True`` if Jenkins node exists
        """

    def assert_node_exists(self, name: str, exception_message: str = "node[%s] does not exist") -> None:
        """Raise an exception if a node does not exist

        :param name: Name of Jenkins node, ``str``
        :param exception_message: Message to use for the exception. Formatted
                                  with ``name``
        :throws: :class:`JenkinsException` whenever the node does not exist
        """

    def delete_node(self, name: str) -> None:
        """Delete Jenkins node permanently.

        :param name: Name of Jenkins node, ``str``
        """

    def disable_node(self, name: str, msg: str = "") -> None:
        """Disable a node

        :param name: Jenkins node name, ``str``
        :param msg: Offline message, ``str``
        """

    def enable_node(self, name: str) -> None:
        """Enable a node

        :param name: Jenkins node name, ``str``
        """

    def create_node(
        self,
        name: str,
        numExecutors: int = 2,
        nodeDescription: str | None = None,
        remoteFS: str = "/var/lib/jenkins",
        labels: str | None = None,
        exclusive: bool = False,
        launcher: str = "hudson.slaves.CommandLauncher",
        launcher_params: MutableMapping[str, Incomplete] = {},
    ) -> None:
        """Create a node

        :param name: name of node to create, ``str``
        :param numExecutors: number of executors for node, ``int``
        :param nodeDescription: Description of node, ``str``
        :param remoteFS: Remote filesystem location to use, ``str``
        :param labels: Labels to associate with node, ``str``
        :param exclusive: Use this node for tied jobs only, ``bool``
        :param launcher: The launch method for the slave, ``jenkins.LAUNCHER_COMMAND``,         ``jenkins.LAUNCHER_SSH``, ``jenkins.LAUNCHER_JNLP``, ``jenkins.LAUNCHER_WINDOWS_SERVICE``
        :param launcher_params: Additional parameters for the launcher, ``dict``
        """

    def get_node_config(self, name: str) -> str:
        """Get the configuration for a node.

        :param name: Jenkins node name, ``str``
        """

    def reconfig_node(self, name: str, config_xml: str) -> None:
        """Change the configuration for an existing node.

        :param name: Jenkins node name, ``str``
        :param config_xml: New XML configuration, ``str``
        """

    def get_build_console_output(self, name: str, number: int) -> str:
        """Get build console text.

        :param name: Job name, ``str``
        :param number: Build number, ``str`` (also accepts ``int``)
        :returns: Build console output,  ``str``
        """

    def get_view_name(self, name: str) -> str | None:
        """Return the name of a view using the API.

        That is roughly an identity method which can be used to quickly verify
        a view exists or is accessible without causing too much stress on the
        server side.

        :param name: View name, ``str``
        :returns: Name of view or None
        """

    def assert_view_exists(self, name: str, exception_message: str = "view[%s] does not exist") -> None:
        """Raise an exception if a view does not exist

        :param name: Name of Jenkins view, ``str``
        :param exception_message: Message to use for the exception. Formatted
                                  with ``name``
        :throws: :class:`JenkinsException` whenever the view does not exist
        """

    def view_exists(self, name: str) -> bool:
        """Check whether a view exists

        :param name: Name of Jenkins view, ``str``
        :returns: ``True`` if Jenkins view exists
        """

    def get_views(self) -> list[_JSON]:
        """Get list of views running.

        Each view is a dictionary with 'name' and 'url' keys.

        :returns: list of views, ``[ { str: str} ]``
        """

    def delete_view(self, name: str) -> None:
        """Delete Jenkins view permanently.

        :param name: Name of Jenkins view, ``str``
        """

    def create_view(self, name: str, config_xml: str) -> None:
        """Create a new Jenkins view

        :param name: Name of Jenkins view, ``str``
        :param config_xml: config file text, ``str``
        """

    def reconfig_view(self, name: str, config_xml: str) -> None:
        """Change configuration of existing Jenkins view.

        To create a new view, see :meth:`Jenkins.create_view`.

        :param name: Name of Jenkins view, ``str``
        :param config_xml: New XML configuration, ``str``
        """

    def get_view_config(self, name: str) -> str:
        """Get configuration of existing Jenkins view.

        :param name: Name of Jenkins view, ``str``
        :returns: view configuration (XML format)
        """

    def get_promotion_name(self, name: str, job_name: str) -> str | None:
        """Return the name of a promotion using the API.

        That is roughly an identity method which can be used to
        quickly verify a promotion exists for a job or is accessible
        without causing too much stress on the server side.

        :param name: Promotion name, ``str``
        :param job_name: Job name, ``str``
        :returns: Name of promotion or None
        """

    def assert_promotion_exists(
        self, name: str, job_name: str, exception_message: str = "promotion[%s] does not exist for job[%s]"
    ) -> None:
        """Raise an exception if a job lacks a promotion

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        :param exception_message: Message to use for the exception. Formatted
                                  with ``name`` and ``job_name``
        :throws: :class:`JenkinsException` whenever the promotion
            does not exist on a job
        """

    def promotion_exists(self, name: str, job_name: str) -> bool:
        """Check whether a job has a certain promotion

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        :returns: ``True`` if Jenkins promotion exists
        """

    def get_promotions_info(self, job_name: str, depth: int = 0) -> _JSON:
        """Get promotion information dictionary of a job

        :param job_name: job_name, ``str``
        :param depth: JSON depth, ``int``
        :returns: Dictionary of promotion info, ``dict``
        """

    def get_promotions(self, job_name: str) -> list[_JSON]:
        """Get list of promotions running.

        Each promotion is a dictionary with 'name' and 'url' keys.

        :param job_name: Job name, ``str``
        :returns: list of promotions, ``[ { str: str} ]``
        """

    def delete_promotion(self, name: str, job_name: str) -> None:
        """Delete Jenkins promotion permanently.

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        """

    def create_promotion(self, name: str, job_name: str, config_xml: str) -> None:
        """Create a new Jenkins promotion

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        :param config_xml: config file text, ``str``
        """

    def reconfig_promotion(self, name: str, job_name: str, config_xml: str) -> None:
        """Change configuration of existing Jenkins promotion.

        To create a new promotion, see :meth:`Jenkins.create_promotion`.

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        :param config_xml: New XML configuration, ``str``
        """

    def get_promotion_config(self, name: str, job_name: str) -> str:
        """Get configuration of existing Jenkins promotion.

        :param name: Name of Jenkins promotion, ``str``
        :param job_name: Job name, ``str``
        :returns: promotion configuration (XML format)
        """

    def assert_folder(self, name: str, exception_message: str = "job[%s] is not a folder") -> None:
        """Raise an exception if job is not Cloudbees Folder

        :param name: Name of job, ``str``
        :param exception_message: Message to use for the exception.
        :throws: :class:`JenkinsException` whenever the job is
            not Cloudbees Folder
        """

    def is_folder(self, name: str) -> bool:
        """Check whether a job is Cloudbees Folder

        :param name: Job name, ``str``
        :returns: ``True`` if job is folder, ``False`` otherwise
        """

    def assert_credential_exists(
        self,
        name: str,
        folder_name: str,
        domain_name: str = "_",
        exception_message: str = "credential[%s] does not exist in the domain[%s] of [%s]",  # noqa: Y053
    ) -> None:
        """Raise an exception if credential does not exist in domain of folder

        :param name: Name of credential, ``str``
        :param folder_name: Folder name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        :param exception_message: Message to use for the exception.
                                  Formatted with ``name``, ``domain_name``,
                                  and ``folder_name``
        :throws: :class:`JenkinsException` whenever the credentail
            does not exist in domain of folder
        """

    def credential_exists(self, name: str, folder_name: str, domain_name: str = "_") -> bool:
        """Check whether a credentail exists in domain of folder

        :param name: Name of credentail, ``str``
        :param folder_name: Folder name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        :returns: ``True`` if credentail exists, ``False`` otherwise
        """

    def get_credential_info(self, name: str, folder_name: str, domain_name: str = "_") -> _JSON:
        """Get credential information dictionary in domain of folder

        :param name: Name of credentail, ``str``
        :param folder_name: folder_name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        :returns: Dictionary of credential info, ``dict``
        """

    def get_credential_config(self, name: str, folder_name: str, domain_name: str = "_") -> str:
        """Get configuration of credential in domain of folder.

        :param name: Name of credentail, ``str``
        :param folder_name: Folder name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        :returns: Credential configuration (XML format)
        """

    def create_credential(self, folder_name: str, config_xml: str, domain_name: str = "_") -> None:
        """Create credentail in domain of folder

        :param folder_name: Folder name, ``str``
        :param config_xml: New XML configuration, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        """

    def delete_credential(self, name: str, folder_name: str, domain_name: str = "_") -> None:
        """Delete credential from domain of folder

        :param name: Name of credentail, ``str``
        :param folder_name: Folder name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        """

    def reconfig_credential(self, folder_name: str, config_xml: str, domain_name: str = "_") -> None:
        """Reconfig credential with new config in domain of folder

        :param folder_name: Folder name, ``str``
        :param config_xml: New XML configuration, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        """

    def list_credentials(self, folder_name: str, domain_name: str = "_") -> list[Incomplete]:
        """List credentials in domain of folder

        :param folder_name: Folder name, ``str``
        :param domain_name: Domain name, default is '_', ``str``
        :returns: Credentials list, ``list``
        """

    def quiet_down(self) -> None:
        """Prepare Jenkins for shutdown.

        No new builds will be started allowing running builds to complete
        prior to shutdown of the server.
        """

    def wait_for_normal_op(self, timeout: int) -> bool:
        """Wait for jenkins to enter normal operation mode.

        :param timeout: number of seconds to wait, ``int``
            Note this is not the same as the connection timeout set via
            __init__ as that controls the socket timeout. Instead this is
            how long to wait until the status returned.
        :returns: ``True`` if Jenkins became ready in time, ``False``
                   otherwise.

        Setting timeout to be less than the configured connection timeout
        may result in this waiting for at least the connection timeout
        length of time before returning. It is recommended that the timeout
        here should be at least as long as any set connection timeout.
        """
