import os

ENV = os.environ['ENV']
SSO_UI_URL="https://sso.ui.ac.id/cas2/login"
if ENV == "PROD":
    BASE_URL = os.environ['BASE_URL']
else:
    BASE_URL = "http://127.0.0.1:5000"