import json,random,string,time
from datetime import date
from kafka import KafkaProducer
topic_name = 'test_sink'

kafka_bootstrap_servers = ["localhost:9092"]

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def create_kafka_producer(bootstrap_servers):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        return producer
    except Exception as err:
        print(f"Producer creation failed due to {err}")

kafka_producer = create_kafka_producer(kafka_bootstrap_servers)

while True:
    v = {
        "data_source": "some_random_api",
        "event": {
            "name": randomword(10),
            "number": random.randint(0, 100),
            "date": str(date.today())
        },
        "date": str(date.today())
        }
    kafka_producer.send(topic_name, value=v)
    print(v)
    time.sleep(3)
