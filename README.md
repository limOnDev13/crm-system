# CRM system

## Description

A simple CRM system for working with clients. The system allows you to manage the services provided by the company, the advertising of these services, potential and active customers, contracts, as well as view various statistics. Access to different functions is delimited by permissions:

- The **administrator** can create, view and edit users, assign them roles and permissions. This functionality is implemented by the Django administrative panel.
- The **operator** can create, view and edit potential customers.
- The **marketer** can create, view and edit the services and advertising campaigns provided.
- The **manager** can create, view and edit contacts, view potential customers and transfer them to active ones.
- All roles can view the statistics of advertising campaigns.

## Visuals

## Installation
To launch the site, it is enough to deploy a docker container. Before that, you need to create a file.env in the root of the project, following the example specified in .env.example. Next, it is enough to execute the ```docker compose up --build``` command from the root of the project. 

A superadmin with the **admin** username and password **123** is added to the database. This will allow you to log in to the admin panel (<ins>http://yourhost:yourport/admin/</ins>). Through it, you can add other users and grant them access rights.

The main links of the site:

- / - total statistics
- /products/ - list of services
- /ads/ - list of ads
- /leads/ - list of leads
- /customers/ - list of customers
- /accounts/login/ - login
- /admin/ - admin panel
