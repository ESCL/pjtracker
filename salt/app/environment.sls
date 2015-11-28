# Create and setup application virtualenv

include:
  - core.virtualenv
  - app.dependencies
  - app.repository

pjtracker-virtualenv:
  virtualenv.managed:
    - name: /home/ubuntu/.virtualenvs/pjtracker
    - python: /usr/bin/python3
    - system_site_packages: False
    - user: ubuntu
    - require:
      - file: virtualenvs-directory

pjtracker-requirements:
  pip.installed:
    - bin_env: /home/ubuntu/.virtualenvs/pjtracker
    - cwd: /home/ubuntu
    - no_chown: true
    - requirements: /home/ubuntu/apps/tracker/requirements/prod-cpython.txt
    - require:
      - cmd: pip-update
      - cmd: pjtracker-repo-pull
      - pkg: pgsql-install
      - virtualenv: pjtracker-virtualenv
