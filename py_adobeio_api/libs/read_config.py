import json
import os
from libs.log import log


def load_config_file(filename):
    fq_config_file = os.path.realpath(filename)
    try:
        with open(fq_config_file, "r", encoding="utf-8") as config_pointer:
            return json.loads(config_pointer.read())
    except (ValueError, KeyError, TypeError):
        log.error(
            "load_config_file: Cannot parse JSON config file: " + fq_config_file)
    return {}
