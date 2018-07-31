# -*- coding: utf-8 -*-

import json
import socket
import requests


def prometheus_register(host, project, port):
    metrics_port = port
    hostname = host
    print hostname, project, metrics_port
    ID = '-'.join([hostname, str(metrics_port)])
    #url = 'http://10.204.207.60:9500/v1/agent/service/deregister/%s' % ID
    url = 'http://10.104.252.251:8500/v1/agent/service/register'
    body = {'ID': ID, 'Name': 'qb-app', 'Tags': [hostname, project, str(port)], 'Address': hostname, 'Port': metrics_port}
    headers = {"Content-Type": "application/json"}
    print json.dumps(body)
    response = requests.put(url, headers=headers, data=json.dumps(body))
    print response, response.content
    print '------------------'


if __name__ == "__main__":
    [prometheus_register('t-pic2', 'qiubai_video', port) for port in range(7970, 7978)]
    [prometheus_register('t-pic2', 'qiubai_video', port) for port in range(9300, 9310)]
    [prometheus_register('t-pic2', 'qiubai_video', port) for port in range(12998, 13000)]
    #  prometheus_register('t-pic2', 'qiubai_video', 19999)

