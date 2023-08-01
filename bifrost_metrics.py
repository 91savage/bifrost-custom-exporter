from metrics import bfcstaking 
from metrics import api
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

eround =bfcstaking.eround
cround = bfcstaking.cround.value
nominatorCount = bfcstaking.nominatorCount
selfStaking = bfcstaking.selfStaking
nominatedToken = bfcstaking.nominatedToken
votingPower = bfcstaking.votingPower
commission = bfcstaking.commission
reward_dst = bfcstaking.reward_dst
validatorCount = bfcstaking.validatorCount
rank = bfcstaking.rank()
tier =bfcstaking.tier
validatorStatus = bfcstaking.validatorStatus
currentPrice = api.currentPrice



class balanceCollector():
    ## metric 만들 때, __init__을  사용하여 메트릭을 초기화
    # def __init__(self):
    #     pass

    ## 프로메테우스 관례 상 함수명을 collect로 해야됨 안하면 에러 남
    ## self는 클래스와 메소드가 클래스의 인스턴스와 상호작용 할 수 있도록 함 .
    def collect(self):
        b = GaugeMetricFamily("bifrostBalance", "Balance of Stash,Controller,Relayer", labels=["account"])
        b.add_metric(["stash"], s_balance)
        b.add_metric(["controller"], c_balance)
        b.add_metric(["relayer"], r_balance)
        ## return 과 같은데 다른점은 값들을 리스트에 저장하고 순차대로 값을 반환함. 대량 코드에 적합.
        yield b # b metrics 반환
        


class roundCollector():
    def collect(self):
        r = GaugeMetricFamily("round", "Current, Execute, Remain Rounds", labels=["round"])
        
        r.add_metric(["current round"], cround)
        if eround is None :
            ## NaN 으로 출력하기
            r.add_metric(["execute round"], float('nan'))
        else :
            r.add_metric(["execute round"], eround)
        yield r





class stakingCollector():
    def collect(self):
        s = GaugeMetricFamily("stakingAmount", "a mount of Staked Token", labels=["staked"])
        s.add_metric(["selfStakingAmount"], round(w3.from_wei((selfStaking),'ether'),2))
        s.add_metric(["nominatedTokenAmount"], round(w3.from_wei((nominatedToken),'ether'),2))
        s.add_metric(["sumOfStakingAmount"], round(w3.from_wei((votingPower),'ether'),2))
        yield s

        
class CountCollector():
    def collect(self):
        c = GaugeMetricFamily("totalCount", "Current Total Validator & Nominator Count", labels=["Count"])
        c.add_metric(["Total Validator Count"], validatorCount)
        c.add_metric(["Total Nominator Count"], nominatorCount)
        yield c
        
def singleMetric():
    c = Gauge("commission"," Validator Commission")
    c.set(commission/ 1e+07)
    v = Gauge("ValidatorRank", "Current Validator Rank")
    v.set(rank)
    p = Gauge("currentPrice", "Current BFC Priece")
    p.set(currentPrice)
    
    
def rewardDestination():
    r = Gauge("rewardDst", "Validator Reward Destination (0: Staked , 1: Account)")
    if reward_dst == "Staked" :
        r.set(0)
    else :
        r.set(1)

def tierNode():
    t = Gauge("nodeTier", "installed node Tier (0: Full , 1: Basic)")
    if tier == "Full" :
        t.set(0)
    else :
        t.set(1)
        
def statusValidator():
    v = Gauge("validatorStatus", "current Validator Status  (0: Active , 1: Inactive)")
    if validatorStatus == "Active" :
        v.set(0)
    else :
        v.set(1)
        
        





## 스크립트가 직접 실행 되었는지 (import 되지 않았는지) 확인하는 용도로 사용
if __name__ == "__main__":
    port = 9000
    
    ## metric 수집 주기 1초
    frequency =1

    ## Exporter 서버 시작
    start_http_server(port)
    # CustomCollector 등록 // 프로메테우스 라이브러리에서 제공하는 레지스트리 객체
    REGISTRY.register(balanceCollector())
    REGISTRY.register(roundCollector())
    REGISTRY.register(stakingCollector())
    REGISTRY.register(CountCollector())
    singleMetric()
    rewardDestination()
    tierNode()
    statusValidator()



    while True:
        # Balance.set(get_stash_balance())
        time.sleep(frequency)

        
        
        
        
        