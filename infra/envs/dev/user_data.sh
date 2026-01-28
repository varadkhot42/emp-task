#!/bin/bash
yum update -y
yum install -y python3 git

pip3 install flask psycopg2-binary gunicorn

cd /home/ec2-user

# replace with your real repo
git clone https://github.com/YOUR_GITHUB_USERNAME/project.git
cd project/backend

export DB_HOST=task-postgres-db.c5iqs864ctd6.ap-south-1.rds.amazonaws.com
export DB_PORT=5432
export DB_NAME=taskdb
export DB_USER=postgres
export DB_PASSWORD=postgres123

gunicorn -b 0.0.0.0:5000 run:app
