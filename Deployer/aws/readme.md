https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html#single-container-docker.setup

VARIABLES:
 - DockerHub username
 - source directory (path)
 - application-name (repo)
 - environment-name (branch)
 - version_label (release)
 
INITIALIZE AWS APPLICATION:
 - $ eb init -p docker application-name


TEST CONTAINER LOCALLY:
 - $ eb local run --port 5000
 - $ eb local open


DEPLOY DOCKER IMAGE TO DOCKERHUB:
 - $ docker build -t docker-username/beanstalk-flask:latest .
 - $ docker push docker-username/beanstalk-flask:latest


CREATE REMOTE-DOCKER DEPLOYMENT DIRECTORY:
 - Example ~/remote-docker/Dockerrun.aws.json
 ``` 
{
 "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "stephenneal/dockerrepo",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000"
    }
  ]
}
```
NEW environment
 - ~/remote-docker$ eb create --label version_label environment-name
 
UPDATE environment
 - ~/remote-docker$ eb deploy --label version_label environment-name (if the environment already exists)
 
 - ~/remote-docker$ eb open