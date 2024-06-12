import boto3

def generate_ansible_inventory(tags_list):
    
    #Generate dynamic inventory for AWS EC2 instances based on tag list
    ec2_client = boto3.client('ec2')

    # Query AWS for running EC2 instances with the specified tags
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    for tag_key, tag_value in tags_list.items():
        filters.append({'Name': f'tag:{tag_key}', 'Values': [tag_value]})

    inst_resp = ec2_client.describe_instances(Filters=filters)

    # Initialize inventory structure
    inventory = {}

    # Populate inventory with EC2 instances
    for reservation in inst_resp['Reservations']:
        for instance in reservation['Instances']:
            public_ip = instance.get('PublicIpAddress', 'N/A')

            # Add instance to inventory groups based on 'Name' tag
            if 'Name' in tags_list:
                group_name = tags_list['Name']
                if group_name not in inventory:
                    inventory[group_name] = []
                inventory[group_name].append(public_ip)

    return inventory

def write_inventory_to_file(inventory, filename='/home/mostafa/MultiCloudDevOpsProject/Ansible/inventory'):

    # Write the generated inventory to a file.

    with open(filename, 'w') as inventory_file:
        inventory_file.write("# Generated Ansible inventory\n" )
        for group, hosts in inventory.items():
            inventory_file.write( f"[{group}]\n" )
            for host in hosts:
                inventory_file.write( f"{host}\n" )
            inventory_file.write("\n")

if __name__ == '__main__':
    # List of instance tags for which the inventory should be generated
    instance_tags = {'Name': 'ivolve'}

    # Generate AWS inventory based on specified tags
    inventory = generate_ansible_inventory(instance_tags)

    # Write inventory to file
    write_inventory_to_file(inventory)
    print("Done.")
