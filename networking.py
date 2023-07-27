import pulumi
from pulumi_aws import ec2

from create_vpc import vpc, public_web_subnet_1, web_route_table, app_route_table, db_route_table

# Create an Internet Gateway and attach it to the VPC
web_internet_gateway = ec2.InternetGateway(
    "my-web-internet-gateway",
    vpc_id=vpc.id,
)

# Create an Elastic IP
eip = ec2.Eip('nat-eip')

# Creating a NAT Gateway and associate it with the newly created Elastic IP and Public Web Subnet
nat_gateway = ec2.NatGateway(
    'my-nat-gateway',
    subnet_id=public_web_subnet_1.id,
    allocation_id=eip.id
)

# Add a route to the Web Route Table that points all traffic to the Internet Gateway
web_route = ec2.Route(
    'web-route',
    destination_cidr_block='0.0.0.0/0',
    gateway_id=web_internet_gateway.id,
    route_table_id=web_route_table.id
)

# Add a route to the App Route Table that points all traffic to the NAT Gateway
app_route = ec2.Route(
    'app-route',
    destination_cidr_block='0.0.0.0/0',
    gateway_id=nat_gateway.id,
    route_table_id=app_route_table.id
)

# Add a route to the DB Route Table that points all traffic to the NAT Gateway
db_route = ec2.Route(
    'db-route',
    destination_cidr_block='0.0.0.0/0',
    gateway_id=nat_gateway.id,
    route_table_id=db_route_table.id
)


# Export the Internet Gateway name
# pulumi.export('web_internet_gateway_name', web_internet_gateway.id)

# Export the NAT Gateway name
# pulumi.export('nat_gateway_name', nat_gateway.id)