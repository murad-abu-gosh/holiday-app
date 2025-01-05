#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo systemctl enable docker

# pull docker image from hub
sudo docker pull vovhubdoc/frontend_container
sudo docker run -d -p 5000:5000 vovhubdoc/frontend_container

echo "running frontend_container..."


