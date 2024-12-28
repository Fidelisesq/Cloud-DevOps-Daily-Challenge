# RabbitMQ Monitoring with Prometheus and Grafana

In this project, I completed two setups for RabbitMQ monitoring with Prometheus and Grafana. The first setup is a **local Docker Compose setup** for quick testing while the other is a **3-node RabbitMQ cluster setup on AWS EC2** for scalability and real-world applications.

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
   Use Docker Compose to start the RabbitMQ cluster and Prometheus instance, along with a basic workload to generate       
   meaningful metrics. This will start a RabbitMQ cluster, Prometheus, and Grafana with predefined configurations, 
   collecting metrics from RabbitMQ.
   ```bash
   docker-compose -f docker-compose-metrics.yml up -d
   docker-compose -f docker-compose-overview.yml up -d
   ```
    ![Docker compose](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Rabbit-Prometheus-Grafana-Up.png)
   <br><br>
   ![Docker compose](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Rabbit-metrics.png)
   <br><br>
   ![Rabbit_Prometheus_Containers](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Rabbit-Prometheus-Grafana-containers.png)

4. **Access RabbitMQ Dashboard:**
   - URL: `http://localhost:15672`
   - Default credentials:  
     Username: `guest`  
     Password: `guest`

5. **Access Grafana Dashboard:**  
   - URL: `http://localhost:3000`  
   - Default credentials:  
     Username: `admin`  
     Password: `admin`
     <br><br>
![Grafana_dashboard](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Grafana%20RabbitmQ%20Metric%20dashboard.png)
<br><br>
![Grafana_dashboard_2](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Grafana%20RabbitmQ%20Metric%20dashboard-2.png)
<br><br>
![Grafana_Dashboard_3](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/Docker_compose_images/Grafana%20RabbitmQ%20Metric%20dashboard-3.png)
---

### Part 2: RabbitMQ 3-Node Cluster on AWS EC2

**Why a Cluster?**  
To ensure high availability and load distribution in production.

#### Prerequisites
3 AWS EC2 instances running Ubuntu 24.04 for RabbitMQ and one each for Prometheus and Grafana. Configure the Security Groups as follows:

- **RabbitMQ Security Groups**:
  - Allow SSH (port 22) from your IP.
  - Allow RabbitMQ Management UI (port 15672) from your IP.
  - Allow RabbitMQ Prometheus Metrics (port 15692) from Prometheus instance SG.

- **Prometheus Security Groups**:
  - Allow HTTP (port 80) from your IP.
  - Allow HTTPS (port 443) from your IP.
  - Allow Grafana (port 3000) from your IP.

- **Grafana Security Groups**:
  - Allow HTTP (port 80) from your IP.
  - Allow HTTPS (port 443) from your IP.


#### Step-by-Step Guide

1. **Install RabbitMQ on All 3 Nodes:**
   Use a **bash script** as EC2 user data during instance launch or save it and run on each EC2 instance.
   The bash script I used is named `rabbitmq_installation.sh` in my git repository. It includes all the plugins needed to help Prometheus scrape metrics from RabbitMQ.

   ![RabbitMQ runing](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/rabbitmq-running-1.png)

3. **Cluster Configuration:**
   - Verify Erlang cookie consistency:
     ```bash
     sudo cat /var/lib/rabbitmq/.erlang.cookie
     ```
     Ensure the same cookie is on all 3 RabbitMQ EC2 nodes.
   - Join nodes to form a cluster:
     ```bash
     sudo rabbitmqctl stop_app
     sudo rabbitmqctl reset
     sudo rabbitmqctl join_cluster rabbit@<master-node-hostname>
     sudo rabbitmqctl start_app
     ```

4. **Verify Cluster Status:**
   ```bash
   sudo rabbitmqctl cluster_status
   ```
   ![Rabbit_3_Node_Cluster](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/rabbit_cluster_3_nodes.png)

---

### Part 3: Monitoring with Prometheus and Grafana

#### Prometheus Setup on AWS EC2

1. **Install Prometheus Using a Bash Script:**
   I used a Bash script named `prometheus.sh` saved in my repository to install Prometheus and it includes all the plugins needed. Save this script on your Prometheus EC2 and run the script.
   ```bash
   ./prometheus.sh
   ```

3. **Configure Prometheus:**
   Edit `prometheus.yml` to scrape RabbitMQ metrics:
   ```yaml
   scrape_configs:
     - job_name: 'rabbitmq'
       static_configs:
         - targets: ['<rabbitmq-node-1-ip>:15692', '<rabbitmq-node-2-ip>:15692', '<rabbitmq-node-3-ip>:15692']
   ```

4. **Run Prometheus:**
   ```bash
   /usr/local/prometheus/prometheus --config.file=/usr/local/prometheus/prometheus.yml
   ```
   ![Prometheus_Scrapping_Metrics](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/Prometheus%20scapping%20metrics.png)

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
   - Add Prometheus as a data source in Grafana
   - Import RabbitMQ dashboards - the file is named `RabbitMQ-Overview.json`

3. **Verify Metrics on Grafana:**
   - URL: `http://<grafana-ip>:3000`
   - Navigate to imported RabbitMQ dashboards to monitor metrics.
     <br><br>
     ![Grafana_Running](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/graphana-running.png)
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
`Grafana showing metrics scrapped by Prometheus`
![Grafana_Metrics](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/grafana.png)
<br><br>
![Grafana_Metrics_2](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-4/3-Node%20AWS%20Setup%20Images/grafana-2.png)

---

### Final Thoughts

This project showcased the power of RabbitMQ in a distributed setup and the importance of monitoring using Prometheus and Grafana. Whether for testing or production, the tools and techniques used here ensure a scalable and observable messaging system.
