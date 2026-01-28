provider "aws" {
  region = "ap-south-1"
}

module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr                   = "10.1.0.0/16"
  public_subnet_cidr          = "10.1.1.0/24"
  private_subnet_cidr_az1     = "10.1.4.0/24"
  private_subnet_cidr_az2     = "10.1.3.0/24"
}

module "rds" {
  source            = "../../modules/rds"
  subnet_ids        = module.vpc.private_subnet_ids
  security_group_id = module.security.rds_sg_id
  db_password       = "postgres123"
}

module "security" {
  source   = "../../modules/security"
  vpc_id   = module.vpc.vpc_id
  vpc_cidr = module.vpc.vpc_cidr
  my_ip    = "27.107.110.182/32"
}

module "backend_ec2" {
  source    = "../../modules/ec2"

  ami_id    = "ami-0f5ee92e2d63afc18"
  subnet_id = module.vpc.public_subnet_id

  sg_id     = module.security.backend_sg_id
  key_name  = "varad-test"

  user_data = file("${path.module}/user_data.sh")
}


