# Run Ansible Locally
* enable `ansible_ssh_private_key_file` in `hosts.yml`
* run the playbook with extra variables
```sh
ansible-playbook playbook.yml -e "git_tag=v0.0.10"
```