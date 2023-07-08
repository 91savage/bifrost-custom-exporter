from web3 import Web3
from dotenv import load_dotenv
import os
import time

from prometheus_client.core import GaugeMetricFamily
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


Balance = Gauge(
    'balance',
    'This is Bifrost Balance',
    ["stash", "controller","relayer"]
)

# def get_stash_balance():
#     balance = round(w3.from_wei(w3.eth.get_balance(stashAddress),'ether'),2)
#     return balance





if __name__ == "__main__":
    port = 9000
    frequency =1

    Balance.labels(stash=f'{s_balance}',controller=f'{c_balance}', relayer=f'{r_balance}')

    ## Exporter 서버 시작
    start_http_server(port)

    while True:
        # Balance.set(get_stash_balance())
        time.sleep(frequency)