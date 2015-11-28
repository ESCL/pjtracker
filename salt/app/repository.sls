# Update repository

include:
  - core.git
  - core.ssh

pjtracker-repo-checkout:
  cmd.run:
    - name: git checkout -- .
    - cwd: /home/ubuntu/apps/tracker
    - user: ubuntu
    - require:
      - pkg: git

# Upgrade protocol to ssh and use deployment key (no passwd)
pjtracker-repo-protocol:
  cmd.run:
    - name: git remote set-url origin 'git+ssh://git@bitbucket.org/escng/tracker.git'
    - cwd: /home/ubuntu/apps/tracker
    - user: ubuntu
    - require:
      - pkg: git

# Temp hack for broken git.latest (see below)
pjtracker-repo-pull:
  cmd.run:
    - name: git pull
    - cwd: /home/ubuntu/apps/tracker
    - user: ubuntu
    - require:
      - pkg: git
      - file: ssh-config
      - ssh_known_hosts: ssh-bitbucket-host
      - cmd: pjtracker-repo-checkout
      - cmd: pjtracker-repo-protocol

# Broken in current version (https://github.com/saltstack/salt/issues/28287)
#pjtracker-repo-pull:
#  git.latest:
#    - name: 'git+ssh://git@bitbucket.org/escng/tracker.git'
#    - rev: master
#    - target: /home/ubuntu/apps/tracker
#    - force_checkout: true
#    - user: ubuntu
#    - require:
#      - file: ssh-config
#      - ssh_known_hosts: ssh-bitbucket-host
#      - cmd: pjtracker-repo-protocol
