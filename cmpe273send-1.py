import pika

QUEUE_NAME = 'hello'
MESSAGE_COUNT = 1000000

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (durable)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

for i in range(MESSAGE_COUNT):
    message = f"Message {i}"
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    if i % 100000 == 0:
        print(f"[x] Sent {i} messages...")

print(f"[x] Finished sending {MESSAGE_COUNT} messages.")
connection.close()
