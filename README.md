> Author: Pau Sabatés

### Explanation:
- lambda_function_ecs.py updates an existing task with the desired docker image in a given service and cluster.

- First the task definition is updated using the same 'family' with the new docker image:tag uploaded in a docker registry.
- Secondly the ECS service is updated forcing a new deployment using the rollback methodology.

### Requirements:
- In order to achive this solution, the following flow was considered:
1. Upload the desired docker imatge:tag to ECR.
2. Create the lambda function with the following aws cli command, using the cluster, service, and container names desired to update:
``` aws lambda create-function --function-name EcsImageUpdate --handler lambda_function_ecs.lambda_handler --memory-size 1024 --timeout 10 --runtime python3.6 --zip-file fileb://walla.zip --role arn:aws:iam::490024992885:role/lambda_full_access --environment Variables={CLUSTER_NAME=Cluster , SERVICE_NAME=Service , TASK_DEF=Task , CONTAINER_NAME=Container , IMAGE=5555555555.dkr.ecr.eu-west-1.amazonaws.com/image:2.0}" ```
3. Run the lambda funtion in the aws panel.


### Notes when creating ECS cluster:
- In ECR repository diable Tag immutability option in order to allow tag overwrite.
- In ECS Service definition, create the service with the 'Rolling Update' deployment type in order to replace the task.

### Improvements of the solution in a DevOps environment:

- Currently the parameters required to indicate which cluster to update are entered manually, so it can be improved in different ways:
    - When a new image is uploaded to ECR, a CloudWatch event for instance is executed to put the image to a lambda target.
    - Call an API Gateway with the ECS desired names in a mapping template that will recieve the lambda function using its 'event' parameter object.
    - Call any of the above combination using CodePipeline for example with a commit trigger or passing ECS desired names as arguments to the pipeline that will invoke the lambda.

- Monitor and log lambda with CloudTrail for instance.