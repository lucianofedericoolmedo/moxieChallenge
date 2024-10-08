# Challenge Moxie by Luciano Olmedo

## Prerequisites

The following dependencies are expected to be installed:

- [Python 3.11 at least][python]
- [Pip][pip]
- [Docker][docker]


## STEP BY STEP PROCESS

### Clone the repository:
    ```bash
    git clone https://github.com/lucianofedericoolmedo/ChallengeMoxie
    ```

### All in One process (tested on Linux, equivalent up to step 11 of manual process)

After you install Docker you can spin up an instance of a postgres db like this, assuming db name as moxie, and username postgres:
Please replace YOUR_SECRET_PASSWORD with the password you want to use. 
    ```bash
    scripts/setup.sh
    ```  

TO supply step 12: You can (after you see the project on), open a second terminal, navigate to the source main folder, enter the virtualenv and run the second one.
    ```bash
    scripts/create_super_user.sh
    ```  


### More Manual process
After that, follow these steps for database setup:
1. Navigate into the project directory:
    ```bash
    cd moxie
    ```

2. Enter docker:
    ```bash
    docker compose -d up
    ```

3a. If the `postgres` user does not exist, enter docker, create a new user named `postgres` with password `postgres`:
    ```sql
    CREATE USER postgres WITH PASSWORD 'YOUR_SECRET_PASSWORD';
    ```
4b.  If the `postgres` user already exists, set the password for this user to 'postgres':
    ```sql
    ALTER USER postgres WITH PASSWORD 'YOUR_SECRET_PASSWORD';
    ```

5. Create a database (if necessary) named `moxie` owned by the `postgres` user:
    ```sql
    CREATE DATABASE moxie OWNER postgres;
    ```

6. Exit the PostgreSQL shell:
    ```bash
    \q
    ```

7. Create your virtual environment, Here we are assuming `myEnv`:
    ```bash
    python3 -m venv myEnv
    ```

8. Enter it:
    ```bash
    source myEnv/bin/activate
    ```

(Optional step, not needed for simple testing). Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
   Open the `.env` file and replace the placeholders with the appropriate values.

9. Run the dependencies:
    ```bash
    pip -r requirements.txt
    ```
10. Run the migrations:
    ```bash
    python manage.py migrate
    ```

11. Run the project:
    ```bash
    python manage.py runserver
    ```

12. On another tab in same folder, create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
13. Access the application by clicking on the following link: [`localhost:8000`](http://localhost:8000). The following response should be seen:
    ```
    {"status": "Running !"}
    ```
14. Access the admin tool by clicking on the following link: [`localhost:8000/admin`](http://localhost:8000/admin).


## IMPORTANT PRIOR TO API USE

Prior to using the API you need to create at least a single med spa. It is a prerequisite.
There is no endpoint for this. To create a dummy one, you can search for the create_dummy_mda_spa in the examples folder.
If you want something more customize you can also enter the , you can create it by using the [admin tool](http://localhost:8000/admin/med-spa/list).

The list of available endpoints is in [localhost:8000/docs](http://localhost:8000/docs).

In order to test the endpoints, you can use whatever tool you feel ok with but I include some examples that are in the api/docs/EXAMPLE_REQUESTS.md file.


## What this project does not, and why

All of them due to time constraints.

### No Authentication Required

**Assumption:** NO API authentication or user tracking: Since it is not initially required, it is not there.

**Why?**: Showing CRUD functionality and the relationships between entities rather than securing those operations. 

### Standard Business Hours and Timezone

**Assumption**: Med spas work from 9:00 AM to 6:00 PM.

**Why?**: the assignment does not provide specifics on operating hours or timezone management, so assuming standard business hours simplifies scheduling, availability checks, and conflict management, avoiding the complexities of handling various timezones or extended hours.

### Unlimited Availability of Services

**Assumption**: All services offered by the med spas are available without
constraints of inventory or availability slots, also duration is expressed in minutes.

**Why?**: Avoid implementing inventory or slot management systems.

### Not tracking the dependencies of services product with categories or service product supplier

**Assumption**: Did not establish validations for given a service. For instance: Neuromodulator (type), Restylane (product) seems to be invalid in the excel sheet and is a valid in this model. A better solution should take this into consideration but I am not due to time.

**Why?**: Avoid implementing inventory or slot management systems.

[docker]: https://www.docker.com/
[python]: https://www.python.org/
[pip]: https://pypi.org/project/pip/