# Django Ecommerce APIs
Very basic Django ecommerce project, with integrated Razorpay.
User can Register, login, list products, add to cart and order COD and Pre-Paid orders.

## Setup
1) Create a directory/folder of any name. Eg: django-ecom-api
2) Go into the directory you created in step 1 and clone the project by running the following command  
`git clone https://github.com/haywiregod/django-ecom-API.git .`
3) Create  and then activate virtual environment. (You can use `virtualenv`)
4) Install requirements in the virtual environment using `pip install -r requirements.txt`
5) Copy `env.example` to `.env`
6) Create a database in your mysql
7) Set the database name you created in step 6 in `.env` file by entering `DATABASE_NAME=YOUR_DATABSE_NAME_HERE`
8) Similary set other values according to your mysql connection
`DATABASE_USER=root`
`DATABASE_PASSWORD=`  
`DATABASE_HOST=localhost`
`DATABASE_PORT=3306`
9) Get your Razorpay Key ID and keys by signing up at razorpay.com and add them in `.env` file.
9) Make Migrations by running `python manage.py makemigrations`
10) Migrate all tables by running `python manage.py migrate`

## How to run?
1) Simply activate your virtual environment if not already activated.
2) Run `python manage.py runserver`