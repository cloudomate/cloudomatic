# Python code to provision resources on g42cloud, this uses the rest APIs to manage cloud resources 

# Deployment
python 3 , install in a venv and pip install the moudles required 

# Modules required
requests

# Usage 
0. Update the paramameters in config-example.py file and rename it to config.py

1. Create an VM , image ID needs to prepopulated in the config.py file 

   python3 ecs.py --create testvm --flavour s6.xlarge

2. Delete a VM 

   python3 ecs.py --delete testvm
