# Install, init and reload uwsgi application server

include:
  - app.environment

workon-pjtracker:
  cmd.run:
    - name: workon pjtracker
    - require:
      - virtualenv: pjtracker-virtualenv

uwsgi-install:
  pip.installed:
    - name: uwsgi
    - require:
      - cmd: workon-pjtracker

uwsgi-logdir:
  file.directory:
    - name: /var/log/uwsgi

uwsgi-run:
  cmd.run:
    - name: uwsgi --ini /home/ubuntu/apps/tracker/tracker/uwsgi.ini --chdir=/home/ubuntu/apps/tracker
    - bin_env: /home/ubuntu/.virtualenvs/pjtracker
    - unless: test -e /tmp/uwsgi-fifo
    - require:
      - pip: uwsgi-install
      - pip: pjtracker-requirements
      - file: uwsgi-logdir

uwsgi-reload:
  cmd.run:
    - name: echo r > /tmp/uwsgi-fifo
    - onlyif: test -e /tmp/uwsgi-fifo
    - require:
      - pip: uwsgi-install
      - pip: pjtracker-requirements
