# Update repository

include:
  - core.git
  - core.ssh

pjtracker-repository-protocol:
  cmd.run:
    - name: git remote set-url origin 'git+ssh://git@bitbucket.org/escng/tracker.git'
    - cwd: /home/ubuntu/apps/tracker
    - user: ubuntu
    - require:
      - pkg: git

# Temp hack for broken git.latest
pjtracker-repository:
  cmd.run:
    - name: git pull
    - cwd: /home/ubuntu/apps/tracker
    - user: ubuntu
    - require:
      - pkg: git
      - file: ssh-config
      - ssh_known_hosts: ssh-bitbucket-host
      - cmd: pjtracker-repository-protocol

# Broken in current version
#pjtracker-repository:
#  git.latest:
#    - name: 'git+ssh://git@bitbucket.org/escng/tracker.git'
#    - rev: master
#    - target: /home/ubuntu/apps/tracker
#    - force_checkout: true
#    - user: ubuntu
#    - require:
#      - file: ssh-config
#      - ssh_known_hosts: ssh-bitbucket-host
#      - cmd: pjtracker-repository-protocol
