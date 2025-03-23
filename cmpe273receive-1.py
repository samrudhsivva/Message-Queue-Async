import pika

QUEUE_NAME = 'hello'
EXPECTED_COUNT = 1000000

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (durable)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

message_count = 0

def callback(ch, method, properties, body):
    global message_count
    message_count += 1

    if message_count % 10000 == 0:
        print(f"Received {message_count} messages so far.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Stop after expected messages
    if message_count >= EXPECTED_COUNT:
        print(f"✅ All {EXPECTED_COUNT} messages received. Shutting down.")
        ch.stop_consuming()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

print(" [*] Waiting for messages. To exit early press CTRL+C")
channel.start_consuming()

connection.close()
