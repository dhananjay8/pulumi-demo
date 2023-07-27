import pulumi
from pulumi_aws import ec2

from create_vpc import vpc, public_web_subnet_1, private_app_subnet_1, private_app_subnet_2

ami_id = 'ami-0f9ce67dcf718d332'  # Amazon Linux 2 AMI

# Create a new security group for web server
web_security_group = ec2.SecurityGroup(
    'my-jump-server-sg',
    vpc_id=vpc.id,
    ingress=[
        ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=80,
            to_port=80,
            cidr_blocks=['0.0.0.0/0'],
        ),
        ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=22,
            to_port=22,
            cidr_blocks=['0.0.0.0/0'],
        )
    ]
)

user_data = """
#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

# Create an Web EC2 instance
web_instance = ec2.Instance(
    'my-jump-server',
    instance_type='t2.micro',
    vpc_security_group_ids=[web_security_group.id],
    ami=ami_id,  # This is the ID for Amazon Linux 2
    subnet_id=public_web_subnet_1.id,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"EC2": "My jump server"}
)

# Create a new security group for app server
app_security_group = ec2.SecurityGroup(
    'my-app-server-sg',
    vpc_id=vpc.id,
    description='Enable SSH access from the specified server',
    ingress=[
        ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=22,
            to_port=22
        ),
        ec2.SecurityGroupIngressArgs(
        protocol='tcp',
        from_port=80,
        to_port=80,
        cidr_blocks=['0.0.0.0/0'],
    )
    ],
    egress=[
        ec2.SecurityGroupEgressArgs(
            protocol='-1',
            from_port=0,
            to_port=0,
            cidr_blocks=['0.0.0.0/0'],
        )
    ]
)

# Create an App EC2 instance
app_instance_1 = ec2.Instance(
    'my-app-server-1',
    instance_type='t2.micro',
    vpc_security_group_ids=[app_security_group.id],
    ami=ami_id,  # This is the ID for Amazon Linux 2
    subnet_id=private_app_subnet_1.id,
    # associate_public_ip_address=True,
    tags={"EC2": "My APP server 1"}
)

# Create an App EC2 instance
app_instance_2 = ec2.Instance(
    'my-app-server-2',
    instance_type='t2.micro',
    vpc_security_group_ids=[app_security_group.id],
    ami=ami_id,  # This is the ID for Amazon Linux 2
    subnet_id=private_app_subnet_2.id,
    # associate_public_ip_address=True,
    tags={"EC2": "My APP server 2"}
)

# Create an Elastic IP address and associate it with the instance
elastic_ip = ec2.Eip("web-eip", instance=web_instance.id)

# Export the public IP address to access the website
pulumi.export("website_ip", elastic_ip.public_ip)

# Export the instance ID
# pulumi.export('web_instance', web_instance.id)
# pulumi.export('app_instance_1', app_instance_1.id)
# pulumi.export('web_instance', web_instance.id)
