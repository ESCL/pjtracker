# Init/reload uwsgi application server

include:
  - app.setup

uwsgi-logdir:
  file.directory:
    - name: /var/log/uwsgi

uwsgi-run:
  cmd.run:
    - name: /home/ubuntu/.virtualenvs/pjtracker/bin/uwsgi --ini tracker/uwsgi.ini
    - cwd: /home/ubuntu/apps/tracker
    - unless: test -e /tmp/uwsgi-fifo
    - require:
      - cmd: django-migrate
      - cmd: django-collectstatic

uwsgi-reload:
  cmd.run:
    - name: echo r > /tmp/uwsgi-fifo
    - onlyif: test -e /tmp/uwsgi-fifo
    - require:
      - cmd: django-migrate
      - cmd: django-collectstatic