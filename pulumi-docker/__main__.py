"""A Python Pulumi program"""

import pulumi
import pulumi_docker as docker


mongo_user = "docker"
mongo_password = "docker"
mongo_port = 27017
mongo_host = "mongo"
app_port = 80
doc_root = "/var/www/html"
pma_port = 8080
mysql_password = "docker"
mysql_user = "docker"
mysql_port = 3306
mysql_host = "database"
 
network = docker.Network("network",
                        name="services")

mongo_image = docker.RemoteImage("mongo_image",
                        name="mongo:3.4",
                        keep_locally=True)

mongo_container = docker.Container("mongo_container",
                        image=mongo_image.latest,
                        ports=[docker.ContainerPortArgs(internal=mongo_port, external=mongo_port)],
                        envs=[
                            f"MONGO_INITDB_ROOT_USERNAME={mongo_user}",
                            f"MONGO_INITDB_ROOT_PASSWORD={mongo_password}",
                        ],

                        networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                            name=network.name,
                            aliases=[mongo_host]
                        )]
)

web_image = docker.Image("web_image",
                        build=docker.DockerBuild(context="./php74"),
                        image_name="phpwebserver",
                        skip_push=True
)


mysql_image = docker.Image("mysql_image",
                        build=docker.DockerBuild(context="./mysql8"),
                        image_name="mysql",
                        skip_push=True
)

mysql_container = docker.Container("mysql_container",
                        image=mysql_image.base_image_name,
                        ports=[docker.ContainerPortArgs(internal=mysql_port, external=mysql_port)],
                        envs=[
                            f"MYSQL_ROOT_PASSWORD={mysql_password}",
                        ],
                        networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                            name=network.name,
                            aliases=[mysql_host]
                        )],
)


app_container = docker.Container("app_container",
                        image=web_image.base_image_name,
                        ports=[docker.ContainerPortArgs(internal=app_port, external=app_port)],
                        envs=[
                            f"APACHE_DOCUMENT_ROOT={doc_root}",
                            f"PMA_PORT={pma_port}",
                            f"MYSQL_ROOT_PASSWORD={mysql_password}"
                        ],
                        networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                            name=network.name
                        )],
                        opts=pulumi.ResourceOptions(depends_on=[mongo_container,mysql_container])
)

pulumi.export("url", f"http://localhost:{app_port}")
