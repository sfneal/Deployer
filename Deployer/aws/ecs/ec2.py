import os
from subprocess import Popen, PIPE
from Deployer.utils import TaskTracker


SSH_DIRECTORY = '~/.ssh'


class EC2(TaskTracker):
    def __init__(self, ec2_dns, ssh_key, efs_id=None, mount_point=None, region='us-east-1', ec2_username='ec2-user'):
        """
        Perform operations on an EC2 container instance running an Amazon AMI.

        :param ec2_dns: Public DNS address of the EC2 instance
        :param ssh_key: PEM file used to connect to your EC2 instance/Cluster
            Assumes file is in ~/.ssh directory unless otherwise specified.
        :param efs_id: ID of the Elastic File System you would like to mount to your EC2 instance
        :param mount_point: Directory to mount the EFS to on the EC2 instance
        :param region: Default region
        :param ec2_username: Username for connecting the EC2 instance
        """
        self.ec2_dns = ec2_dns
        self.ssh_key = ssh_key if os.path.exists(ssh_key) else os.path.join(SSH_DIRECTORY, ssh_key)
        self.efs_id = efs_id
        self.region = region
        self.mount_point = mount_point
        self.ec2_username = ec2_username

    def connect(self):
        """Login to the container instance via SSH."""
        cmd = 'ssh -i {ssh_key} {user}@{dns}'.format(ssh_key=self.ssh_key, user=self.ec2_username, dns=self.ec2_dns)
        r = Popen(cmd, shell=True, stdout=PIPE)
        for i in r.stdout:
            return str(i.decode("utf-8")).strip()


def main():
    ec2 = EC2('ec2-3-91-42-242.compute-1.amazonaws.com', 'pdfconduit.pem', 'fs-a3d1a243', '/efs')
    ec2.connect()


if __name__ == '__main__':
    main()
