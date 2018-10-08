import os
from time import sleep

projects = [
    ('databasetools', '/Users/Stephen/Dropbox/scripts/dbtools'),
    ('looptools', '/Users/Stephen/Dropbox/scripts/looptools'),
    ('psdconvert', '/Users/Stephen/Dropbox/scripts/psdconvert'),
    ('dirutility', '/Users/Stephen/Dropbox/scripts/dirutility'),
    ('PyPDF3', '/Users/Stephen/Dropbox/scripts/PyPDF3'),
    ('PyBundle', '/Users/Stephen/Dropbox/scripts/PyBundle'),
    ('synfo', '/Users/Stephen/Dropbox/scripts/synfo'),
    ('ImgConverter', '/Users/Stephen/Dropbox/scripts/ImgConverter'),
    ('pdd_tools3', '/Users/Stephen/Dropbox/scripts/psd-tools3'),
    ('differentiate', '/Users/Stephen/Dropbox/scripts/differentiate'),
    ('mysql-toolkit', '/Users/Stephen/Dropbox/scripts/mysql-toolkit'),
]

if __name__ == '__main__':
    print('PyPi distribution control::\n\n' + 'Deploy releases of...')

    try:
        for name, directory in projects:
            update_project = input(name + ' [y/n]: ')
            if update_project == 'y':
                os.chdir(directory)
                os.system('python setup.py sdist')
                sleep(1)
                os.system('twine upload -u stephenneal -p pythonstealth19 dist/*')
                print(name + str(' successfully deployed\n'))
                exit(0)
    except KeyboardInterrupt:
        exit(0)
