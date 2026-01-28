variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
}

variable "private_subnet_cidr_az1" {
  description = "CIDR block for private subnet in AZ1"
  type        = string
}

variable "private_subnet_cidr_az2" {
  description = "CIDR block for private subnet in AZ2"
  type        = string
}
