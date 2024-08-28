import time
import memory_collector


def get_metric_dict():

    metric_dict = {}

    metric_dict['vm_memory_metrics'] = memory_collector.get_all_vm_memory_metrics()
        
    return metric_dict
