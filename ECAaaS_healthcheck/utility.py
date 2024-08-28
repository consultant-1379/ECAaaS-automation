##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################
import yaml
from dbhost.constants import CONFIG_FILE_NAME, DB_KEY, USER_KEY


def read_config_file():
    with open(CONFIG_FILE_NAME, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg


def get_api_user_info(config_obj):
    api_user_info = config_obj[USER_KEY]
    username = str(api_user_info["username"])
    password = str(api_user_info["password"])
    return username, password


def get_db_dict(config_obj, key):
    db_dict = config_obj[key]
    return db_dict
