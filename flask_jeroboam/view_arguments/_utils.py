"""Helper functions for extracting values from request locations."""
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from werkzeug.datastructures import MultiDict

from flask_jeroboam._utils import is_sequence_field
from flask_jeroboam.wrapper import current_app


def _extract_scalar(
    *,
    source: Union[MultiDict, dict],
    name: Optional[str],
    alias: Optional[str],
    **_kwargs,
):
    """Extract a scalar value from a source."""
    return source.get(alias, source.get(name))


def _extract_sequence(
    *, source: MultiDict, name: Optional[str], alias: Optional[str], **_kwargs
) -> List:
    """Extract a Sequence value from a source."""
    _values = source.getlist(alias)
    if len(_values) == 0:
        _values = source.getlist(name)
    return _values


def _extract_sequence_with_key_transformer(
    *, source: MultiDict, name: Optional[str], alias: Optional[str], **_kwargs
):
    """Apply the key transformer to the source."""
    transformed_source = current_app.query_string_key_transformer(
        current_app, source.to_dict()
    )
    return _extract_scalar(source=transformed_source, name=name, alias=alias)


def _undirected_extraction(
    *,
    field,
    source,
    alias: str,
    name: str,
    has_key_transformer: bool,
    **_kwargs,
):
    if is_sequence_field(field):
        values = _extract_sequence(source=source, name=name, alias=alias)
        if len(values) == 0 and has_key_transformer:
            values = _extract_sequence_with_key_transformer(
                source=source, name=name, alias=alias
            )
    else:
        values = _extract_scalar(source=source, name=name, alias=alias)
    return values


def _extract_subfields(
    *,
    source: MultiDict,
    fields: Dict,
    **_kwargs,
) -> Dict:
    """Extract a Sequence from subfields."""
    has_key_transformer = (
        getattr(current_app, "query_string_key_transformer", False) is not None
    )
    return {
        field_name: _undirected_extraction(
            field=subfield,
            source=source,
            name=field_name,
            alias=subfield.alias,
            has_key_transformer=has_key_transformer,
        )
        for field_name, subfield in fields.items()
    }
