import time


from prometheus_client import start_http_server, Counter

c = Counter(
    name ="counter_test",
    documentation = "This is Custom Counter",
    labelnames=["first", "second"])


if __name__ == "__main__":
    port = 9000
    frequency =1


    c.labels(first='1', second='2').inc(1)

    start_http_server(port)

    while True:
        # period between collection
        time.sleep(frequency)