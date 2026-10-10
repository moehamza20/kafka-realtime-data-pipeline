from kafka import KafkaConsumer
import json
import psycopg2


consumer = KafkaConsumer(
    'crm-payments',
    bootstrap_servers='localhost:9092',
    group_id='payments-consumers',
    value_deserializer=lambda value: json.loads(
        value.decode('utf-8')
    )
)

connection =psycopg2.connect(
    host="localhost",
    port=5432,
    database="raiseup",
    user="postgres",
    password="5591"
)

cursor = connection.cursor()


print("started consumer.....")
for message in consumer:
    payment = message.value
    print("payment event received: ")
    print(payment)
    
    query="""
    INSERT INTO streaming_payments (lead_id , course_id , amount , payment_method , event_time) VALUES (%s , %s , %s , %s , %s)
"""

    cursor.execute(query, (
        payment['lead_id'], 
        payment['course_id'], 
        payment['amount'], 
        payment['payment_method'], 
        payment['timestamp']
        )
    )
    connection.commit()
    print("payment saved to database")
    
    
    
    
    

    