import os
from time import sleep

username = 'stephenneal'
password = 'pythonstealth19'
base_dir = '/Users/Stephen/Dropbox/scripts'

projects = [
    'databasetools',
    'looptools',
    'psdconvert',
    'dirutility',
    'PyPDF3',
    'PyBundle',
    'synfo',
    'ImgConverter',
    'psd-tools3',
    'differentiate',
    'mysql-toolkit',
]

if __name__ == '__main__':
    print('PyPi distribution control::\n\n' + 'Deploy releases of...')

    try:
        for project in projects:
            update_project = input(project + ' [y/n]: ')
            if update_project == 'y':
                os.chdir(os.path.join(base_dir, project))
                os.system('python setup.py sdist')
                sleep(1)
                command = 'twine upload -u {0} -p {1} dist/*'.format(username, password)
                os.system(command)
                print(project + str(' successfully deployed\n'))
                exit(0)
    except KeyboardInterrupt:
        exit(0)
