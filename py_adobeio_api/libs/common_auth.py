from jwt import (
    JWT, jwk_from_pem
)
import json
import calendar
from datetime import timedelta, datetime
import os
import copy
import requests

DEFAULT_EXPIRE_TIME = 1  # Hours until the token expires
DEFAULT_ADOBE_BEARER_TOKEN_ENDPOINT = "https://ims-na1.adobelogin.com/ims/exchange/jwt/"
JWT_TEMPLATE = {}


def expires_timestamp(max_timeout_hours=DEFAULT_EXPIRE_TIME):
    return calendar.timegm((datetime.utcnow() + timedelta(hours=max_timeout_hours+1)).timetuple())


def compute_jwt_token(log, private_file, jwt_token_template=JWT_TEMPLATE,
                      max_timeout_hours=DEFAULT_EXPIRE_TIME):
    jwt_token_template["exp"] = expires_timestamp(max_timeout_hours)
    fp_private_file = os.path.realpath(private_file)
    log.info("Opening private file: " + fp_private_file)
    log.debug("JWT: " + json.dumps(jwt_token_template))
    jwt_token = "not-calculated"
    jwt_obj = JWT()

    with open(fp_private_file, "r", encoding="UTF-8") as priv_file_pointer:
        priv_key = jwk_from_pem(priv_file_pointer.read().encode())
        jwt_token = jwt_obj.encode(jwt_token_template,
                                   priv_key, 'RS256')
        log.debug("Calculated JWT token: " + str(jwt_token))
        return jwt_token
    return jwt_token


def get_adobe_bearer_token(log,
                           client_id,
                           client_secret,
                           private_file,
                           jwt_token_template=JWT_TEMPLATE,
                           endpoint=DEFAULT_ADOBE_BEARER_TOKEN_ENDPOINT,
                           max_timeout_hours=DEFAULT_EXPIRE_TIME):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "jwt_token": compute_jwt_token(log, private_file, jwt_token_template, max_timeout_hours)
    }
    log.debug("Payload: " + json.dumps(payload))
    result = requests.post(endpoint,
                           data=payload,
                           headers={"cache-control": "no-cache"})
    log.debug("Request Result: " + str(result.text))
    result_obj = {
        "response_object": json.loads(result.text)
    }
    result_obj["bearer_token"] = result_obj["response_object"]["access_token"]
    return result_obj


def get_adobe_bearer_token_with_config(log, configuration):
    return get_adobe_bearer_token(log,
                                  client_id=configuration["api"]["client_id"],
                                  client_secret=configuration["api"]["client_secret"],
                                  private_file=configuration["files"]["api_private_key_file"],
                                  jwt_token_template=configuration["jwt_template"],
                                  endpoint=configuration["api"]["bearer_token_endpoint"])
