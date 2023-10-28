provider "aws" {
  access_key = "<your-access-key>"
  secret_key = "<your-secret-key>"
  region     = "eu-central-1"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }
}

module "security_group" {
  source              = "terraform-aws-modules/security-group/aws"
  name                = "image-compressor-aws-modules-sg"
  description         = "Security group made using an AWS module"
  vpc_id              = data.aws_vpc.default.id
  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "all-icmp", "ssh-tcp"]
  egress_rules        = ["all-all"]
}

module "ec2" {
  source                      = "terraform-aws-modules/ec2-instance/aws"
  name                        = "image-compressor-aws-modules-ec2"
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t2.micro"
  key_name                    = "flask-app"
  subnet_id                   = tolist(data.aws_subnets.all.ids)[0]
  vpc_security_group_ids      = [module.security_group.security_group_id]
  associate_public_ip_address = true
  user_data                   = file("./provision.sh")
}
