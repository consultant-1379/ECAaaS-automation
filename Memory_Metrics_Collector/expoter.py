from prometheus_client.core import  GaugeMetricFamily, REGISTRY, CounterMetricFamily, Metric
from prometheus_client import start_http_server

import json
import requests
import time
import collector
import parser
import urllib3


# Suppress InsecureWarning while contanting openstack endpoints
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initiating STDOUT log handler
import logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:  %(message)s")
logger = logging.getLogger(__name__)


class CapacityCollector(object):

    def __init__(self):
      #  self._metrics_dict = metrics_dict
        pass

    def collect(self):
        logger.info('Collecting Capacity Metrics')
        metric_dict = collector.get_metric_dict()        

        metric = Metric('os_capacity', 'Metrics taken in every 10 seconds', 'summary')
        _exculde = ['vm_memory_metrics']

        for data in metric_dict:
            if not data in _exculde:
                metric.add_sample(data, value=metric_dict[data], labels={})
        yield metric

        logger.info('Collecting Free mem metrics')
        metric = Metric('vm_cur_free_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_free_memory', value=subvalue['free_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric

        logger.info('Collecting Used mem metrics')
        metric = Metric('vm_cur_used_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_used_memory', value=subvalue['used_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric

        logger.info('Collecting total mem metrics')
        metric = Metric('vm_cur_total_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_total_memory', value=subvalue['total_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric

        logger.info('Collecting shared mem metrics')
        metric = Metric('vm_cur_shared_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_shared_memory', value=subvalue['shared_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric

        logger.info('Collecting buffer mem metrics')
        metric = Metric('vm_cur_buffer_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_buffer_memory', value=subvalue['buffers_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric

        logger.info('Collecting cached mem metrics')
        metric = Metric('vm_cur_cached_memory', "Metrics taken in every 10 sec", 'summary')
        for k, v in metric_dict['vm_memory_metrics'].items():
            if not isinstance(v,dict):
                continue
            for subkey, subvalue in v.items():
                metric.add_sample('vm_cur_cached_memory', value=subvalue['cached_mem'], labels={'app_name': k, 'vm_name': subkey, 'dc': subvalue['datacenter']})            
        yield metric


 
        

if __name__ == '__main__':
    logger.info('Initializing Expoter')
    start_http_server(8082)
    logger.info('Expoter listening on 8082')
    REGISTRY.register(CapacityCollector())
    
    while True: 	time.sleep(10)

