# RabbitMQ Monitoring with Prometheus and Grafana

In this blog, I’ll walk you through the setup of a RabbitMQ environment that includes a **local Docker Compose setup** for quick testing and a **3-node RabbitMQ cluster setup on AWS EC2** for scalability and real-world applications. Additionally, we’ll integrate **Prometheus and Grafana** for monitoring, ensuring robust observability. 

### Overview of the Project

RabbitMQ is a popular message broker that plays a crucial role in distributed systems. This project aimed to:
1. Set up a RabbitMQ environment both locally and on AWS.
2. Monitor RabbitMQ metrics using Prometheus and visualize them with Grafana.
3. Test the message queuing system using Python scripts.

---

### Part 1: Local RabbitMQ Setup Using Docker Compose

**Why Local Setup?**  
The local setup serves as a quick testing environment before deploying to the cloud.

**Steps to Set Up:**

1. **Clone the RabbitMQ Repository:**
   ```bash
   git clone https://github.com/rabbitmq/rabbitmq-server.git
   cd rabbitmq-server/deps/rabbitmq_prometheus/docker
   ```

2. **Run Docker Compose:**
   ```bash
   docker-compose -f docker-compose-metrics.yml up -d
   docker-compose -f docker-compose-overview.yml up -d
   ```

3. **Access RabbitMQ Dashboard:**
   - URL: `http://localhost:15672`
   - Default credentials:  
     Username: `guest`  
     Password: `guest`

4. **Access Grafana Dashboard:**  
   - URL: `http://localhost:3000`  
   - Default credentials:  
     Username: `admin`  
     Password: `admin`

---

### Part 2: RabbitMQ 3-Node Cluster on AWS EC2

**Why a Cluster?**  
To ensure high availability and load distribution in production.

#### Prerequisites
- Three AWS EC2 instances running Ubuntu 24.04.
- Security groups allowing necessary ports (e.g., 4369, 25672, 15692, 15672).

#### Step-by-Step Guide

1. **Install RabbitMQ on All Nodes:**
   Use the following **bash script** as EC2 user data during instance launch:

   ```bash
   #!/bin/bash
   sudo apt update -y
   sudo apt upgrade -y
   sudo apt install -y curl gnupg software-properties-common
   curl -fsSL https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey | sudo apt-key add -
   sudo apt-add-repository "deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ focal main"
   sudo apt update -y
   sudo apt install -y rabbitmq-server
   sudo systemctl enable rabbitmq-server
   sudo systemctl start rabbitmq-server
   sudo rabbitmq-plugins enable rabbitmq_management rabbitmq_prometheus
   ```

2. **Cluster Configuration:**
   - Verify Erlang cookie consistency:
     ```bash
     sudo cat /var/lib/rabbitmq/.erlang.cookie
     ```
     Ensure the same cookie on all nodes.
   - Join nodes to form a cluster:
     ```bash
     sudo rabbitmqctl stop_app
     sudo rabbitmqctl reset
     sudo rabbitmqctl join_cluster rabbit@<master-node-hostname>
     sudo rabbitmqctl start_app
     ```

3. **Verify Cluster Status:**
   ```bash
   sudo rabbitmqctl cluster_status
   ```

---

### Part 3: Monitoring with Prometheus and Grafana

#### Prometheus Setup on AWS EC2

1. **Install Prometheus Using a Bash Script:**
   ```bash
   #!/bin/bash
   sudo apt update -y
   sudo apt upgrade -y
   sudo apt install -y wget tar
   wget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-arm64.tar.gz
   tar xvf prometheus-2.47.0.linux-arm64.tar.gz
   sudo mv prometheus-2.47.0 /usr/local/prometheus
   echo 'Prometheus installed.'
   ```

2. **Configure Prometheus:**
   Edit `prometheus.yml` to scrape RabbitMQ metrics:
   ```yaml
   scrape_configs:
     - job_name: 'rabbitmq'
       static_configs:
         - targets: ['<rabbitmq-node-1-ip>:15692', '<rabbitmq-node-2-ip>:15692', '<rabbitmq-node-3-ip>:15692']
   ```

3. **Run Prometheus:**
   ```bash
   /usr/local/prometheus/prometheus --config.file=/usr/local/prometheus/prometheus.yml
   ```

#### Grafana Setup on AWS EC2

1. **Install Grafana Using a Bash Script:**
   ```bash
   #!/bin/bash
   sudo apt update -y
   sudo apt install -y wget unzip
   wget https://dl.grafana.com/enterprise/release/grafana-enterprise-11.4.0.linux-arm64.tar.gz
   tar xvf grafana-enterprise-11.4.0.linux-arm64.tar.gz
   sudo mv grafana-11.4.0 /usr/local/grafana
   echo 'Grafana installed.'
   ```

2. **Configure Grafana:**
   - Add Prometheus as a data source.
   - Import RabbitMQ dashboards.

3. **Verify Metrics on Grafana:**
   - URL: `http://<grafana-ip>:3000`
   - Navigate to imported RabbitMQ dashboards to monitor metrics.

---

### Part 4: Testing the Message Queue

Using Python scripts, I tested message publishing and consumption:

```python
import pika

# Connection setup
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-node-ip', credentials=credentials))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='test_queue')

# Publish message
channel.basic_publish(exchange='', routing_key='test_queue', body='Hello RabbitMQ!')
print("Message published.")

# Consume message
def callback(ch, method, properties, body):
    print(f"Received: {body}")

channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

---

### Final Thoughts

This project showcased the power of RabbitMQ in a distributed setup and the importance of monitoring using Prometheus and Grafana. Whether for testing or production, the tools and techniques used here ensure a scalable and observable messaging system.