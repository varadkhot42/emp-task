resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "task-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = "ap-south-1a"
}

resource "aws_subnet" "private_az1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnet_cidr_az1
  availability_zone = "ap-south-1a"
}

resource "aws_subnet" "private_az2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnet_cidr_az2
  availability_zone = "ap-south-1b"
}
