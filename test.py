import time
import random
import http.server

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server

class myustomCollector(object):
    def __init__(self):
        pass

    # Collect 함수를 꼭 만들어 주어야 Start_http_server에서 사용함.
    def collect(self):
        #Gauge 만들기           # 메트릭 이름       # 메트릭 설명                   #라벨     -> 을 가진 g(gauge) 를 생성
        g = GaugeMetricFamily("random_number", "Gauge-- Number Generator", labels=["randomNum1", "randomNum2"])
        #Gauge 값 넣기
        g.add_metric("", random.randint(1,20))
        g.add_metric(["First"], random.randint(1,20))
        g.add_metric(["", "Second"], random.randint(1,20))
        g.add_metric(["First", "Second"], random.randint(1,20))
        yield g ## gauge 메트릭을 반환함.

        #Counter 만들기
        c = CounterMetricFamily("random_number_2", "Counter-- Number Generator", labels=["randomNum1", "randomNum2"])
        #Counter 값 넣기
        c.add_metric("", random.randint(1,20))
        c.add_metric(["First"], random.randint(1,20))
        c.add_metric(["First", "Second"], random.randint(1,20))
        yield c ## counter 메트릭을 반환함.

if __name__ == "__main__":
    port = 9000
    frequency = 1


    # Exporter 서버  시작
    start_http_server(port)
    # CustomCollector 등록
    REGISTRY.register(myustomCollector())

    while True:
        # period between collection
        time.sleep(frequency)