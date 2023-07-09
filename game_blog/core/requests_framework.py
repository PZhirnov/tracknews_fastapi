import json

class PostRequest:
    @staticmethod
    def parse_body_json(data: bytes):
        data = data.decode('utf-8')
        data = json.loads(data)
        return data
