# Plate Club Inventory
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

## Deployment

TODO
