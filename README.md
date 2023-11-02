hanwooplz
=============
Portfolio website project for developers
-------------
### Backend Developer Bootcamp Oreumi 2nd generation by EstSoft

## Before you starts

This project is based on python and django framework, so please install:
```sh
sudo apt install python3 python3-pip python3-venv
```

## How to start

First of all, clone this repository in your space:
```sh
git clone https://github.com/hwan3526/hanwooplz.git ~
```

Set your Python virtual environment with `venv`:
```sh
python3 -m venv ~/hanwooplz/hanwooplz_env
```

Activate generated venv and install all requiring packages:
```sh
cd ~/hanwooplz
. hanwooplz_env/bin/activate
pip3 install -r requirements.txt
```

Copy your TinyMCE static folder into static folder:
```sh
cd ~/hanwooplz
chmod 744 tinymce_setup.sh
./tinymce_setup.sh
```

Do not forget create `secrets.json` in `hanwooplz_project/hanwooplz_project` directory

## How to set PostgreSQL database using AWS RDS

Please refer the following link: [How to set PostgreSQL on AWS RDS](https://velog.io/@server30sopt/AWS-AWS-rds-postgreSQL-환경세팅)

After creating and matching AWS RDS, run the following commands to create database:
```sh
cd ~/hanwooplz/hanwooplz_project
python3 manage.py makemigrations
python3 manage.py migrate
```

## How to test run

Run the following command:
```sh
cd ~/hanwooplz/hanwooplz_project
python3 manage.py runserver
```

You can get into website on http://localhost:8000

## Get set AWS EC2 and for running uWSGI and nginx

[Series: How to set AWS EC2 instance in addition to uWSGI and nginx](https://nerogarret.tistory.com/45)
[How to apply SSL on AWS EC2](https://velog.io/@wijoonwu/AWS-EC2에-SSL-적용하기-Feat.-ACM-Route53-ALB-Nginx)
[How to redirect HTTP requests to HTTPS](https://medium.com/@yangga0070/aws-로드밸런서-http-https-리다이렉션-37c1039be0ab)

Even this is explained on the links above, after install uWSGI and nginx, you should copy configuration files and restart daemons:
```sh
sudo ln -f ~/hanwooplz/hanwooplz_project/hanwooplz_project/.config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service
sudo systemctl daemon-reload
sudo systemctl enable uwsgi
sudo systemctl restart uwsgi
sudo cp -f ~/hanwooplz/hanwooplz_project/hanwooplz_project/.config/nginx/hanwooplz_project.conf /etc/nginx/sites-available/hanwooplz_project.conf
sudo ln -sf /etc/nginx/sites-available/hanwooplz_project.conf /etc/nginx/sites-enabled/hanwooplz_project.conf
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload
sudo systemctl restart uwsgi nginx
```

## How to set GitHub Actions

You can set auto deployment by configuring GitHub Actions.

Please refer the below link to set auto deployment: [How to set GitHub Actions](https://iamjooon2.tistory.com/25)