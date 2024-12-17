#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# pull docker image from hub
sudo docker pull vovhubdoc/frontend_container
sudo docker run -p 5000:5000 frontend_container

echo "running frontend_container..."







