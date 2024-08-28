##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

import urllib3
from prometheus_client.core import Metric
from logconf import get_logger
from utility import read_config_file
from nexenta import get_nexenta_metrics
from constants import DB_KEY, METRICS_TO_MONITOR

# Suppress InsecureWarning while contanting openstack endpoints
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger()


class NexentaHealthCheckCollector(object):
    def __init__(self):
        pass

    def collect(self):
        logger.info('Collecting Nexenta Health check Metrics')
        # Read Config File
        config_data = read_config_file()

        # Collecting the Dictionary element with all Nexenta Data
        db_metrics_dict = get_nexenta_metrics(config_data, METRICS_TO_MONITOR, DB_KEY)

        # Assigning Host Type
        host_type = DB_KEY

        ##############################
        # Pool Metrics
        ##############################
        logger.info('Collecting Nexenta Pool Health check Metrics')
        # Collecting pool_status
        metric = Metric("{}_pool_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["pool"].items():
                metric.add_sample("{}_pool_status".format(host_type), value=elem_val["status"],
                                  labels={"host": node, "pool": elem})
        yield metric

        # Collecting pool_free_storage
        metric = Metric("{}_pool_free_storage".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["pool"].items():
                metric.add_sample("{}_pool_free_storage".format(host_type), value=elem_val["free_storage"],
                                  labels={"host": node, "pool": elem})
        yield metric

        # Collecting pool_allocated_storage
        metric = Metric("{}_pool_allocated_storage".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["pool"].items():
                metric.add_sample("{}_pool_allocated_storage".format(host_type), value=elem_val["allocated_storage"],
                                  labels={"host": node, "pool": elem})
        yield metric

        # Collecting pool_total_capacity
        metric = Metric("{}_pool_total_capacity".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["pool"].items():
                metric.add_sample("{}_pool_total_capacity".format(host_type), value=elem_val["total_capacity"],
                                  labels={"host": node, "pool": elem})
        yield metric

        ##############################
        # Disk Metrics
        ##############################
        logger.info('Collecting Nexenta Disk Health check Metrics')
        # Collecting disk_status
        metric = Metric("{}_disk_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["disk"].items():
                metric.add_sample("{}_disk_status".format(host_type), value=elem_val["status"],
                                  labels={"host": node, "disk_number": elem, "model": elem_val["model"],
                                          "usedBy": elem_val["usedBy"]})
        yield metric

        # Collecting disk_size
        metric = Metric("{}_disk_size".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["disk"].items():
                metric.add_sample("{}_disk_size".format(host_type), value=elem_val["size"],
                                  labels={"host": node, "disk_number": elem, "model": elem_val["model"],
                                          "usedBy": elem_val["usedBy"]})
        yield metric

        ##############################
        # HACluster Metrics
        ##############################
        logger.info('Collecting Nexenta HACluster Health check Metrics')
        # Collecting hacluster_status
        metric = Metric("{}_hacluster_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            ha = node_val["hacluster"]
            metric.add_sample("{}_hacluster_status".format(host_type), value=ha["status"],
                              labels={"host": node})
        yield metric

        # Collecting hacluster_site_status
        metric = Metric("{}_hacluster_site_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            ha = node_val["hacluster"]
            metric.add_sample("{}_hacluster_site_status".format(host_type), value=ha["site_status"],
                              labels={"host": node})
        yield metric

        ##############################
        # Filesystem Metrics
        ##############################
        logger.info('Collecting Nexenta Filesystem Health check Metrics')
        # Collecting filesystem_size_used
        metric = Metric("{}_filesystem_size_used".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["filesystem"].items():
                metric.add_sample("{}_filesystem_size_used".format(host_type), value=elem_val["size_used"],
                                  labels={"host": node, "file_system": elem})
        yield metric

        # Collecting filesystem_size_available
        metric = Metric("{}_filesystem_size_available".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["filesystem"].items():
                metric.add_sample("{}_filesystem_size_available".format(host_type), value=elem_val["size_available"],
                                  labels={"host": node, "file_system": elem})
        yield metric

        ##############################
        # Links Metrics
        ##############################
        logger.info('Collecting Nexenta Links Health check Metrics')
        # Collecting links_status
        metric = Metric("{}_links_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["links"].items():
                metric.add_sample("{}_links_status".format(host_type), value=elem_val["status"],
                                  labels={"host": node, "link_name": elem, "class": elem_val["class"]})
        yield metric

        # Collecting links_interface_status
        metric = Metric("{}_links_interface_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["links"].items():
                metric.add_sample("{}_links_interface_status".format(host_type), value=elem_val["interface_status"],
                                  labels={"host": node, "link_name": elem, "class": elem_val["class"]})
        yield metric

        ##############################
        # Service Metrics
        ##############################
        logger.info('Collecting Nexenta Service Health check Metrics')
        # Collecting service_status
        metric = Metric("{}_service_status".format(host_type), "Metrics taken in every N sec", "summary")
        for node, node_val in db_metrics_dict.items():
            for elem, elem_val in node_val["service"].items():
                metric.add_sample("{}_service_status".format(host_type), value=elem_val,
                                  labels={"host": node, "service_name": elem})
        yield metric


# class SDIHealthCheckCollector(object):
#     def __init__(self):
#         pass
#
#     def collect(self):
#         logger.info('Collecting SDI Health check Metrics')
