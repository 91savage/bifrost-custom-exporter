from web3 import Web3
from dotenv import load_dotenv
import os
import time
import requests



from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server, Gauge



load_dotenv()


relayerAddress = os.environ.get('relayerAddress')
stashAddress = os.environ.get('stashAddress')
controllerAddress = os.environ.get('controllerAddress')

w3 = Web3(Web3.HTTPProvider('https://public-01.mainnet.thebifrost.io/rpc'))
balance = round(w3.from_wei(w3.eth.get_balance(relayerAddress),'ether'),2)

s_balance = round(w3.from_wei(w3.eth.get_balance(stashAddress),'ether'),2)
c_balance = round(w3.from_wei(w3.eth.get_balance(controllerAddress),'ether'),2)
r_balance = round(w3.from_wei(w3.eth.get_balance(relayerAddress),'ether'),2)



class mycustomCollector(object):
    def __init__(self):
        pass


    def collect(self):
        b = GaugeMetricFamily("bifrostBalance", "Balance of Stash,Controller,Relayer", labels=["account"])

        b.add_metric(["stash"], s_balance)
        b.add_metric(["controller"], c_balance)
        b.add_metric(["relayer"],r_balance)
        yield b # b metrics 반환


if __name__ == "__main__":
    port = 9000
    frequency =1

    ## Exporter 서버 시작
    start_http_server(port)
    # CustomCollector 등록
    REGISTRY.register(mycustomCollector())
    

    while True:
        # Balance.set(get_stash_balance())
        time.sleep(frequency)