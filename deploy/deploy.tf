

variable "frontend_ingress_rules" {
  type    = list(number)
  default = [22, 5000]
}

variable "db_ingress_rules" {
  type    = list(number)
  default = [22, 5001]
}

variable "gemini_ingress_rules" {
  type    = list(number)
  default = [22, 5002]
}

# secret manager port variable
variable "database_port" {
  default = 5001
}

variable "holiday_api_port" {
  default = 5002
}

# ec2
resource "aws_instance" "frontend_server" {
  ami                  = "ami-07d9cf938edb0739b"
  instance_type        = "t2.micro"
  key_name             = "frontkey"
  security_groups      = [aws_security_group.frontend_Server_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  tags = {
    Name = "frontend_Server"
  }
  user_data = file("frontend-script.sh")
}

resource "aws_instance" "db_server" {
  ami                  = "ami-07d9cf938edb0739b"
  instance_type        = "t2.micro"
  key_name             = "frontkey"
  security_groups      = [aws_security_group.db_Server_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  tags = {
    Name = "db_server"
  }
  user_data = file("db-script.sh")
}

resource "aws_instance" "gemini_server" {
  ami                  = "ami-07d9cf938edb0739b"
  instance_type        = "t2.micro"
  key_name             = "frontkey"
  security_groups      = [aws_security_group.gemini_Server_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  tags = {
    Name = "gemini_server"
  }
  user_data = file("gemini-script.sh")
}


# security group for frontend ec2
resource "aws_security_group" "frontend_Server_sg" {
  name        = "frontend-Traffic-sg"
  description = "Allow inbound traffic to frontend server"

  dynamic "ingress" {
    # iterator = port
    for_each = toset(var.frontend_ingress_rules)
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# security group for db ec2
resource "aws_security_group" "db_Server_sg" {
  name        = "db-Traffic-sg"
  description = "Allow inbound traffic to db server"

  dynamic "ingress" {
    # iterator = port
    for_each = toset(var.db_ingress_rules)
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# security group for gemini ec2
resource "aws_security_group" "gemini_Server_sg" {
  name        = "gemini-Traffic-sg"
  description = "Allow inbound traffic to gemini server"

  dynamic "ingress" {
    # iterator = port
    for_each = toset(var.gemini_ingress_rules)
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}



# define and attach iam role for each ec2 instance
resource "aws_iam_role" "ec2_iam_role" {
  name = "secret_manager_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "attach_secretsmanager" {
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  role       = aws_iam_role.ec2_iam_role.name
}

resource "aws_iam_role_policy_attachment" "attach_dynamodb" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  role       = aws_iam_role.ec2_iam_role.name
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2_instance_profile"
  role = aws_iam_role.ec2_iam_role.name

}


# create secret manager 
resource "aws_secretsmanager_secret" "holiday_secret" {
  name        = "holiday_secret"
  description = "Contains API key for Gemini and URLs for DB and API Handlers"
}

resource "aws_secretsmanager_secret_version" "holiday_ips" {
  secret_id = aws_secretsmanager_secret.holiday_secret.id

  secret_string = jsonencode({
    AWS_REGION           = "us-west-2"
    GEMINI_API_KEY       = "AIzaSyCm97Bj5ZXfmKWeh7KpL0wL80uom6afAUE"
    DATABASE_HANDLER_URL = format("http://%s:%d", aws_instance.db_server.private_ip, var.database_port)
    HOLIDAY_API_URL      = format("http://%s:%d", aws_instance.gemini_server.public_ip, var.holiday_api_port)
  })
}


output "frontend-ip" {
  value = aws_instance.frontend_server.public_ip
}
output "db-ip" {
  value = aws_instance.db_server.private_ip
}
output "gemini-ip" {
  value = aws_instance.gemini_server.public_ip

}
