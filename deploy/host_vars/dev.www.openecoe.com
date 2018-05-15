---
# configuration for vagrant

env: develop
hostname: openecoe-webui-dev
app_fqdn: www.openecoe.com
app_port: 5080

#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
ansible_connection: local

# Enviroment Config
app_debug: True
api_uri: "https://dev.api.openecoe.com:5000"
api_route: "{{api_uri}}/api"
api_auth_token: "{{api_uri}}/auth/tokens"