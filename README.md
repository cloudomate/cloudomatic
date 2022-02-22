# python code to provision resources on g42cloud, this uses the rest APIs to manage cloud resources 

# Deployment
python 3 , install in a venv and pip install the moudles required 

# modules required

requests


# Usage 

1. Create an VM , image ID needs to prepopulated in the config.py file 

python3 ecs.py --create <vmname> --flavour <flavourname>

2. Delet a VM 

python3 ecs.py --delete <vmname>
