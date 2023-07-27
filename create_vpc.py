import pulumi
from pulumi_aws import ec2

vpc = ec2.Vpc("my_vpc",
              cidr_block="172.20.0.0/20",
              instance_tenancy="default",
              tags={
                  "Name": "my-vpc",
              })

# Create the web public subnets
public_web_subnet_1 = ec2.Subnet('my-public-web-subnet-1',
    vpc_id=vpc.id,
    cidr_block='172.20.1.0/24',
    map_public_ip_on_launch=True,  # enables public IP on instances in this subnet
    availability_zone='us-east-1a')

public_web_subnet_2 = ec2.Subnet('my-public-web-subnet-2',
    vpc_id=vpc.id,
    cidr_block='172.20.2.0/24',
    map_public_ip_on_launch=True,  # enables public IP on instances in this subnet
    availability_zone='us-east-1b')

public_web_subnet_3 = ec2.Subnet('my-public-web-subnet-3',
    vpc_id=vpc.id,
    cidr_block='172.20.3.0/24',
    map_public_ip_on_launch=True,  # enables public IP on instances in this subnet
    availability_zone='us-east-1c')
    
# Create the app private subnets
private_app_subnet_1 = ec2.Subnet('my-private-app-subnet-1',
    vpc_id=vpc.id,
    cidr_block='172.20.4.0/24',
    availability_zone='us-east-1a')

private_app_subnet_2 = ec2.Subnet('my-private-app-subnet-2',
    vpc_id=vpc.id,
    cidr_block='172.20.5.0/24',
    availability_zone='us-east-1b')

private_app_subnet_3 = ec2.Subnet('my-private-app-subnet-3',
    vpc_id=vpc.id,
    cidr_block='172.20.6.0/24',
    availability_zone='us-east-1c')

# Create the DB private subnets
private_db_subnet_1 = ec2.Subnet('my-private-db-subnet-1',
    vpc_id=vpc.id,
    cidr_block='172.20.7.0/24',
    availability_zone='us-east-1a')

private_db_subnet_2 = ec2.Subnet('my-private-db-subnet-2',
    vpc_id=vpc.id,
    cidr_block='172.20.8.0/24',
    availability_zone='us-east-1b')

private_db_subnet_3 = ec2.Subnet('my-private-db-subnet-3',
    vpc_id=vpc.id,
    cidr_block='172.20.9.0/24',
    availability_zone='us-east-1c')


# Create a public web route table
web_route_table = ec2.RouteTable('my-public-web-route-table',
    vpc_id=vpc.id
)
# Create a private route table
app_route_table = ec2.RouteTable('my-private-app-route-table',
    vpc_id=vpc.id
)
# Create a private route table
db_route_table = ec2.RouteTable('my-private-db-route-table',
    vpc_id=vpc.id
)

# Associate the route table with the web subnets
web_association1 = ec2.RouteTableAssociation('my-web-route-table-association-1',
                                         subnet_id=public_web_subnet_1.id,
                                         route_table_id=web_route_table.id)
                                         
web_association2 = ec2.RouteTableAssociation('my-web-route-table-association-2',
                                         subnet_id=public_web_subnet_2.id,
                                         route_table_id=web_route_table.id)

web_association3 = ec2.RouteTableAssociation('my-web-route-table-association-3',
                                         subnet_id=public_web_subnet_3.id,
                                         route_table_id=web_route_table.id)
# Associate the route table with the app subnets
app_association1 = ec2.RouteTableAssociation('my-app-route-table-association-1',
                                         subnet_id=private_app_subnet_1.id,
                                         route_table_id=app_route_table.id)
                                         
app_association2 = ec2.RouteTableAssociation('my-app-route-table-association-2',
                                         subnet_id=private_app_subnet_2.id,
                                         route_table_id=app_route_table.id)

app_association3 = ec2.RouteTableAssociation('my-app-route-table-association-3',
                                         subnet_id=private_app_subnet_3.id,
                                         route_table_id=app_route_table.id)
# Associate the route table with the db subnets
db_association1 = ec2.RouteTableAssociation('my-route-table-association-1',
                                         subnet_id=private_db_subnet_1.id,
                                         route_table_id=db_route_table.id)
                                         
db_association2 = ec2.RouteTableAssociation('my-route-table-association-2',
                                         subnet_id=private_db_subnet_2.id,
                                         route_table_id=db_route_table.id)

db_association3 = ec2.RouteTableAssociation('my-route-table-association-3',
                                         subnet_id=private_db_subnet_3.id,
                                         route_table_id=db_route_table.id)

# Export IDs of the created resources
pulumi.export('vpcId', vpc.id)

# pulumi.export('subnetId1', public_web_subnet_1.id)
# pulumi.export('subnetId2', public_web_subnet_2.id)
# pulumi.export('subnetId3', public_web_subnet_3.id)
# pulumi.export('subnetId4', private_app_subnet_1.id)
# pulumi.export('subnetId5', private_app_subnet_2.id)
# pulumi.export('subnetId6', private_app_subnet_3.id)
# pulumi.export('subnetId7', private_db_subnet_1.id)
# pulumi.export('subnetId8', private_db_subnet_2.id)
# pulumi.export('subnetId9', private_db_subnet_3.id)

# pulumi.export('RouteTableId1', web_route_table.id)
# pulumi.export('RouteTableId2', app_route_table.id)
# pulumi.export('RouteTableId3', db_route_table.id)

# pulumi.export('web_association1', web_association1.id)
# pulumi.export('web_association2', web_association2.id)
# pulumi.export('web_association3', web_association3.id)
# pulumi.export('app_association1', app_association1.id)
# pulumi.export('app_association2', app_association2.id)
# pulumi.export('app_association3', app_association3.id)
# pulumi.export('db_association1', db_association1.id)
# pulumi.export('db_association2', db_association2.id)
# pulumi.export('db_association3', db_association3.id)
