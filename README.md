# CSC648 Section 04 Team 206
## Members
| Name                   | Email                  | Role             |
|------------------------|------------------------|------------------|
| Phyo Thein Htut        | phtut@mail.sfsu.edu    | Lead             |
| Eduardo Alexis Ramos   | eramos4@mail.sfsu.edu  | Frontend (UI/UX) |
| Myles Pedronan         | mpedrona@mail.sfsu.edu | Backend Lead     |
| Antonio Damaso Carmona | acarmona@mail.sfsu.edu | Git & DB Master  |
| Zijie (Jason) Wei      | zwei@mail.sfsu.edu     | Frontend Lead    |

# Project Summary


For most hobbyists, web-surfing for Do-It-Yourself (DIY) projects can sometimes be difficult since they are all scattered all over the internet. We believed that it would be nice if there were a large hub of DIY projects, and as a result, the idea for DIYup was born. With DIYup, guests and creators alike can browse and upload their own step-by-step DIY tutorials. Creator or not, our site makes it easy for anyone to pick up a variety of projects and follow step-by-step instructions with pictures to easily complete their project. Users can easily browse through the hottest projects on our site and sort depending on the difficulty or on the category of the project to suit their interests and level of building knowledge. Becoming a registered user comes with its own perks. As a registered user, users can become authors and upload their own projects, share their experience making a project from our site, rate, and save their favorite projects. As an author, authors can view and respond to comments to posts they’ve made as well as edit their original post in case of any typos or other errors. Any posts that are reported and found to be violating our site’s rules will be deleted by site administrators. With site administrators there will be a team looking at reported posts to ensure users follow our site’s rules and guidelines in order for our users to have the most enjoyable experience.


# Server URL: http://54.67.109.241/


# Running and Installation Guide
## Frontend
### Dependencies
* Node >= 8.9.0
* npm >= 5.6.0
* Apache >= v2.4.0
```sh
# instruction on how to install Apache2.0 and start
https://phoenixnap.com/kb/how-to-install-apache-web-server-on-ubuntu-18-04
```

#### Deploying the Single-Page Application to Server
**Note:** It is important the aforementioned dependencies are installed prior to proceeding.

If all the dependecies are installed, run the following commands from the root from your AWS or host machine.

```sh
$ git clone https://github.com/CSC-648-SFSU/csc648-04-fa19-Team206.git
$ cd csc648-04-fa19-Team206
$ sudo cp -r application/frontend/dist/spa/. /var/www/html/
```

You have just sucessfully deploy the frontend on our server.

## Backend
* Python >= v3.5.0
* MySQL v5.7.27
```sh
# instruction on how to install MySQL Workbench
https://dev.mysql.com/doc/workbench/en/wb-installing-windows.html
```

#### Running the backend

1. Navigate into csc648-04-fa19-Team206/application/backend
2. Run:
```sh
$ pip3 install -r requirements.txt
$ nohup python3 run.py &
```

#### Accessing the existing MySQL Server directly

1. Run MySQL Workbench
2. Navigate to Database > Connect to Database
3. Use the following parameters to connect:
```sh
Hostname: 54.67.109.241
Port: 3306
Username: admin
Default Schema: diyup
```
4. Click "OK" and enter the following password:
```sh
Password: team206pass
```
5. Click "OK" to connect
