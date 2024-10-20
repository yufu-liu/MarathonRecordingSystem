# Marathon Recording System
## Features
1. APIs for initiating marathons, racers, checkpoints, final results.
2. Tables for marathon, racers, stations, checkpoints of each stations and racers, a summary.
3. Package this service with Docker for deployment. 

## Note
This repository focus on backend service (Django and MySQL), if you want to know more about the whole system or frontend (PC and RFID).
- For more details:
> reference : [HackMD](https://hackmd.io/8wvVDF9RQVaYyxSAl-8O_w?both)

## How to construct a backend service (Django + MySQL) with Docker
Step 1. Clone or Download the Project
git clone git@gitlab.com:chiashengchen/marathon-system.git

Step 2. Go to the directory
cd <your_project_directory> (where docker related files and manage.py are)

Step 3. Run docker-compose up:
docker-compose up --build

Step 4. Apply Migrations
docker-compose exec web python manage.py migrate

Step 5. Stop the Services
docker-compose down

If you need to view or modify the database directly, they can connect to the MySQL container from the terminal using the following command:
docker-compose exec db mysql -u root -p




