# Create and setup application virtualenv

include:
  - core.virtualenv
  - app.dependencies

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
      - virtualenv: pjtracker-virtualenv
      - pkg: pgsql-install
      - cmd: pip-update
