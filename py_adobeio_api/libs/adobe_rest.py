import json
import os
import calendar
from datetime import timedelta, datetime
import copy
import requests
import csv
from .common_auth import get_adobe_bearer_token_with_config
from .basiclog import log

MIN_EXPIRE_TIME = 1  # Hours until token expires

def load_config_file(filename):
    fq_config_file = os.path.realpath(filename)
    try:
        with open(fq_config_file, "r", encoding="utf-8") as config_pointer:
            return json.loads(config_pointer.read())
    except (ValueError, KeyError, TypeError):
        log.error(
            "load_config_file: Cannot parse JSON config file: " + fq_config_file)
    return {}

def expires_timestamp(expires_hours=MIN_EXPIRE_TIME):
    return calendar.timegm((datetime.utcnow() + timedelta(hours=expires_hours)).timetuple())


def now():
    return calendar.timegm(datetime.utcnow().timetuple())


class AdobeIORestAPI:
    def __init__(self,
                 config,  # configuration object for Adobe
                 # Bearer Token Generation routine - used to renew bearer token
                 bearer_token_gen=get_adobe_bearer_token_with_config,
                 default_expires_hours=MIN_EXPIRE_TIME):
        self.config = config
        self.bearer_token_gen = bearer_token_gen
        self.default_expires_hours = default_expires_hours
        self.bearer_token_expires = 0
        self.counter = 1

    def renew_bearer_token(self):
        bearer_token = self.bearer_token_gen(
            log=log, configuration=self.config)
        self.bearer_token = bearer_token["response_object"]["access_token"]
        self.bearer_token_expires = expires_timestamp(
            self.default_expires_hours)

    def rest_get(self, endpoint):
        if self.bearer_token_expires < now():
            log.debug("Detected expired token: renewing now")
            self.renew_bearer_token()
        headers = copy.deepcopy(self.config["header_template"])
        headers["x-gw-ims-org-id"] = self.config["api"]["org_id"]
        headers["x-api-key"] = self.config["api"]["client_id"]
        headers["Authorization"] = "Bearer " + self.bearer_token
        log.debug("header: " +
                       json.dumps(headers))
        result = requests.get(endpoint, headers=headers)
        log.debug("GET REQUEST RESULT: " + result.text)
        result_json = json.loads(result.text)
        return result_json

    def rest_post(self, endpoint, body_object):
        if self.bearer_token_expires < now():
            log.debug("Detected expired token: renewing now")
            self.renew_bearer_token()
        headers = copy.deepcopy(self.config["header_template"])
        headers["x-gw-ims-org-id"] = self.config["api"]["org_id"]
        headers["x-api-key"] = self.config["api"]["client_id"]
        headers["Authorization"] = "Bearer " + self.bearer_token
        log.debug("header: " +
                       json.dumps(headers))
        result = requests.post(
            endpoint, data=json.dumps(body_object), headers=headers)
        log.debug("POST REQUEST RESULT: " + result.text)
        result_json = json.loads(result.text)
        return result_json

    def rest_patch(self, endpoint, body_object):
        if self.bearer_token_expires < now():
            log.debug("Detected expired token: renewing now")
            self.renew_bearer_token()
        headers = copy.deepcopy(self.config["header_template"])
        headers["x-gw-ims-org-id"] = self.config["api"]["org_id"]
        headers["x-api-key"] = self.config["api"]["client_id"]
        headers["Authorization"] = "Bearer " + self.bearer_token
        log.debug("header: " +
                       json.dumps(headers))
        result = requests.patch(
            endpoint, data=json.dumps(body_object), headers=headers)
        log.debug("PATCH REQUEST RESULT: " + result.text)
        result_json = json.loads(result.text)
        return result_json
