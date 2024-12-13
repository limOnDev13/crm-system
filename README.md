# CRM system

## Description

A simple CRM system for working with clients. The system allows you to manage the services provided by the company, the advertising of these services, potential and active customers, contracts, as well as view various statistics. Access to different functions is delimited by permissions:

- The **administrator** can create, view and edit users, assign them roles and permissions. This functionality is implemented by the Django administrative panel.
- The **operator** can create, view and edit potential customers.
- The **marketer** can create, view and edit the services and advertising campaigns provided.
- The **manager** can create, view and edit contacts, view potential customers and transfer them to active ones.
- All roles can view the statistics of advertising campaigns.

## Visuals
![](demo.gif)

## Installation
**To launch the site**, it is enough to deploy a docker container. Before that, you need to create a file.env in the root of the project, following the example specified in .env.example. Next, it is enough to execute the ```docker compose up --build``` command from the root of the project.

**To download static files for the admin panel**, you need to log into the container with the application (open a new terminal, run the ```docker exec -ti <your-app-container-name> sh``` command - in my case ```docker exec -ti crm-system-app-1 sh```), go to the **/crm/crm** directory (where is the file located **manage.py** ) and execute the command ```python manage.py collectstatic```

**To add an administrator**, you need to go to the **/crm/crm** directory in the container with the application (where the file is located manage.py ) (**see above**) and execute the command ```python manage.py createsuperuser```, then enter the necessary data.

**To create a set of random data (products, advertisements, leads, customers and contracts)**, you need to go to the /crm/crm/ directory (where the file is located manage.py ) (**see above**) and execute the command ```python  manage.py create_random_data```

## Main links

- / - total statistics
- /products/ - list of services
- /ads/ - list of ads
- /leads/ - list of leads
- /customers/ - list of customers
- /accounts/login/ - login
- /admin/ - admin panel

## Technologies

- Django
- Postgres
- Docker
- Nginx
- gunicorn
