##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

from constants import API_ACCESS_PORT
from utility import get_api_user_info, get_db_dict
from authentication import Authentication
from api import invoke_get_request


def get_full_header(token):
    return {"Authorization": "Bearer {}".format(token)}


def get_pool_dict(token, ip):
    pool_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/storage/pools".format(ip, API_ACCESS_PORT)
    pool_response = invoke_get_request(url, header).json()
    pool_response_data = pool_response['data']
    for pool in pool_response_data:
        pool_item = {"status": 0 if pool["health"] == "ONLINE" else 1, "total_capacity": pool["storageCapacity"],
                     "allocated_storage": pool["storageAllocated"], "free_storage": pool["storageFree"]}
        pool_dict[str(pool["poolName"])] = pool_item

    return pool_dict


def get_disk_dict(token, ip):
    disk_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/inventory/disks?fields=diskIndex" \
          "%2Cstate" \
          "%2Cmodel" \
          "%2Csize" \
          "%2Cusage".format(ip, API_ACCESS_PORT)
    disk_response = invoke_get_request(url, header).json()
    disk_response_data = disk_response['data']
    for disk in disk_response_data:
        disk_dict[str(disk["diskIndex"])] = {"status": 0 if disk["state"] == "ONLINE" else 1, "size": disk["size"],
                                             "model": str(disk["model"]),
                                             "usedBy": str(disk["usage"]["usedName"]) if disk["usage"]["usedBy"] != "unused" else "unused"}

    return disk_dict


def get_hacluster_dict(token, ip):
    ha_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/services/ha".format(ip, API_ACCESS_PORT)
    ha_response = invoke_get_request(url, header).json()
    ha_dict = {"status": 0 if ha_response["state"] == "online" else 1,
               "site_status": 0 if str(ha_response["site"]) in "siteA" else 1}

    return ha_dict


def get_nfs_fs_dict(token, ip):
    fs_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/storage/filesystems?sharedOverNfs=true".format(ip, API_ACCESS_PORT)
    fs_response = invoke_get_request(url, header).json()
    fs_response_data = fs_response['data']
    for fs in fs_response_data:
        fs_dict[str(fs["path"])] = {"size_available": fs["bytesAvailable"], "size_used": fs["bytesUsed"]}

    return fs_dict


def get_service_dict(token, ip):
    service_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/services".format(ip, API_ACCESS_PORT)
    svc_response = invoke_get_request(url, header).json()
    svc_response_data = svc_response['data']
    for svc in svc_response_data:
        service_dict[str(svc["name"])] = 0 if svc["state"] == "online" else 1

    return service_dict


def get_links_dict(token, ip):
    links_dict = {}
    header = get_full_header(token)
    url = "https://{}:{}/network/links".format(ip, API_ACCESS_PORT)
    links_response = invoke_get_request(url, header).json()
    links_response_data = links_response['data']
    for link in links_response_data:
        links_dict[str(link["name"])] = {"status": 0 if str(link["state"]) == "up" else 1, "class": str(link["class"]),
                                         "interface_status": 0 if str(link["interface"]) == "ok" else 1}

    return links_dict


switcher = {
    "pool": get_pool_dict,
    "disk": get_disk_dict,
    "hacluster": get_hacluster_dict,
    "service": get_service_dict,
    "filesystem": get_nfs_fs_dict,
    "links": get_links_dict
}


def collect_metric(arg, token, ip):
    func = switcher.get(arg)
    return func(token, ip)


def collect_node_metrics(token, ip, metrics_to_monitor):
    node_metric_dict = {}
    for item in metrics_to_monitor:
        node_metric_dict[item] = collect_metric(item, token, ip)

    return node_metric_dict


def get_nexenta_metrics(config_data, metrics_to_monitor, db_key):
    """
    Script Entry point
    Following are the main functions executed in the script, which will be executed whenever there is a data scrape.
        1. Creating an auth object for the nexenta api user which will contain an auth-token
        2. Use the above auth-token to make further calls to get health-check metrics
    :return: Health check metrics Dictionary for Nexenta
    """
    # config_data = read_config_file()
    username, password = get_api_user_info(config_data)

    db_dict = get_db_dict(config_data, db_key)

    nex_metric_dict = {}
    for hostname, ip in db_dict.items():
        auth = Authentication(ip, username, password)
        token = auth.generate_nexenta_auth_token()
        nex_metric_dict[hostname] = collect_node_metrics(token, ip, metrics_to_monitor)

    return nex_metric_dict
