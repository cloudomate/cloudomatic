host1="rancher-bastion"
ipaddr=$(python3 ecs.py -a $host1)
echo "ip addr is : "$ipaddr