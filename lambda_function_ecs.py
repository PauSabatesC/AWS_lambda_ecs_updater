import boto3
import os

CLUSTER_NAME = os.environ['CLUSTER_NAME']
SERVICE_NAME = os.environ['SERVICE_NAME']
TASK_FAMILY_DEF = os.environ['TASK_DEF']
CONTAINER_NAME = os.environ['CONTAINER_NAME']
DOCKER_IMAGE = os.environ['IMAGE']

ecs_instance = boto3.client('ecs', region_name="eu-west-1")

# First the task definition is updated using the same 'family' with
#   the new docker image:tag uploaded in a docker registry.
# Secondly the ECS service is updated forcing a new deployment using the rollback methodology.
# Note: It's not necessary to indicate the revision of the task because it uses the latest Active by default
def lambda_handler(event, context):

    task_response = ecs_instance.register_task_definition(
        family=TASK_FAMILY_DEF,
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': CONTAINER_NAME,
                'image': DOCKER_IMAGE,
                'memory': 500,
                'portMappings': [
                    {
                        'containerPort': 80,
                        'hostPort': 80,
                        'protocol': 'tcp'
                    },
                ],
                'essential': True,
            },
        ],
    )

    service_response = ecs_instance.update_service(
        cluster=CLUSTER_NAME,
        service=SERVICE_NAME,
        desiredCount=2,
        forceNewDeployment=True,
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 100
        },
    )
