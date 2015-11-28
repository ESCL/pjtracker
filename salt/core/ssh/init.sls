ssh-directory:
  file.directory:
    - name: /home/ubuntu/.ssh
    - user: ubuntu
    - mode: 775

ssh-identity-file:
  file.managed:
    - name: /home/ubuntu/.ssh/id_rsa
    - user: ubuntu
    - mode: 600
    - source: salt://core/ssh/id_rsa
    - require:
      - file: ssh-directory

ssh-public-key:
  file.managed:
    - name: /home/ubuntu/.ssh/id_rsa.pub
    - user: ubuntu
    - mode: 600
    - source: salt://core/ssh/id_rsa.pub
    - require:
      - file: ssh-directory

ssh-bitbucket-host:
  ssh_known_hosts:
    - present
    - name: 'bitbucket.org'
    - user: ubuntu
    - fingerprint: 97:8c:1b:f2:6f:14:6b:5c:3b:ec:aa:46:46:74:7c:40
    - require:
      - file: ssh-directory

ssh-config:
  file.managed:
    - name: /home/ubuntu/.ssh/config
    - user: ubuntu
    - mode: 644
    - template: jinja
    - source: salt://core/ssh/config
    - require:
      - file: ssh-directory
      - file: ssh-identity-file
      - file: ssh-public-key
