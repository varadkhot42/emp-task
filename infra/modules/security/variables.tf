variable "vpc_id" {
  description = "VPC ID where security group will be created"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC"
  type        = string
}

variable "my_ip" {
  description = "Your public IP in CIDR format (x.x.x.x/32)"
  type        = string
}
