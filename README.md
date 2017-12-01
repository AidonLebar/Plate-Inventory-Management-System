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
TODO

## Automatic Deployment

1. **ALWAYS** thoroughly test new changes to make sure nothing is broken before deploying.

2. Merge the working branch into the `master` branch.

3. Tag the release with a new version tag, something like `production-v0.10.0`. This will trigger a continuous
integration job which will deploy the tagged version of the software.

4. Merge changes from the origin `master` branch back into the working branch (including the merge commit) to continue
development.
