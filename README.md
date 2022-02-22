# cloudomatic

# python code to provision resources on g42cloud.com, this uses the rest APIs to manage cloud resources 

# Deployement
python 3 , install in a venv and pip install the moudles required 

# python modules required

requests


# Usage 

1. Create an VM , image ID needs to prepopulated in the config.py file 

python3 ecs.py --create <vmname> --flavour <flavourname>

2. Delet a VM 

python3 ecs.py --delete <vmname>
