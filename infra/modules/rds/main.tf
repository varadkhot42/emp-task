resource "aws_db_subnet_group" "this" {
  name       = "task-db-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "this" {
  identifier              = "task-postgres-db"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  db_name                 = "taskdb"
  username                = "postgres"
  password                = var.db_password
  publicly_accessible     = false
  skip_final_snapshot     = true
  vpc_security_group_ids  = [var.security_group_id]
  db_subnet_group_name    = aws_db_subnet_group.this.name
}

variable "subnet_ids" {}
variable "security_group_id" {}
variable "db_password" {}

output "db_endpoint" {
  value = aws_db_instance.this.address
}
