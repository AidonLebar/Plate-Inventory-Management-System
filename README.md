# Plate Inventory Management System (PIMS)
An system for McGill's Plate Club to manage their inventory.
## Developing
### Setting Up the Environment

1. Clone the repository:
```bash
git clone https://gitlab.science.mcgill.ca/ctf-general/plate-club-inventory.git
```

2. Install virtualenv (if you haven't already):
```bash
pip install virtualenv
```

3. Set up a virtual environment with Python 3:
```bash
virtualenv -p python3 env
```

4. Start virtual environment:
 ```bash
source env/bin/activate
```

5. Switch branch to dev:
```bash
git checkout dev
```

6. Install the dependencies:
```bash
pip install -r requirements.txt
```

7. Start the development server
```bash
python manage.py runserver
```

## Deploying by Hand

1. **Use Automated Deployment whenever possible!**

2. SSH into the `lockers` server.

3. Download a stable tagged version or an archive of the master for a possibly non-functional snapshot.

4. Move the code into the deployment folder. On the current `lockers` server, this is located at
   `/home/django/locker_distribution/`.

5. Run the following `bash` commands to set permissions, install dependencies, and migrate the database:
```bash
cd /home/django/
sudo chmod 770 ./locker_distribution/*
sudo chown -R gitlab-runner:django-users ./locker_distribution/*
cd ./locker_distribution
virtualenv venv_locker_distribution -p python3
source venv_locker_distribution/bin/activate
pip3 install -r requirements.txt
python3 ./manage.py migrate
python3 ./manage.py collectstatic
touch reload.trigger
deactivate
```

6. Check that the changes have been successfully deployed.

7. Exit the SSH session with `exit`.

## Automatic Deployment

1. **ALWAYS** thoroughly test new changes to make sure nothing is broken before deploying.

2. Merge the working branch into the `master` branch.

3. Tag the release with a new version tag, something like `production-v0.10.0`. This will trigger a continuous
integration job which will deploy the tagged version of the software.

4. Merge changes from the origin `master` branch back into the working branch (including the merge commit) to continue
development.
