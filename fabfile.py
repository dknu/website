from fabric.api import env, run, cd, abort, settings
from fabric.operations import sudo

env.hosts = ['progge.party']
domains = ['progge.party'] #('hackerspace-ntnu.no', 'hackerspace.idi.ntnu.no')
root_folder = '/devops/containers/'


######################
###      INIT      ###
######################

def init():
    sudo('mkdir -p %s' % root_folder)
    sudo('touch %s/.env' % root_folder)
    install_nginx()
    update_nginx_min()
    install_letsencrypt()
    create_certificate('', domains)
    update_nginx()


######################
###   LETSENCRYPT  ###
######################

def install_letsencrypt():
    sudo('apt-get update')
    sudo('apt-get install software-properties-common')
    sudo('add-apt-repository ppa:certbot/certbot')
    sudo('apt-get update')
    sudo('apt-get install python-certbot-nginx ')

    sudo('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')


def create_certificate(subdomain, domains=domains):
    dot = '.' if subdomain else ''
    cert_domains = []
    for domain in domains:
        cert_domains.append('%s%s%s' % (subdomain, dot, domain))
        cert_domains.append('www.%s%s%s' % (subdomain, dot, domain))
    cert_str = ''.join([' -d %s' % cert_domain for cert_domain in cert_domains])
    sudo('certbot certonly --webroot-path /var/www/html %s' % cert_str)


######################
###      NGINX     ###
######################

def install_nginx():
    sudo('apt-get update')
    sudo('apt-get install nginx')

    sudo("ufw allow 'Nginx Full'")
    sudo("ufw delete allow 'Nginx HTTP'")


def update_nginx_min():
    with cd('/tmp'):
        sudo('git clone https://github.com/hackerspace-ntnu/docker-services.git')
        sudo('mv docker-services/nginx/templates/global_min /etc/nginx/sites-available/default')
        sudo('rm -rf docker-services')


def update_nginx(name='test', port=8000):
    """ Update nginx config for the container. """
    with cd(root_folder + name):
        sudo('python3 docker-services/nginx/nginx.py %s %r' % (name, port))


######################
###   CONTAINERS   ###
######################

def start_server(name='test'):
    with cd(root_folder + name + '/docker-services'):
        sudo('docker-compose -p '+name+' up -d')


def stop_server(name='test'):
    with settings(warn_only=True):
        sudo('docker stop %s' % (name+"_database"))
        sudo('docker stop %s' % (name+"_website"))
        sudo('docker stop %s' % (name+"_proxy"))


def create_server(name='test', port=8000):
    with cd(root_folder):
        sudo('mkdir -p ' + name)
        with cd(root_folder + name):
            sudo('rm -rf docker-services')
            sudo('git clone https://github.com/hackerspace-ntnu/docker-services.git')
            with cd(root_folder + name + '/docker-services'):
                sudo('git clone https://github.com/hackerspace-ntnu/website.git')
            sudo('cp ' + root_folder + '.env docker-services')
            update_nginx(name, port)
            update_docker_compose(name, port)
            create_certificate(name)
            update_server(name)
            start_server(name)


def delete_server(name='test'):
    stop_server(name)
    with settings(warn_only=True):
        sudo('docker rm %s' % (name+"_database"))
        sudo('docker rm %s' % (name+"_proxy"))
        sudo('docker rm %s' % (name+"_website"))
    with cd(root_folder):
        sudo('rm -rf ' + name)


# TODO: Check if works
def update_server(name='test', branch='master'):
    path = root_folder + name + '/docker-services/website'
    git_pull(path, branch)
    migrations(path, name)


######################
###  CONTAINERS +  ###
######################

def update_docker_compose(name='test', port=8000):
    with cd(root_folder + name + '/docker-services'):
        sudo('python3 compose.py %s %r' % (name, port))


def git_pull(path, branch='master'):
    with cd(path):
        sudo('git checkout %s' % branch, user='git')
        sudo('git pull', user='git')
        sudo('git reset --hard origin/%s' % branch, user='git')


def migrations(path, name='test'):
    with cd(path):
        run('docker exec -it %s_website bash' % name)
        run('python manage.py makemigrations')
        run('python manage.py migrate')
        run('exit')
