"""Transform secrets engine methods module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class Transform(VaultApiBase):
    """Transform Secrets Engine (API).

    Reference: https://www.vaultproject.io/api-docs/secret/transform
    """

    def create_or_update_role(self, name, transformations, mount_point: str = "transform"):
        """Creates or update the role with the given name.

        If a role with the name does not exist, it will be created. If the role exists, it will be
        updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/role/:name.

        :param name: the name of the role to create. This is part of the request URL.
        :type name: str | unicode
        :param transformations: Specifies the transformations that can be used with this role.
            At least one transformation is required.
        :type transformations: list
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the create_or_update_role request.
        :rtype: requests.Response
        """

    def read_role(self, name, mount_point: str = "transform"):
        """Query an existing role by the given name.

        Supported methods:
            GET: /{mount_point}/role/:name.

        :param name: the name of the role to read. This is part of the request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the read_role request.
        :rtype: requests.Response
        """

    def list_roles(self, mount_point: str = "transform"):
        """List all existing roles in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/role.

        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the list_roles request.
        :rtype: requests.Response
        """

    def delete_role(self, name, mount_point: str = "transform"):
        """Delete an existing role by the given name.

        Supported methods:
            DELETE: /{mount_point}/role/:name.

        :param name: the name of the role to delete. This is part of the request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the delete_role request.
        :rtype: requests.Response
        """

    def create_or_update_transformation(
        self,
        name,
        transform_type,
        template,
        tweak_source: str = "supplied",
        masking_character: str = "*",
        allowed_roles=None,
        mount_point: str = "transform",
    ):
        """Create or update a transformation with the given name.

        If a transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformation/:name.

        :param name: the name of the transformation to create or update. This is part of
            the request URL.
        :type name: str | unicode
        :param transform_type: Specifies the type of transformation to perform.
            The types currently supported by this backend are fpe and masking.
            This value cannot be modified by an update operation after creation.
        :type transform_type: str | unicode
        :param template: the template name to use for matching value on encode and decode
            operations when using this transformation.
        :type template: str | unicode
        :param tweak_source: Only used when the type is FPE.
        :type tweak_source: str | unicode
        :param masking_character: the character to use for masking. If multiple characters are
            provided, only the first one is used and the rest is ignored. Only used when
            the type is masking.
        :type masking_character: str | unicode
        :param allowed_roles: a list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :type allowed_roles: list
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the create_or_update_ation request.
        :rtype: requests.Response
        """

    def create_or_update_fpe_transformation(
        self, name, template, tweak_source: str = "supplied", allowed_roles=None, mount_point: str = "transform"
    ):
        """Creates or update an FPE transformation with the given name.

        If a transformation with the name does not exist, it will be created. If the transformation exists, it will be
        updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/fpe/:name.


        :param name: The name of the transformation to create or update. This is part of
            the request URL.
        :type name: str
        :param template: The template name to use for matching value on encode and decode
            operations when using this transformation.
        :type template: str
        :param tweak_source: Specifies the source of where the tweak value comes from. Valid sources are:
            supplied, generated, and internal.
        :type tweak_source: str
        :param allowed_roles: A list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :type allowed_roles: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the create_or_update_fpe_transformation request.
        :rtype: requests.Response
        """

    def create_or_update_masking_transformation(
        self, name, template, masking_character: str = "*", allowed_roles=None, mount_point: str = "transform"
    ):
        """Creates or update a masking transformation with the given name. If a
        transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/masking/:name.


        :param name: The name of the transformation to create or update. This is part of
            the request URL.
        :type name: str
        :param template: The template name to use for matching value on encode and decode
            operations when using this transformation.
        :type template: str
        :param masking_character: The character to use for masking. If multiple characters are
            provided, only the first one is used and the rest is ignored. Only used when
            the type is masking.
        :type masking_character: str
        :param allowed_roles: A list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :type allowed_roles: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the create_or_update_masking_transformation request.
        :rtype: requests.Response
        """

    def create_or_update_tokenization_transformation(
        self,
        name,
        max_ttl: int = 0,
        mapping_mode: str = "default",
        allowed_roles=None,
        stores=None,
        mount_point: str = "transform",
    ):
        """
        This endpoint creates or updates a tokenization transformation with the given name. If a
        transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/:name.

        :param max_ttl: The maximum TTL of a token. If 0 or unspecified, tokens may have no expiration.
        :type max_ttl: str
        :param mapping_mode: Specifies the mapping mode for stored tokenization values.

            * `default` is strongly recommended for highest security
            * `exportable` exportable allows for all plaintexts to be decoded via the export-decoded endpoint in an emergency.

        :type mapping_mode: str
        :param allowed_roles: aAlist of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :type allowed_roles: list
        :param stores: list of tokenization stores to use for tokenization state. Vault's
            internal storage is used by default.
        :type stores: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the create_or_update_tokenization_transformation request.
        :rtype: requests.Response
        """

    def read_transformation(self, name, mount_point: str = "transform"):
        """Query an existing transformation by the given name.

        Supported methods:
            GET: /{mount_point}/transformation/:name.

        :param name: Specifies the name of the role to read.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the read_ation request.
        :rtype: requests.Response
        """

    def list_transformations(self, mount_point: str = "transform"):
        """List all existing transformations in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/transformation.

        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the list_ation request.
        :rtype: requests.Response
        """

    def delete_transformation(self, name, mount_point: str = "transform"):
        """Delete an existing transformation by the given name.

        Supported methods:
            DELETE: /{mount_point}/transformation/:name.

        :param name: the name of the transformation to delete. This is part of the
            request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the delete_ation request.
        :rtype: requests.Response
        """

    def create_or_update_template(self, name, template_type, pattern, alphabet, mount_point: str = "transform"):
        """Creates or update a template with the given name.

        If a template with the name does not exist, it will be created. If the
        template exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/template/:name.

        :param name: the name of the template to create.
        :type name: str | unicode
        :param template_type: Specifies the type of pattern matching to perform.
            The only type currently supported by this backend is regex.
        :type template_type: str | unicode
        :param pattern: the pattern used to match a particular value. For regex type
            matching, capture group determines the set of character that should be matched
            against. Any matches outside of capture groups are retained
            post-transformation.
        :type pattern: str | unicode
        :param alphabet: the name of the alphabet to use when this template is used for FPE
            encoding and decoding operations.
        :type alphabet: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the create_or_update_template request.
        :rtype: requests.Response
        """

    def read_template(self, name, mount_point: str = "transform"):
        """Query an existing template by the given name.

        Supported methods:
            GET: /{mount_point}/template/:name.

        :param name: Specifies the name of the role to read.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the read_template request.
        :rtype: requests.Response
        """

    def list_templates(self, mount_point: str = "transform"):
        """List all existing templates in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/transformation.

        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the list_template request.
        :rtype: requests.Response
        """

    def delete_template(self, name, mount_point: str = "transform"):
        """Delete an existing template by the given name.

        Supported methods:
            DELETE: /{mount_point}/template/:name.

        :param name: the name of the template to delete. This is part of the
            request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the delete_template request.
        :rtype: requests.Response
        """

    def create_or_update_alphabet(self, name, alphabet, mount_point: str = "transform"):
        """Create or update an alphabet with the given name.

        If an alphabet with the name does not exist, it will be created. If the
        alphabet exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/alphabet/:name.

        :param name: Specifies the name of the transformation alphabet to create.
        :type name: str | unicode
        :param alphabet: the set of characters that can exist within the provided value
            and the encoded or decoded value for a FPE transformation.
        :type alphabet: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the create_or_update_alphabet request.
        :rtype: requests.Response
        """

    def read_alphabet(self, name, mount_point: str = "transform"):
        """Queries an existing alphabet by the given name.

        Supported methods:
            GET: /{mount_point}/alphabet/:name.


        :param name: the name of the alphabet to delete. This is part of the request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the read_alphabet request.
        :rtype: requests.Response
        """

    def list_alphabets(self, mount_point: str = "transform"):
        """List all existing alphabets in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/alphabet.

        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the list_alphabets request.
        :rtype: requests.Response
        """

    def delete_alphabet(self, name, mount_point: str = "transform"):
        """Delete an existing alphabet by the given name.

        Supported methods:
            DELETE: /{mount_point}/alphabet/:name.

        :param name: the name of the alphabet to delete. This is part of the request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the delete_alphabet request.
        :rtype: requests.Response
        """

    def create_or_update_tokenization_store(
        self,
        name,
        driver,
        connection_string,
        username=None,
        password=None,
        type: str = "sql",
        supported_transformations=None,
        schema: str = "public",
        max_open_connections: int = 4,
        max_idle_connections: int = 4,
        max_connection_lifetime: int = 0,
        mount_point: str = "transform",
    ):
        """Create or update a storage configuration for use with tokenization.
        The database user configured here should only have permission to SELECT, INSERT, and UPDATE rows in the tables.

        Supported methods:
            POST: /{mount_point}/store/:name.

        :param name: The name of the store to create or update.
        :type name: str
        :param type: Specifies the type of store. Currently only `sql` is supported.
        :type type: str
        :param driver: Specifies the database driver to use, and thus which SQL database type.
            Currently the supported options are `postgres` or `mysql`
        :type driver: str
        :param supported_transformations: The types of transformations this store can host. Currently only `tokenization` is supported.
        :type supported_transformations: list(str)
        :param connection_string: database connection string with template slots for username and password that
            Vault will use for locating and connecting to a database.  Each
            database driver type has a different syntax for its connection strings.
        :type connection_string: str
        :param username: username value to use when connecting to the database.
        :type username: str
        :param password: password value to use when connecting to the database.
        :type password: str
        :param schema: schema within the database to expect tokenization state tables.
        :type schema: str
        :param max_open_connections: maximum number of connections to the database at any given time.
        :type max_open_connections: int
        :param max_idle_connections: maximum number of idle connections to the database at any given time.
        :type max_idle_connections: int
        :param max_connection_lifetime: means no limit.
        :type max_connection_lifetime: duration
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the create_or_update_tokenization_store request.
        :rtype: requests.Response
        """

    def encode(self, role_name, value=None, transformation=None, tweak=None, batch_input=None, mount_point: str = "transform"):
        """Encode the provided value using a named role.

        Supported methods:
            POST: /{mount_point}/encode/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :type role_name: str | unicode
        :param value: the value to be encoded.
        :type value: str | unicode
        :param transformation: the transformation within the role that should be used for this
            encode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :type transformation: str | unicode
        :param tweak: the tweak source.
        :type tweak: str | unicode
        :param batch_input: a list of items to be encoded in a single batch. When this
            parameter is set, the 'value', 'transformation' and 'tweak' parameters are
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :type batch_input: list
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the encode request.
        :rtype: requests.Response
        """

    def decode(self, role_name, value=None, transformation=None, tweak=None, batch_input=None, mount_point: str = "transform"):
        """Decode the provided value using a named role.

        Supported methods:
            POST: /{mount_point}/decode/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :type role_name: str | unicode
        :param value: the value to be decoded.
        :type value: str | unicode
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :type transformation: str | unicode
        :param tweak: the tweak source.
        :type tweak: str | unicode
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value', 'transformation' and 'tweak' parameters are
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :type batch_input: array<object>
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the decode request.
        :rtype: requests.Response
        """

    def validate_token(self, role_name, value, transformation, batch_input=None, mount_point: str = "transform"):
        """Determine if a provided tokenized value is valid and unexpired.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/validate/:role_name.


        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :type role_name: str
        :param value: the token for which to check validity.
        :type value: str
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :type transformation: str
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :type batch_input: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the validate_token request.
        :rtype: requests.Response
        """

    def check_tokenization(self, role_name, value, transformation, batch_input=None, mount_point: str = "transform"):
        """Determine if a provided plaintext value has an valid, unexpired tokenized value.
        Note that this cannot return the token, just confirm that a
        tokenized value exists. This endpoint is only valid for tokenization
        transformations.

        Supported methods:
            POST: /{mount_point}/tokenized/:role_name.


        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :type role_name: str
        :param value: the token to test for whether it has a valid tokenization.
        :type value: str
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :type transformation: str
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :type batch_input: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the check_tokenization request.
        :rtype: requests.Response
        """

    def retrieve_token_metadata(self, role_name, value, transformation, batch_input=None, mount_point: str = "transform"):
        """
        This endpoint retrieves metadata for a tokenized value using a named role.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/metadata/:role_name.


        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :type role_name: str
        :param value: the token for which to retrieve metadata.
        :type value: str
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :type transformation: str
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :type batch_input: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the retrieve_token_metadata request.
        :rtype: requests.Response
        """

    def snapshot_tokenization_state(self, name, limit: int = 1000, continuation: str = "", mount_point: str = "transform"):
        """
        This endpoint starts or continues retrieving a snapshot of the stored
        state of a tokenization transform.  This state is protected as it is
        in the underlying store, and so is safe for storage or transport.  Snapshots
        may be used for backup purposes or to migrate from one store to another.
        If more than one store is configured for a tokenization transform, the
        snapshot data contains the contents of the first store.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/snapshot/:name.


        :param name: the name of the transformation to snapshot.
        :type name: str
        :param limit: maximum number of tokenized value states to return on this call.
        :type limit: int
        :param continuation: absent or empty, a new snapshot is started.  If present, the
            snapshot should continue at the next available value.
        :type continuation: str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the snapshot_tokenization_state request.
        :rtype: requests.Response
        """

    def restore_tokenization_state(self, name, values, mount_point: str = "transform"):
        """
        This endpoint restores previously snapshotted tokenization state values
        to the underlying store(s) of a tokenization transform.  Calls to this
        endpoint are idempotent, so multiple outputs from a snapshot run can
        be applied via restore in any order and duplicates will not cause a problem.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/restore/:name.


        :param name: the name of the transformation to restore.
        :type name: str
        :param values: number of tokenization state values from a previous snapshot call.
        :type values: str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the restore_tokenization_state request.
        :rtype: requests.Response
        """

    def export_decoded_tokenization_state(self, name, limit: int = 1000, continuation: str = "", mount_point: str = "transform"):
        """Start or continue retrieving an export of tokenization state, including the tokens and their decoded values.
        This call is only supported on tokenization stores configured with the exportable mapping mode.
        Refer to the Tokenization documentation for when to use the exportable mapping mode.
        Decoded values are in Base64 representation.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/export-decoded/:name.


        :param name: the name of the transformation to export.
        :type name: str
        :param limit: maximum number of tokenized value states to return on this call.
        :type limit: int
        :param continuation: absent or empty, a new export is started.  If present, the
            export should continue at the next available value.
        :type continuation: str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the export_decoded_tokenization_state request.
        :rtype: requests.Response
        """

    def rotate_tokenization_key(self, transform_name, mount_point: str = "transform"):
        """Rotate the version of the named key.
        After rotation, new requests will be encoded with the new version of the key.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/rotate.


        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :type transform_name: str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the rotate_tokenization_key request.
        :rtype: requests.Response
        """

    def update_tokenization_key_config(self, transform_name, min_decryption_version, mount_point: str = "transform"):
        """Allow the minimum key version to be set for decode operations.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/config.


        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :type transform_name: str
        :param min_decryption_version: the minimum key version that vault can use to decode values for the
            corresponding transform.
        :type min_decryption_version: int
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the update_tokenization_key_config request.
        :rtype: requests.Response
        """

    def list_tokenization_key_configuration(self, mount_point: str = "transform"):
        """List all tokenization keys.
        Only valid for tokenization transformations.

        Supported methods:
            LIST: /{mount_point}/tokenization/keys/.

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the list_tokenization_key_configuration request.
        :rtype: requests.Response
        """

    def read_tokenization_key_configuration(self, transform_name, mount_point: str = "transform"):
        """Read tokenization key configuration for a particular transform.
        Only valid for tokenization transformations.

        Supported methods:
            GET: /{mount_point}/tokenization/keys/:{mount_point}_name.


        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :type transform_name: str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the read_tokenization_key_configuration request.
        :rtype: requests.Response
        """

    def trim_tokenization_key_version(self, transform_name, min_available_version, mount_point: str = "transform"):
        """Trim older key versions setting a minimum version for the keyring.
        Once trimmed, previous versions of the key cannot be recovered.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/trim.


        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :type transform_name: str
        :param min_available_version:
        :type min_available_version: int
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str
        :return: The response of the trim_tokenization_key_version request.
        :rtype: requests.Response
        """
