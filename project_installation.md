# 🛠️ Installation Guide

### Steps to install and run the project.
#### [Step 1](#step-1-clone-the-repository-1): Clone the Repository
#### [Step 2](#step-2-Setup-the-environment): Setup the environment
- [Step 2.1](#Django-Configuration): Django Configuration
- [Step 2.2](#Neon-Configuration): Neon Configuration
- [Step 2.3](#TMD-Configuration): TMD Configuration
#### [Step 3](#step-3-install-the-required-modules-1) Install the Required Modules
#### [Step 4](#step-4-database-migrations-1): Database Migrations
#### [Step 5](#run-server): Run Server

---

## Step 1: Clone the repository
Clone the repository and using this command on terminal:
```commandline
git clone https://github.com/SmileyFaceZ/KU-Hub.git
```

---

## Step 2: Setup the Environment

### Get Environment Variables
Get the environment variables from the project owner and put it in the `.env` file.

#### Django Configuration

| Variable                               | Description                                                                        |
|:---------------------------------------|------------------------------------------------------------------------------------|
| `SECRET_KEY`                           | Used for cryptographic signing [Generate Secret Key](https://djecrety.ir/)         |
| `DEBUG`                                | Set `True` for development, `False` for actual use                                 |
| `ALLOWED_HOSTS`                        | List of strings representing the host/domain names that this Django site can serve |
| `TIME_ZONE`                            | Time zone                                                                          |                                                                          |

#### Neon Configuration

To get neon database url follow these steps.
1. Go to [NEON](https://neon.tech/) (Read [Documentation](https://neon.tech/docs/introduction))
2. Create a new project
3. Create a Database
4. Go to Dashboard and copy for python settings and put it in .env file in the root directory of the project

| Variable                            | Description                |
|:------------------------------------|----------------------------|
| `PGHOST`                            | Postgres Database Host     |
| `PGDATABASE`                        | Postgres Database Name     |
| `PGUSER`                            | Postgres Database User     |
| `PGPASSWORD`                        | Postgres Database Password |
| `PGPORT`                            | Postgres Database Port     |


#### TMD Configuration

To get TMD API key follow these steps.
1. Go to [TMD WEATHER FORECAST API](https://data.tmd.go.th/nwpapi/doc/main/getting_start.html)
2. Follow the instructions to get the API key
3. Put your API key in .env file in the root directory of the project

| Variable                            | Description                |
|:------------------------------------|----------------------------|
| `TMD_API_KEY`                       | The Movie Database API Key |

### Create a virtual environment and activate it
To create a virtual environment, run the following command:

```commandline
python -m venv venv
```

To activate the virtual environment, use one of the following commands:

Windows
```commandline
venv\Scripts\activate
```

macOS / Linux:
```commandline
source venv/bin/activate
```

---

## Step 3: Install the required modules

Installing the required `Python` modules by executing the following command:
```commandline
pip install -r requirements.txt
```

---

To verify that all modules are installed, run the following command:
```commandline
pip list
```

---

## Step 4: Database migrations

To create a new database, run the following command:
```commandline
python manage.py migrate
```
---

# 🚀 Running the project

## Run server

Launch the server, running the following command:
```commandline
python manage.py runserver
```
