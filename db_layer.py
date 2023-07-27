from mysql_dynamic_provider import *
import pulumi
from pulumi_aws import rds, ec2
import pulumi_mysql as mysql

from create_vpc import \
    vpc, private_db_subnet_1, private_db_subnet_2, private_db_subnet_3
from service_layer import app_security_group


# Get neccessary settings from the pulumi config
config = pulumi.Config()
admin_name = config.require("sql-admin-name")
admin_password = config.require_secret("sql-admin-password")
user_name = config.require("sql-user-name")
user_password = config.require_secret("sql-user-password")
availability_zone = 'us-east-1'

# Create RDS Subnet Group using the above created subnets
db_subnet_group = rds.SubnetGroup(
    'subnet-group',
    subnet_ids=[
        private_db_subnet_1.id,
        private_db_subnet_2.id,
        private_db_subnet_3.id
    ],
    description='A subnet group for 3 subnets'
)

# Create a VPC security group
db_security_group = ec2.SecurityGroup(
    'db-securitygroup',
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
            from_port=3306,
            to_port=3306,
            cidr_blocks=['0.0.0.0/0'],
        )
    ]
)

# An RDS instnace is created to hold our MySQL database
db_instance = rds.Instance(
    "mysql-server",
    engine="mysql",
    username=admin_name,
    password=admin_password,
    instance_class="db.t2.micro",
    allocated_storage=20,
    skip_final_snapshot=True,
    publicly_accessible=False,
    db_subnet_group_name=db_subnet_group.id,
    vpc_security_group_ids=[db_security_group.id]
)

# Allow inbound traffic to the RDS instance from the EC2 instance's security group
rds_sg_rule = ec2.SecurityGroupRule("rds-security-group-rule",
    type="ingress",
    from_port=3306,
    to_port=3306,
    protocol="tcp",
    security_group_id=db_security_group.id,
    source_security_group_id=app_security_group.id,
)

# Creating a Pulumi MySQL provider to allow us to interact with the RDS instance
mysql_provider = mysql.Provider(
    "mysql-provider",
    endpoint=db_instance.endpoint,
    username=admin_name,
    password=admin_password
)

# Initializing a basic database on the RDS instance
mysql_database = mysql.Database(
    "mysql-database",
    name="votes-database",
    opts=pulumi.ResourceOptions(provider=mysql_provider)
)

# Creating a user which will be used to manage MySQL tables
mysql_user = mysql.User(
    "mysql-standard-user",
    user=user_name,
    host="%",  # allow connection from any host",
    plaintext_password=user_password,
    opts=pulumi.ResourceOptions(provider=mysql_provider)
)

# The user needs the permissions to function
mysql_access_grant = mysql.Grant(
    "mysql-access-grant",
    user=mysql_user.user,
    host=mysql_user.host,
    database=mysql_database.name,
    privileges= ["SELECT", "UPDATE", "INSERT", "DELETE"],
    opts=pulumi.ResourceOptions(provider=mysql_provider)
)

# The database schema and initial data to be deployed to the database
creation_script = """
    CREATE TABLE votesTable (
        choice_id int(10) NOT NULL AUTO_INCREMENT,
        vote_count int(10) NOT NULL,
        PRIMARY KEY (choice_id)
    ) ENGINE=InnoDB;
    INSERT INTO votesTable(choice_id, vote_count) VALUES (0,0);
    INSERT INTO votesTable(choice_id, vote_count) VALUES (1,0);
    """

# The SQL commands the database performs when deleting the schema
deletion_script = "DROP TABLE votesTable CASCADE"

# Creating our dynamic resource to deploy the schema during `pulumi up`. The arguments
# are passed in as a SchemaInputs object
mysql_votes_table = Schema(
    name="mysql_votes_table",
    args=SchemaInputs(
        admin_name, admin_password, db_instance.address,
        mysql_database.name, creation_script, deletion_script
    )
)

# Export the instance endpoint
pulumi.export('db_instance_endpoint', db_instance.endpoint)
