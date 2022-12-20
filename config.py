import os

class Config(object):
    # API URL we will connect to - note versioning:
    API_URL = os.environ.get('API_URL') or 'http://127.0.0.1:5001/api/v1'

    # TODO: set environment variables before going live if you want
    # otherwise it will pull the values from here.
    # DO NOT use the defaulted values here for a production instance.

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Z8ltgjR9NWuqFrTHh2sw9jwmsKM1wf9g'

    # The tokens used to authenticate with the API:
    READ_TOKEN = os.environ.get('READ_TOKEN') or '5daf6de2-fe42-468b-9e1b-a453afc0fc1c'

    WRITE_TOKEN = os.environ.get('WRITE_TOKEN') or '5daf718e-e77e-4dc8-84d9-86e50cb6adbd'
