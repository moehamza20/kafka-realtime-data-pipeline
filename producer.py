from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda value:json.dumps(value).encode('utf-8')
)


while True:
    payment ={
        "event_type": "payment_created",
        "lead_id": random.randint(1, 100),
        "course_id": random.randint(1, 10),
        "amount": random.randint(500, 5000),
        "payment_method": random.choice(["cash", "visa","instapay"]),
        "timestamp":datetime.now().isoformat()
    }
    producer.send('crm-payments', value=payment)
    producer.flush()
    
    print("payment event sent: ")
    print(payment)
    time.sleep(2)
    