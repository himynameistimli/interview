# interview

## Installation

* create virtualenv and install requirements.txt
* python manage.py makemigrations ; python manage.py migrate
* sudo -u postgres psql
* create database interview
* create user interview with password 'interview'
* grant all privileges on database interview to interview;
* \q
* python manage.py makemigrations ; python manage.py migrate ;
* python manage.py create_demo_users (to create demo users and make them friends of each other)
* python manage.py populate_products (picks first user created and enter product details and assigns first user as
  seller)
* 4 users are created user1@gmail.com,user2@gmail.com,user3@gmail.com,user4@gmail.com with password <strong>Password@123</strong>
* python manage.py runserver

## Flow

* Log in
* Users will see all prouct list , if user itself is the owner of product then he should see option of edit
* any user can add product
* only product list and details page are implemented
* When product details is viewed it's is added to the UserProductView table and user's friends will see those product as
  recommendations, however this can be improved like based on specific product or product category

* Log files are not configured since it is demo only  
