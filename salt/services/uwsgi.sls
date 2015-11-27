# Install, init and reload uwsgi application server

include:
  - app.environment

uwsgi-install:
  pip.installed:
    - bin_env: /home/ubuntu/.virtualenvs/pjtracker
    - no_chown: true
    - name: uwsgi
    - require:
      - virtualenv: pjtracker-virtualenv

uwsgi-logdir:
  file.directory:
    - name: /var/log/uwsgi

uwsgi-run:
  cmd.run:
    - name: uwsgi --ini /home/ubuntu/apps/tracker/tracker/uwsgi.ini --chdir=/home/ubuntu/apps/tracker
    - bin_env: /home/ubuntu/.virtualenvs/pjtracker
    - unless: test -e /tmp/wsgi-fifo
    - require:
      - pip: uwsgi-install
      - pip: pjtracker-requirements
      - file: uwsgi-logdir

uwsgi-reload:
  cmd.run:
    - name: echo r > /tmp/wsgi-fifo
    - onlyif: test -e /tmp/wsgi-fifo
    - require:
      - pip: uwsgi-install
      - pip: pjtracker-requirements
