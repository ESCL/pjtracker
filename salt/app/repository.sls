# Update repository

include:
  - core.git
  - core.ssh

pjtracker-repository:
  git.latest:
    - name: 'git+ssh://git@bitbucket.org:escng/tracker.git'
    - rev: master
    - target: /home/ubuntu/apps/tracker
    - force_checkout: true
    - force_clone: true
    - user: ubuntu
    - require:
      - pkg: git
      - file: ssh-config
      - ssh_known_hosts: ssh-bitbucket-host
