from http import HTTPStatus as _HS

# re‑export for convenience:  status.OK  instead of  HTTPStatus.OK
class status:
    OK                    = _HS.OK
    CREATED               = _HS.CREATED
    NO_CONTENT            = _HS.NO_CONTENT
    BAD_REQUEST           = _HS.BAD_REQUEST
    UNAUTHORIZED          = _HS.UNAUTHORIZED
    NOT_FOUND             = _HS.NOT_FOUND
    CONFLICT              = _HS.CONFLICT
    INTERNAL_SERVER_ERROR = _HS.INTERNAL_SERVER_ERROR