from abc import abstractmethod
from collections.abc import Callable, Sequence
from typing import Any
from typing_extensions import Self

from wtforms.fields import HiddenField
from wtforms.fields.core import UnboundField, _Filter, _FormT, _Validator, _Widget
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta, _SupportsGettextAndNgettext

__all__ = ("CSRFTokenField", "CSRF")

class CSRFTokenField(HiddenField):
    """
    A subclass of HiddenField designed for sending the CSRF token that is used
    for most CSRF protection schemes.

    Notably different from a normal field, this field always renders the
    current token regardless of the submitted value, and also will not be
    populated over to object data via populate_obj
    """

    current_token: str | None
    csrf_impl: CSRF
    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: str | Callable[[], str] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
        *,
        csrf_impl: CSRF,
    ) -> None: ...

class CSRF:
    field_class: type[CSRFTokenField]
    def setup_form(self, form: BaseForm) -> list[tuple[str, UnboundField[Any]]]:
        """
        Receive the form we're attached to and set up fields.

        The default implementation creates a single field of
        type :attr:`field_class` with name taken from the
        ``csrf_field_name`` of the class meta.

        :param form:
            The form instance we're attaching to.
        :return:
            A sequence of `(field_name, unbound_field)` 2-tuples which
            are unbound fields to be added to the form.
        """

    @abstractmethod
    def generate_csrf_token(self, csrf_token_field: CSRFTokenField) -> str:
        """
        Implementations must override this to provide a method with which one
        can get a CSRF token for this form.

        A CSRF token is usually a string that is generated deterministically
        based on some sort of user data, though it can be anything which you
        can validate on a subsequent request.

        :param csrf_token_field:
            The field which is being used for CSRF.
        :return:
            A generated CSRF string.
        """

    @abstractmethod
    def validate_csrf_token(self, form: BaseForm, field: CSRFTokenField) -> None:
        """
        Override this method to provide custom CSRF validation logic.

        The default CSRF validation logic simply checks if the recently
        generated token equals the one we received as formdata.

        :param form: The form which has this CSRF token.
        :param field: The CSRF token field.
        """
