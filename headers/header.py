import base64

from api.headers.errors import InvalidHeaderTypeError

class Headers:
    def __init__(self, values = None):
        if values:
            if type(values) == dict:
                self.values = values.copy()
            elif type(values) == Headers:
                self.values = values.values.copy()
            else:
                raise InvalidHeaderTypeError()
        else: 
            self.values = {}

    def __add__(self, other):
        if type(other) == Headers:
            other = other.values.copy()

        elif type(other) != dict:
            raise InvalidHeaderTypeError(f'Type \'{type(other)}\' is not a valid header type.')

        result = self.values.copy()
        for key, value in other.items():
            result[key] = value

        return Headers(result)

    def to_dict(self) -> dict[str, str]:
        return self.values.copy()

def accept_json():
    return Headers({'Accept': 'application/json'})

def content_type_json():
    return Headers({'Content-Type': 'application/json'})

ACCEPT_JSON = accept_json()

def _get_basic_token(
        username: str, 
        password: str, 
        string_encoding: str = 'utf-8', 
        string_decoding: str = 'ascii', 
        byte_encoding = base64.b64encode):
    
    token_content = f'{username}:{password}'
    token_content_bytes = token_content.encode(string_encoding)
    token_encoded_bytes = byte_encoding(token_content_bytes)
    return token_encoded_bytes.decode(string_decoding)

def basic_authorization(
        username: str, 
        password: str, 
        string_encoding: str = 'utf-8', 
        string_decoding: str = 'ascii', 
        byte_encoding = base64.b64encode):
    
    token = _get_basic_token(username, password, string_encoding, string_decoding, byte_encoding)

    return Headers({'Authorization': f'Basic {token}'})

def bearer_token_authorization(token: str):
    return Headers({'Authorization': f'Bearer {token}'})