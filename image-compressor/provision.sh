#!/usr/bin/env bash

# Setup project
sudo yum update -y
sudo yum install -y python3-pip git
sudo mkdir /app && cd /app
sudo git clone https://github.com/k1lgor/image-compressor.git
sudo chown -R ec2-user:ec2-user image-compressor
cd image-compressor
python3 -m venv venv
source venv/bin/activate
pip3 install pip3 -U
pip3 install -r requirements.txt --no-cache-dir
# nohup gunicorn -w 4 -b 0.0.0.0:8000 app:app &

# Setup systemd service
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn daemon to serve Image Compressor
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/app/image-compressor
ExecStart=/app/image-compressor/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable gunicorn --now

# Setup NGINX
sudo amazon-linux-extras install -y nginx1
sudo systemctl enable nginx --now
sudo tee /etc/nginx/conf.d/gunicorn.conf > /dev/null <<EOF
server {
  listen 80;
  server_name .compute.amazonaws.;

  location / {
    proxy_pass  http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
EOF

sudo systemctl restart nginx
