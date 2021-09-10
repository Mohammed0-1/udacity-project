import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-z6rs6ps7.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting_agency'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
    attempts to get the header from the request
    raises an AuthError if no header is present
    attempts to split bearer and the token
    raises an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({'code':'Not Authorized',
                        'description':'You Are not authorized'}
                        ,401)
    
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({'code':'invalid header',
        'description':'malfromed request'}
        ,400)
    if header_parts[0].lower() != 'bearer':
        raise AuthError({'code':'invalid header',
        'description':'malfromed request'}
        ,400)
    
    return header_parts[1]

'''
    @INPUTS
        permission: string permission (i.e. 'get:actors')
        payload: decoded jwt payload

    raises an AuthError if permissions are not included in the payload
    raises an AuthError if the requested permission string is not in the payload permissions array
    returns true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({'code':'Bad Request'},400)
    if permission != '' and permission not in payload['permissions']:
        raise AuthError({'code':'Forbidden',
                        'description':'You Do Not Have The Permissons To View The Resouce You Requested'}
                        ,403)
    
    return True

'''
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
    @INPUTS
        permission: string permission (i.e. 'post:movie')

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt method to decode the jwt
    uses the check_permissions method validate claims and check the requested permission
    returns the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator