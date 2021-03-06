from datetime import datetime
from plone.app.users import userdataschema
from slt.theme import _
from zope import schema
from zope.interface import Interface


class UserDataSchemaProvider(userdataschema.UserDataSchemaProvider):
    """"""

    def getSchema(self):
        """
        """
        return IUserDataSchema


class BirthDateValidationError(schema.ValidationError):
    """Validation error for birth date"""
    __doc__ = _(u'birth_date_format', default=u'Use format: YYYY-MM-DD')


def validate_birth_date(value):
    value = value.strip()
    try:
        datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        raise BirthDateValidationError(value)
    return True


class IUserDataSchema(Interface):
    """
    """

    fullname = userdataschema.IUserDataSchema.get('fullname')
    email = userdataschema.IUserDataSchema.get('email')

    birth_date = schema.TextLine(
        title=_('Birth Date'),
        description=_(u'birth_date_format', default=u'Use format: YYYY-MM-DD'),
        required=False,
        constraint=validate_birth_date)

    registration_number = schema.TextLine(
        title=_('Registration Number'),
        required=False)

    allow_direct_marketing = schema.Bool(
        title=_(u'allow_direct_marketing_title', default=u'Allow Direct Marketing'),
        description=_(u'allow_direct_marketing_description', u'Check this box to allow direct marketing from this site.'),
        required=False)
