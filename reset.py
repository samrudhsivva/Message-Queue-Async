import pika

QUEUE_NAME = 'hello'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_purge(queue=QUEUE_NAME)
print(f"[!] Queue '{QUEUE_NAME}' purged.")

connection.close()
