##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################
from prometheus_client.core import REGISTRY
from prometheus_client import start_http_server

import time
from logconf import get_logger
from dbhost.nexenta_collector import NexentaHealthCheckCollector
# from sdi.sdi_collector import SDIHealthCheckCollector

logger = get_logger()


if __name__ == '__main__':
    logger.info('Initializing Exporter')
    start_http_server(8082)
    logger.info('Exporter listening on 8082')
    REGISTRY.register(NexentaHealthCheckCollector())
    # REGISTRY.register(SDIHealthCheckCollector())

    while True:
        time.sleep(10)

