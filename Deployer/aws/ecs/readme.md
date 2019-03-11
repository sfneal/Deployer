<p align="left">
    <img src="https://i.imgur.com/YVmIHsN.png" alt="logo" width="200px">
</p>

# Connecting Elastic File System (EFS) with Elastic Container System (ECS) instnaces

Amazon Elastic File System (Amazon EFS) provides simple, scalable file storage for use with Amazon EC2 instances. With Amazon EFS, storage capacity is elastic, growing and shrinking automatically as you add and remove files. Your applications can have the storage they need, when they need it.

You can use Amazon EFS file systems with Amazon ECS to export file system data across your fleet of container instances. That way, your tasks have access to the same persistent storage, no matter the instance on which they land. However, you must configure your container instance AMI to mount the Amazon EFS file system before the Docker daemon starts. Also, your task definitions must reference volume mounts on the container instance to use the file system.

[Read More (AWS Docs)] (https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_efs.html)



## Step 1: Gather Cluster Information
Before you can create all of the required resources to use Amazon EFS with your Amazon ECS cluster, gather some basic information about the cluster, such as the VPC it is hosted inside of, and the security group that it uses.

 1. Open the [Amazon EC2 console](https://console.aws.amazon.com/ec2/).
 2. Select one of the container instances from your cluster and view the Description tab of the instance details. If you created your cluster with the Amazon ECS first-run or cluster creation wizards, the cluster name should be part of the EC2 instance name. For example, a cluster named default has this EC2 instance name: ECS Instance - EC2ContainerService-default.
 3. **Record the VPC ID value** for your container instance. Later, you create a **security group** and an **Amazon EFS file system** in this **VPC**.
 4. Open the security group to view its details.
 5. Record the **Group ID**. Later, you allow **inbound traffic** from this **security group** to your Amazon EFS file system.



## Step 2: Create a Security Group for an Amazon EFS File System
In this section, you create a security group for your Amazon EFS file system that allows inbound access from your container instances.

 1. Open the [Amazon EC2 console](https://console.aws.amazon.com/ec2/).
 2. In the left navigation pane, choose **Security Groups**, Create Security Group.
 3. For Security group name, enter a unique name for your security group. For example, EFS-access-for-sg-dc025fa2.
 4. For Description, enter a description for your security group.
 5. For VPC, choose the **VPC that you identified earlier (1-3)** for your cluster.
 6. Choose **Inbound**, Add rule.
 7. For Type, choose **All traffic**.
 8. For Source, choose Custom and then enter the s**ecurity group ID that you identified earlier (1-5)** for your cluster.
 9. Choose Create.

 
 
## Step 3: Create an Amazon EFS File System
Before you can use Amazon EFS with your container instances, you must create an Amazon EFS file system.

 1. Open the [Amazon Elastic File System console](https://console.aws.amazon.com/efs/)
 2. Choose **Create file system**
 3. On the **Configure file system access page**, choose the **VPC that your container instances are hosted in (1-3)** and choose Next Step. By default, each subnet in the specified VPC receives a mount target that uses the default security group for that VPC.
 4. For **Security groups**, add the security group that you created in the previous section. Choose Next step
 5. (Optional) Add tags for your file system. For example, you could specify a unique name for the file system by entering that name in the Value column next to the Name key
 6. Choose a performance mode for your file system and choose Next Step
 7. Review your file system options and choose Create File System.

 
 
## Step 4: Configure Container Instances (create if needed)
After you've created your Amazon EFS file system in the same VPC as your container instances, you must configure the container instances to access and use the file system.

 1. Log in to the container instance via SSH. For more information, see Connect to Your Container Instance.
 2. Create a mount point for your Amazon EFS file system. For example, /efs.
 3. Install NFS client software on your container instance
 4. Mount your file system with the following command. Be sure to replace the file system ID and region with your own.
 5. Validate that the file system is mounted correctly with the following command. You should see a file system entry that matches your Amazon EFS file system. If not, see Troubleshooting Amazon EFS in the Amazon Elastic File System User Guide.
 6. Make a backup of the /etc/fstab file.
 7. Update the /etc/fstab file to automatically mount the file system at boot.
 8. Reload the file system table to verify that your mounts are working properly.

```
1. $ ssh -i ~/.ssh/persistent-storage.pem ubuntu@ec2-3-91-42-242.compute-1.amazonaws.com
2. $ sudo mkdir /efs
3. $ sudo apt-get install -y nfs-common
4. $ sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 fs-5e0d65be.efs.us-east-1.amazonaws.com:/ /efs
5. $ mount | grep efs
6. $ sudo cp /etc/fstab /etc/fstab.bak
7. $ echo 'fs-5e0d65be.efs.us-east-1.amazonaws.com:/ /efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 0 0' | sudo tee -a /etc/fstab
8. $ sudo mount -a
```



## Step 5: Create a Task Definition to Use the Amazon EFS File System
Because the file system is mounted on the host container instance, you must create a volume mount in your Amazon ECS task definition that allows your containers to access the file system. For more information, see [Using Data Volumes in Tasks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html).

The following task definition creates a data volume called efs-html at /efs/html on the host container instance Amazon EFS file system. The nginx container mounts the host data volume at the NGINX root, /usr/share/nginx/html.

```
{
  "containerDefinitions": [
    {
      "memory": 128,
      "portMappings": [
        {
          "hostPort": 80,
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "mountPoints": [
        {
          "containerPath": "/usr/share/nginx/html",
          "sourceVolume": "efs-html"
        }
      ],
      "name": "nginx",
      "image": "nginx"
    }
  ],
  "volumes": [
    {
      "host": {
        "sourcePath": "/efs/html"
      },
      "name": "efs-html"
    }
  ],
  "family": "nginx-efs"
}
```

You can save this task definition to a file called nginx-efs.json and register it to use in your own clusters with the following AWS CLI command. For more information, see Installing the AWS Command Line Interface in the AWS Command Line Interface User Guide.

```$ aws ecs register-task-definition --cli-input-json file://nginx-efs.json```



## Step 6: Add Content to the Amazon EFS File System
For the NGINX example task, you created a directory at /efs/html on the container instance to host the web content. Before the NGINX containers can serve any web content, you must add the content to the file system. In this section, you log in to a container instance and add an index.html file.

1. Connect using SSH to one of your container instances that is using the Amazon EFS file system. For more information, see Connect to Your Container Instance.
2. Write a simple HTML file by copying and pasting the following block of text into a terminal.

```
sudo bash -c "cat >/efs/html/index.html" <<'EOF'
<html>
    <body>
        <h1>It Works!</h1>
        <p>You are using an Amazon EFS file system for persistent container storage.</p>
    </body>
</html>
EOF
```


## Step 7: Run a Task and View the Results
Now that your Amazon EFS file system is available on your container instances and there is web content for the NGINX containers to serve, you can run a task using the task definition that you created earlier. The NGINX web servers serve your simple HTML page. If you update the content in your Amazon EFS file system, those changes are propagated to any containers that have also mounted that file system.

 1. Open the [Amazon ECS console](https://console.aws.amazon.com/ecs/)
 2. Choose the cluster that you have configured to use Amazon EFS
 3. Choose **Tasks**, **Run new task**
 4. For **Task Definition**, choose the nginx-efs taskjob definition that you created earlier and choose **Run Task**. For more information on the other options in the run task workflow, see Running Tasks
 5. Below the **Tasks** tab, choose the task that you just ran.
 6. Expand the container name at the bottom of the page, and choose the IP address that is associated with the container. Your browser should open a new tab with the following message: