---
# configuration for production

env: production
hostname: openecoe-webui
app_fqdn: www.openecoe.com
#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
ansible_connection: local

git_branch: master

# Enviroment Config
app_secret_key: 'f24b05095b4748a8b9d13df5cdb8d83c'
app_debug: False
api_uri: "https://api.openecoe.com"
api_route: "{{api_uri}}/api"
api_auth_token: "{{api_uri}}/auth/tokens"

app_workers: 4

supervisor_user: root
supervisor_password: 'kkGFGhiK06BXdEW9gKi4j5VD'

#Deactivate supervisor http server in production
supervisor_inet_http_server_enable: false