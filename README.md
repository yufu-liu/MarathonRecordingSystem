# Marathon System
> reference : [HackMD](https://hackmd.io/8wvVDF9RQVaYyxSAl-8O_w?both)

## How to construct a backend service (Django + MySQL) with Docker
Step 1. Clone or Download the Project
git clone git@gitlab.com:chiashengchen/marathon-system.git
cd <your_project_directory> (where docker related files and manage.py are)

Step 2. Run docker-compose up:
docker-compose up --build

Step 3. Apply Migrations
docker-compose exec web python manage.py migrate

Step 4. Stop the Services
docker-compose down

If you need to view or modify the database directly, they can connect to the MySQL container from the terminal using the following command:
docker-compose exec db mysql -u root -p




