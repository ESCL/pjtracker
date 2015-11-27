# Setup virtualenv use (install env, wrapper and create container dir)

include:
  - core.python

virtualenv:
  pip.installed:
    - name: virtualenv
    - require:
      - pkg: pip3

virtualenvwrapper:
  pip.installed:
    - name: virtualenvwrapper
    - require:
      - pip: virtualenv

virtualenvs-directory:
  file.directory:
    - name: /home/ubuntu/.virtualenvs
    - user: ubuntu
    - group: ubuntu
    - dir_mode: 755
    - require:
      - pip: virtualenvwrapper
