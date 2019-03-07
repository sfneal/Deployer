<p align="left">
    <img src="https://github.com/Radu-Raicea/Dockerized-Flask/blob/master/dockerized_logo.png?raw=true" alt="logo" width="800px">
</p>

# AWS Elastic Beanstalk
# Deploying Dockerized Flask applications
AWS Elastic Beanstalk can launch single container Docker environments by building an image described in a Dockerfile or pulling a remote Docker image. If you're deploying a remote Docker image, you don't need to include a Dockerfile. Instead, use a Dockerrun.aws.json file, which specifies an image to use and additional configuration options.

## Prerequisites
#### References
 - [AWS Docs: Elastic Beanstalk Single Container Docker](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html#single-container-docker.setup)
 - [Getting Started with Docker & Flask] (https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/)
 - [Dockerize Your Flask App] (https://runnable.com/docker/python/dockerize-your-flask-application)
 - [Dockerize Flask APP with NGINX server] (https://medium.com/bitcraft/dockerizing-a-python-3-flask-app-line-by-line-400aef1ded3a)

#### Variables
 - ```<docker-user>``` DockerHub username
 - ```<source>``` Codebase source path
 - ```<application-name>``` AWS application name/GitHub repo name
 - ```<environment-name>``` AWS environment name/GitHub branch/DockerHub image name
 - ```<version-label>``` AWS version label/GitHub release

 
#### Additional Commands
Docker build and run commands for local testing.

 - Build and run local Docker container
	 - ```docker build -t <docker-user>/<environment-name>:tag <source>```
	 - ```docker run -i -t -p 5000:5000 <docker-user>/<environment-name>:tag```
 - Other commands
	 - ```docker image ls``` — list available images
	 - ```docker container ls``` — list all containers
	 - ``docker logs <partial container ID>``` — tail logs from a container
	 - ```docker kill <partial container ID>``` — kill execution of a container
	 - ```docker restart <partial container ID>``` — restart container
	 - ```docker start <partial container ID>``` — start stopped container
	 - ```docker stop <partial container ID>``` — gracefully end container
	 - ```docker container prune``` — delete all non-running containers


 
#### Example Directory Structure
Example files and directory structures that will be created in the process of deploying to AWS Elastic Beanstalk.  The 'source' folder represents your code base's root path and 'source-remote' is your code base's root path with a '-remote' extension.  'Code' represents the directory on your local machine where you store codiing projects.

```
Code
├── source
|	├── .elasticbeanstalk
|	│   └── config.yml
|	├── app.py
|	├── Dockerfile
|	└── requirements.txt
└── source-remote
	├── .elasticbeanstalk
	│   └── config.yml
	└── Dockerrun.aws.json
```    
 
 
## Deployment
### 1A. Initialize ```<source>``` as AWS application
Use the Elastic Beanstalk CLI (EB CLI) to configure your local repository for deployment to Elastic Beanstalk. Set your application's Dockerfile at the root of the directory.

```$ eb init -p docker <application-name>```


### 1B (optional). Test container locally
Use ```eb local run``` to build and run your container locally and ```eb local open``` to open the container in a web browser.

 - ```$ eb local run --port 5000```
 - ```$ eb local open```


### 2. Deploy Docker image to DockerHub:
The following steps create a publicly available Docker image.

Once we've built and pushed our image, we can deploy it to Elastic Beanstalk with a Dockerrun.aws.json file. To build a Docker image of the Flask application and push it to Docker Hub, run the following commands.

 - ```$ docker build -t <docker-user>/<environment-name>:latest <source>```
 - ```$ docker push <docker-user>/<environment-name>:latest```

Now you can deploy your application using only a Dockerrun.aws.json file.


### 3. Make new directory for remote deployment file
Make a new directory and create a Dockerrun.aws.json file.  It is suggested that you create a new directory next to your source code root that ends with '-remote'.

Example Dockerrun.aws.json file.

```
{
 "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "<docker-user>/<environment-name>",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000"
    }
  ]
}
```

### 4. Deploy to Elastic Beanstalk
Configure your local repository for deployment to Elastic Beanstalk.

Then, determine weather you are creating a new Elastic Beanstalk environment within your Elastic Beanstalk application.

#### 4A. Configure local repository for deployment
 - ```$ cd <source>-remote```
 - ```$ eb init -p docker <application-name>```

#### 4B. Create new environment or update existing
 - NEW environment: ```$ eb create <environment-name>```
 - UPDATE environment: ```$ eb deploy --label <version_label> <environment-name>```

 
#### 4C. Open deployed environment in a web browser
 - ```$ eb open```