from Deployer.aws.s3.s3 import S3
from Deployer.aws.s3.gui import sync


def main():
    params = sync()
    S3(params['bucket']).sync(params['source'], params['destination'], params['delete'], params['acl'])


if __name__ == '__main__':
    main()
