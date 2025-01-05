#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo systemctl enable docker

# pull docker image from hub
sudo docker pull vovhubdoc/db_container
sudo docker run -d -p 5001:5001 vovhubdoc/db_container

echo "running db_container..."



