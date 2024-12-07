# Distributed Logging System with RabbitMQ
![RabbitMQ_logs_queue](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-3/Images/Queue-UI.png)

Below is the setup procedure for my centralised distributed logging. This system is essential for log management, message queues, and monitoring, which are critical to modern DevOps practices. The system setup includes a log producer and consumer system using RabbitMQ, which can aggregate them into a file for analysis.

## System Setup Guide

### 1. Install RabbitMQ
First, install RabbitMQ on your server. Follow the installation instructions for your specific operating system from the official RabbitMQ website: https://www.rabbitmq.com/download.html I installed RabbitMQ on AWS EC2 running Ubuntu

```sh
sudo apt update
sudo apt install rabbitmq-server -y
```
![RabbitMQ_server_running](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-3/Images/Rabbitmq%20server%20running%20with%20queue%20created.png)
### 2. Enable RabbitMQ Management Plugin
The management plugin provides a user interface and HTTP-based API for managing RabbitMQ. Run the following command to enable it:

```sh
sudo rabbitmq-plugins enable rabbitmq_management
```
_This command enables the RabbitMQ management plugin, allowing access to the web-based management interface._

### 3. Create a New User
Create a new RabbitMQ user with a specific username and password:

```sh
rabbitmqctl add_user rabituser secret_password
```
_This command creates a new user named `rabbituser` with the password `secret_password`._

### 4. Set Permissions for the User
Grant the user permissions to access and manage resources:

```sh
rabbitmqctl set_permissions -p / rabbituser ".*" ".*" ".*"
```
_This command gives the user `rabbituser` full permissions (read, write, and configure) on the default virtual host `/`._

### 5. Add Management Tag to the User
Grant the user access to the RabbitMQ management interface:

```sh
rabbitmqctl set_user_tags rabbituser management
```
_This command adds the `management` tag to the user `rabbituser`, allowing them to log in to the RabbitMQ management interface._

### 6. Configuring External Network Access
Edit the `/etc/rabbitmq/rabbitmq.conf` file to allow external access because `RabbitMQ` blocks localhost access by default. Add the configuration.

```listeners.tcp.default = 5672```
Now restart the system
```sh
sudo systemctl restart rabbitmq-server
```

### 7. Add a Queue
Once logged in, follow these steps to add a queue:

- Click on the "Queues" tab.
- Click on "Add a new queue".
- Enter the name of the queue (e.g., `logs_queue`) and configure any additional settings as needed.
- Click the "Add queue" button to create the queue.

### 8. Adding Queue via CLI (Optional)
Alternatively, you can add a queue using the `rabbitmqadmin` command-line tool:

1. **Download `rabbitmqadmin`**: Navigate to `http://<your_rabbitmq_server>:15672/cli/rabbitmqadmin` to download the tool.
2. **Make it executable**:
   ```sh
   chmod +x rabbitmqadmin
   ```
3. **Declare a Queue**:
   ```sh
   ./rabbitmqadmin declare queue name=logs_queue durable=true
   ```
   _This command creates a durable queue named `logs_queue`._

### 9. Access the RabbitMQ Management Interface
Open your web browser and navigate to `http://<your_rabbitmq_server>:15672/`. Log in with the username `rabbituser` and the password you set to verify that `logs_queue` that you created exists. 
You may also verify using CLI command to see the queue
```sh
sudo rabbitmqctl list_queues
```
![logs_queue](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-3/Images/Queue-UI.png)

### 10. Install Required Python Libraries
Install pika and write a python script that will produce logs and consume them. See tutorial on Rabbitmq Documentation https://www.rabbitmq.com/tutorials/tutorial-one-python or check my script log_producer.py & log_aggregtor.py
`pip install pika`

Run the producer script 
```python
python3 log_prodcer.py "Log Entry 1: Data ready for processing in AWS Lambda"
```

Run the consumer script. 
```python
python3 log aggregator.py
```
`Note:` Perform step 10 several times with different messages to send and capture multiple logs

### Verify Logs
Open the `aggregated_logs.txt` file to ensure all logs are captured
![log captured](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-3/Images/Log%20entries.png)

### Challenges
- After creating a queue sucessfully, I could not log in into the `RabbitMQ Management` console with the credentials I created. I discovered I had to tag the user as part of `Management` to be able to login. 
```python
rabbitmqctl set_user_tags username management
```
- Port configuration and permission management. At first, I could not create the `logs_queue` as it was returning `Access Denied`. Then, I granted my user the needed permission to vHosts and created EC2 Security group that allows TCP port 15672 to access the RabbitMQ management console.

### Key Learnings
- Enabling Management Plugin: I learnt to enable and use the RabbitMQ management plugin for web-based monitoring and management.
- User and Permission Management: Gained skills in creating users, setting passwords, and managing permissions in RabbitMQ.
- Queue Management: I learned how to create and manage queues both via the management interface and command line.
- Port Configuration: Understanding the importance of configuring and managing RabbitMQ ports (5672 for AMQP traffic and 15672 for the management console). 
