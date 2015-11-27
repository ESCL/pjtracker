# Install, init and reload uwsgi application server

include:
  - app.environment

uwsgi-install:
  pip.installed:
    - name: uwsgi

uwsgi-logdir:
  file.directory:
    - name: /var/log/uwsgi

uwsgi-run:
  cmd.run:
    - name: uwsgi --ini /home/ubuntu/apps/tracker/tracker/uwsgi.ini --chdir=/home/ubuntu/apps/tracker
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
