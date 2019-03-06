https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html#single-container-docker.setup

VARIABLES:
 - DockerHub username
 - source directory
 - application-name
 - environment-name
 - image-name
 - version_label
 
INITIALIZE AWS APPLICATION:
 - $ eb init -p docker application-name

TEST CONTAINER LOCALLY:
 - $ eb local run --port 5000
 - $ eb local open

## OPTION 1:
DEPLOY ENVIRONMENT TO AWS:
 - $ eb create environment-name --label version_label 
 - $ eb deploy environment-name --label version_label (if the environment already exists)
 - $ eb open

## OPTION 2:
DEPLOY DOCKER IMAGE TO DOCKERHUB:
 - $ docker build -t docker-username/beanstalk-flask:latest .
 - $ docker push docker-username/beanstalk-flask:latest

CREATE REMOTE-DOCKER DEPLOYMENT DIRECTORY:
 - Example ~/remote-docker/Dockerrun.aws.json
 ``` 
{
 "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "username/beanstalk-flask",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000"
    }
  ]
}
```
 - ~/remote-docker$ eb init -p docker application-name
 - ~/remote-docker$ eb create --label version_label environment-name
 - ~/remote-docker$ eb deploy --label version_label environment-name (if the environment already exists)
 - ~/remote-docker$ eb open