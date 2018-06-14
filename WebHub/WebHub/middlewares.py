# encoding=utf-8
import random
from WebHub.user_agents import agents
import json
import requests


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'platform': 'pc',
        'ss': '367701188698225489',
        'bs': '%s',
        'RNLBSERVERID': 'ded6699',
        'FastPopSessionRequestNumber': '1',
        'FPSRN': '1',
        'performance_timing': 'home',
        'RNKEY': '40859743*68067497:1190152786:3363277230:1'
    }

    def process_request(self, request, spider):
        bs = ''
        for i in range(32):
            bs += chr(random.randint(97, 122))
        _cookie = json.dumps(self.cookie) % bs
        request.cookies = json.loads(_cookie)

class MyProxyMiddleware(object):
    def __init__(self):
        self.ip_url = 'http://localhost:5555/random'
        self.base_url_ip = 'https://'
        self.ip_list = []
        for i in range(10):
            ip = self.get_proxy()
            if ip not in self.ip_list:
                self.ip_list.append(ip)

    def process_request(self, request, spider):
        ip = random.choice(self.ip_list)
        if ip:
            request.meta['proxy'] = ip

    def get_proxy(self):
        url_response = requests.get(self.ip_url)
        if url_response.status_code == 200:
            ip = self.base_url_ip + url_response.text
            return ip
        else:
            None
