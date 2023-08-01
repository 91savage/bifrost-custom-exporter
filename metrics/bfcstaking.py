from substrateinterface import SubstrateInterface
from pprint import pprint



ws_provider = SubstrateInterface(
    url="wss://public-01.mainnet.thebifrost.io/wss"
)

stakingCandidateInfo = ws_provider.query(
    module='BfcStaking',
    storage_function='CandidateInfo',
    params=['0x03FCBa6842bc2e0538Cc5360328ff3cb72038d43']
)

stakingCandidatePool = ws_provider.query(
    module='BfcStaking',
    storage_function='CandidatePool'
)

stakingRound = ws_provider.query(
    module='BfcStaking',
    storage_function='Round'
)


## unbond 신청 확인
request = stakingCandidateInfo['request']
## Current Round
cround = stakingRound['current_round_index']
## Execute Round or None
eround = stakingCandidateInfo['request']['whenExecutable'] if request.value is not None else None
# 남은 라운드 확인
rround = eround.value - cround.value if request.value is not None else None

################################################################################################

## 지명자 수
nominatorCount = stakingCandidateInfo['nomination_count'].value

## self-staking 한 token 양
selfStaking = stakingCandidateInfo['bond'].value

## staking 받은 token 양
nominatedToken = stakingCandidateInfo['voting_power'].value - stakingCandidateInfo['bond'].value

## 전체 스테이킹 된 Token 양 (votingPower)
votingPower = stakingCandidateInfo['voting_power'].value

## 수수료 율
commission = stakingCandidateInfo['commission'].value

## 리워드 처리
reward_dst = stakingCandidateInfo['reward_dst']

## Validator 수
validatorCount = len(stakingCandidatePool.value)

## validator 순위
def rank():
    for index, obj in enumerate(stakingCandidatePool.value):
        if obj['owner'] == '0x03fcba6842bc2e0538cc5360328ff3cb72038d43' :
            return index
        
## 노드 Tier (Full or Basic)
tier = stakingCandidateInfo['tier']

# Validator Status (Active or Inactive)
validatorStatus = stakingCandidateInfo['status']


# pprint(stakingCandidateInfo.value)