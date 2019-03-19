import os
from Deployer.utils import TaskTracker
from Deployer.aws.s3.gui import sync, ACL


class S3(TaskTracker):
    def __init__(self, bucket):
        self.bucket = bucket

    def sync(self, source, destination=None, delete=False, acl='private'):
        """
        Synchronize local files with an S3 bucket.

        S3 sync only copies missing or outdated files or objects between
        the source and target.  However, you can also supply the --delete
        option to remove files or objects from the target that are not
        present in the source.

        :param source: Local source directory
        :param destination: Destination directory (relative to bucket root)
        :param delete: Sync with deletion, disabled by default
        :param acl: Access permissions, must be either 'private', 'public-read' or 'public-read-write'
        :return:
        """
        assert acl in ACL, "acl parameter must be one of the following: 'private', 'public-read', 'public-read-write'"
        cmd = 'aws s3 sync "{src}" s3://{bucket}/{dst} --acl {acl}'.format(src=source, dst=destination,
                                                                         bucket=self.bucket, acl=acl)
        if delete:
            cmd += ' --delete'
        print(cmd)
        os.system(cmd)


def main():
    params = sync()
    S3(params['bucket']).sync(params['source'], params['destination'], params['delete'], params['acl'])


if __name__ == '__main__':
    main()
