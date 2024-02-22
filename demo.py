from typing import Any, Mapping

import jsonschema

store: dict[str, Mapping[str, Any]] = {}

jsonschema.RefResolver(base_uri="file://mypath.json", referrer={}, store=store)
