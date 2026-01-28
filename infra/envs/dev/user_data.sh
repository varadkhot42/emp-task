#!/bin/bash
yum update -y
yum install -y python3 git

pip3 install flask psycopg2-binary gunicorn

cd /home/ec2-user
git clone https://github.com/varadkhot42/emp-task.git
cd emp-task/backend

export DB_HOST=task-postgres-db.c5iqs864ctd6.ap-south-1.rds.amazonaws.com
export DB_PORT=5432
export DB_NAME=taskdb
export DB_USER=postgres
export DB_PASSWORD=postgres123

gunicorn -b 0.0.0.0:5000 run:app
