

variable "ingressrules" {
  type = list(number)
  default = [ 22, 443, 80, 5000 ]
}

variable "egressrules" {
  type =  list(number)
  default = [ 80, ]
}


resource "aws_instance" "frontend_server" {
  ami             = "ami-07c5ecd8498c59db5"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.frontend_Server_sg.name]

  tags = {
    Name = "frontend_Server"
  }
  user_data = file("server-script.sh")  
}


# create security group
resource "aws_security_group" "frontend_Server_sg" {
  name = "Allow Web Traffic"
  description = "Allow custom ports including port 5000"

  dynamic "ingress" {
    # iterator = port
    for_each = var.ingressrules
    content {
      from_port = ingress.value
      to_port = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    } 
  }

   dynamic "egress" {
    iterator = port
    for_each = var.egressrules
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}