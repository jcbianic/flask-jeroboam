from flask_jeroboam.openapi.models import SecurityBase as SecurityBaseModel


class SecurityBase:
    model: SecurityBaseModel
    scheme_name: str
