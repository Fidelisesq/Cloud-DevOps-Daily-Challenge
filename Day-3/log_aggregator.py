import pika

# RabbitMQ credentials and host
rabbitmq_host = '18.175.223.242'  # Replace with your RabbitMQ server IP or hostname
rabbitmq_user = 'rabbituser'  # Replace with your RabbitMQ username
rabbitmq_password = 'rabbituser7'  # Replace with your RabbitMQ password

# Set up credentials
credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

# Declare a durable queue
channel.queue_declare(queue='logs_queue', durable=True)

# Callback function to process log messages
def callback(ch, method, properties, body):
    log_message = body.decode()
    print(f" [x] Received: {log_message}")

    # Save the log to a file
    with open('aggregated_logs.txt', 'a') as f:
        f.write(log_message + '\n')

    print(" [x] Log saved to file")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Ensure fair dispatch
channel.basic_qos(prefetch_count=1)

# Start consuming messages
channel.basic_consume(queue='logs_queue', on_message_callback=callback)

print(" [*] Waiting for logs. To exit press CTRL+C")
channel.start_consuming()