terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region     = var.region
}

resource "aws_key_pair" "deployer" {
  key_name   = var.name
  public_key = var.public_key
}
resource "aws_instance" "bot_telegram" {
  ami                    = data.aws_ami.ami.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.deployer.id
  vpc_security_group_ids = [aws_security_group.tb.id]

  user_data = templatefile("telegram_bot_lite.sh.tpl",
    {
      TOKEN        = var.TOKEN
      ManheimLogin = var.ManheimLogin
      ManheimPass  = var.ManheimPass
      REDIS_PASS   = var.REDIS_PASS
      ADMIN_ID     = var.ADMIN_ID
      CopartURL    = var.CopartURL
    }
  )
  tags = {
    Name = var.name
  }

}

data "aws_availability_zones" "avbz" {}

data "aws_ami" "ami" {
  owners      = ["099720109477"]
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }
}



resource "aws_security_group" "tb" {
  name = var.name

  dynamic "ingress" {
    for_each = ["443", "22"]
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = var.name
  }
}
