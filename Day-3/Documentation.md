# Distributed Logging System


### 1. Install RabbitMQ
First, install RabbitMQ on your server. Follow the installation instructions for your specific operating system from the official RabbitMQ website: [RabbitMQ Installation Guide](https://www.rabbitmq.com/download.html).

### 2. Enable RabbitMQ Management Plugin
The management plugin provides a user interface and HTTP-based API for managing RabbitMQ. Run the following command to enable it:

```sh
sudo rabbitmq-plugins enable rabbitmq_management
```
_This command enables the RabbitMQ management plugin, allowing access to the web-based management interface._

### 3. Create a New User
Create a new RabbitMQ user with a specific username and password:

```sh
rabbitmqctl add_user alice secret_password
```
_This command creates a new user named `alice` with the password `secret_password`._

### 4. Set Permissions for the User
Grant the user permissions to access and manage resources:

```sh
rabbitmqctl set_permissions -p / alice ".*" ".*" ".*"
```
_This command gives the user `alice` full permissions (read, write, and configure) on the default virtual host `/`._

### 5. Add Management Tag to the User
Grant the user access to the RabbitMQ management interface:

```sh
rabbitmqctl set_user_tags alice management
```
_This command adds the `management` tag to the user `alice`, allowing them to log in to the RabbitMQ management interface._

### 6. Access the RabbitMQ Management Interface
Open your web browser and navigate to `http://<your_rabbitmq_server>:15672/`. Log in with the username `alice` and the password you set.

### 7. Add a Queue
Once logged in, follow these steps to add a queue:

- Click on the "Queues" tab.
- Click on "Add a new queue".
- Enter the name of the queue (e.g., `my_queue`) and configure any additional settings as needed.
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
   ./rabbitmqadmin declare queue name=my_queue durable=true
   ```
   _This command creates a durable queue named `my_queue`._

### Challenges
- After creating a queue sucessfully, I could not log in into the `RabbitMQ Management` console with the credentials I created. I discovered I had to tag the user as part of `Management` to be able to login. 
```python
rabbitmqctl set_user_tags username management
```