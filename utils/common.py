import base64

from werkzeug.exceptions import BadRequest


def decode_file(path, encoded_file_base64):
    with open(path, "wb") as file:
        try:
            file.write(base64.b64decode(encoded_file_base64.encode("utf-8")))
        except Exception as ex:
            raise BadRequest("Invalid photo encoding")
