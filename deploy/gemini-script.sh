#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo systemctl enable docker

# pull docker image from hub
sudo docker pull vovhubdoc/api_container
sudo docker run -d -p 5002:5002 vovhubdoc/api_container

echo "running api_container..."
