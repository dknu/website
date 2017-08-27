from fabric.api import env, run, cd, abort
from fabric.operations import sudo

env.hosts = ['ec2-18-194-15-120.eu-central-1.compute.amazonaws.com']
root_folder = '/devops/containers/'


def init():
    sudo('mkdir -p %s' % root_folder)
    sudo('touch %s/.env' % root_folder)
    install_nginx()
    update_global_nginx()
    install_letsencrypt()


def install_letsencrypt():
    sudo('apt-get update')
    sudo('apt-get install software-properties-common')
    sudo('add-apt-repository ppa:certbot/certbot')
    sudo('apt-get update')
    sudo('apt-get install python-certbot-nginx ')

    sudo('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')


def create_certificate(subdomain, domains=('hackerspace-ntnu.no', 'hackerspace.idi.ntnu.no')):
    cert_domains = []
    for domain in domains:
        cert_domains.append('%s.%s' % (subdomain, domain))
        cert_domains.append('www.%s.%s' % (subdomain, domain))
    cert_str = ''.join([' -d %s' % cert_domain for cert_domain in cert_domains])
    sudo('certbot certonly --webroot-path /var/www/html %s' % cert_str)


def create_server(name='test'):
    with cd(root_folder):
        sudo('mkdir -p ' + name)
        with cd(root_folder + name):
            sudo('rm -rf docker-services')
            sudo('git clone https://github.com/hackerspace-ntnu/docker-services.git')
            with cd(root_folder + name + '/docker-services'):
                sudo('git clone https://github.com/hackerspace-ntnu/website.git')
            sudo('cp ' + root_folder + '.env docker-services')
            update_nginx(name)
            update_docker_compose(name)
            create_certificate(name)
            update_server(name)
            with cd(root_folder + name + '/docker-services'):
                sudo('docker-compose -p '+name+' up -d')


def update_nginx(name='test'):
    """ Update nginx config for the container. """
    with cd(root_folder + name):
        sudo('python3 docker-services/nginx/nginx.py %s' % name)

def update_docker_compose(name='test'):
    with cd(root_folder + name + '/docker-services'):
        sudo('python3 compose.py %s' % name)


def install_nginx():
    sudo('apt-get update')
    sudo('apt-get install nginx')

    sudo("ufw allow 'Nginx Full'")
    sudo("ufw delete allow 'Nginx HTTP'")


def update_global_nginx():
    with cd('/tmp'):
        sudo('git clone https://github.com/hackerspace-ntnu/docker-services.git')
        sudo('mv docker-services/nginx/templates/global /etc/nginx/sites-available/default')
        sudo('rm -rf docker-services')

# TODO: Check if works
def update_server(name='test'):
    path = root_folder + name + '/website'
    git_pull(path, branch)
    migrations(path)

def git_pull(path, branch='master'):
    with cd(path):
        sudo(f'git checkout {branch}', user='git')
        sudo('git pull', user='git')
        sudo(f'git reset --hard origin/{branch}', user='git')

def migrations(path):
    run('python manage.py makemigrations')
    run('python manage.py migrate')
		
def delete_server(name='test'):
    sudo('docker rm $(docker stop $(docker ps -a -q --filter ancestor=%s --format="{{.ID}}"))' % name)
    sudo('docker rm')
    with cd(root_folder):
        sudo('rm -rf ' + name)
