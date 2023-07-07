from web3 import Web3
from dotenv import load_dotenv
import os
import time

from prometheus_clinet.core import GaugeMetricFamily
from prometheus_client import start_http_server, Gauge

load_dotenv()

relayerAddress = os.environ.get('relayerAddress')
stashAddress = os.environ.get('stashAddress')
controllerAddress = os.environ.get('controllerAddress')

w3 = Web3(Web3.HTTPProvider('https://public-01.mainnet.thebifrost.io/rpc'))
balance = round(w3.from_wei(w3.eth.get_balance(relayerAddress),'ether'),2)


rBalance = Gauge(
    'balance',
    'This is Bifrost Balance'
)

def balance():

    balance = GaugeMetricFamily("Bifrost_Balance", "This is Balance of Bifrost", labels =["Stash","Controller","Relayer"])

def get_stash_balance():
    balance = round(w3.from_wei(w3.eth.get_balance(stashAddress),'ether'),2)
    return balance

def get_relayer_balance():
    balance = round(w3.from_wei(w3.eth.get_balance(relayerAddress),'ether'),2)
    return balance

def get_controller_balance():
    balance = round(w3.from_wei(w3.eth.get_balance(controllerAddress),'ether'),2)
    return balance

if __name__ == "__main__":
    port = 9000
    frequency =1


    start_http_server(port)

    while True:
        rBalance.set(get_relayer_balance())
        time.sleep(frequency)