#!/bin/bash

# Update and install prerequisites
sudo apt update && sudo apt upgrade -y
sudo apt install -y wget tar nano

# Download and install Prometheus
PROM_VERSION="2.49.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROM_VERSION/prometheus-$PROM_VERSION.linux-amd64.tar.gz
tar -xvf prometheus-$PROM_VERSION.linux-amd64.tar.gz
cd prometheus-$PROM_VERSION.linux-amd64

# Move binaries to /usr/local/bin
sudo mv prometheus /usr/local/bin/
sudo mv promtool /usr/local/bin/

# Create Prometheus configuration directory and move files
sudo mkdir -p /etc/prometheus
sudo mv prometheus.yml /etc/prometheus/
sudo mv consoles /etc/prometheus/
sudo mv console_libraries /etc/prometheus/

# Configure Prometheus to scrape RabbitMQ metrics
cat <<EOF | sudo tee /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'rabbitmq'
    static_configs:
      - targets:
          - 172.31.32.238:15692
          - 172.31.35.73:15692
          - 172.31.42.130:15692
EOF

# Create a Prometheus systemd service file
cat <<EOF | sudo tee /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus \\
  --config.file=/etc/prometheus/prometheus.yml \\
  --storage.tsdb.path=/var/lib/prometheus/

[Install]
WantedBy=multi-user.target
EOF

# Create Prometheus storage directory
sudo mkdir -p /var/lib/prometheus
sudo chown -R $USER:$USER /var/lib/prometheus

# Reload systemd, enable and start Prometheus
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus

# Verify Prometheus status
sudo systemctl status prometheus

echo "Prometheus setup complete! Access the UI at http://<your-ec2-public-ip>:9090"
