from fabric.api import env, run, cd, abort
from fabric.context_managers import prefix
from fabric.operations import sudo

env.hosts = ['hackerspace-ntnu.no']
root_folder = '/devops/'
project_folder = '/website'
projects = ['prod', 'dev']


def handle_project(func):
    def _handle_project(*args, **kwargs):
        if not args:
            func(projects[0], *args[1:], **kwargs)
        elif args[0] == 'all':
            for project in projects:
                func(project, *args[1:], **kwargs)
        elif args[0] in projects:
            func(args[0], *args[1:], **kwargs)
        else:
            abort('Invalid project')

    return _handle_project


@handle_project
def deploy(project, branch='master'):
    git(project, branch)
    requirements(project)
    django(project)
    gunicorn(project)
    nginx()


@handle_project
def git(project, branch='master'):
    with cd(root_folder + project + project_folder):
        sudo('git stash', user='git')
        sudo('git fetch --all', user='git')
        sudo('git checkout %s' % branch, user='git')
        sudo('git reset --hard origin/%s' % branch, user='git')


@handle_project
def requirements(project):
    with cd(root_folder + project + project_folder), prefix('. ../%senv/bin/activate' % project):
        run('pip install -r requirements.txt')
        run('pip install -r prod_requirements.txt')


@handle_project
def django(project):
    with cd(root_folder + project + project_folder), prefix('. ../%senv/bin/activate' % project):
        run('python manage.py makemigrations')
        run('python manage.py migrate')
        run('python manage.py collectstatic --no-input')


@handle_project
def gunicorn(project):
    sudo('systemctl restart %s' % project)


def nginx():
    sudo('systemctl restart nginx')


@handle_project
def restart(project):
    gunicorn(project)
    nginx()
