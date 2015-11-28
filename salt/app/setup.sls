# Run required django commands before deployment

include:
  - app.environment

django-migrate:
  cmd.run:
    - name: /home/ubuntu/.virtualenvs/pjtracker/bin/python manage.py migrate --noinput --settings=tracker.settings.prod
    - cwd: /home/ubuntu/apps/tracker
    - require:
      - pip: pjtracker-requirements

django-collectstatic:
  cmd.run:
    - name: /home/ubuntu/.virtualenvs/pjtracker/bin/python manage.py collectstatic --noinput --settings=tracker.settings.prod
    - cwd: /home/ubuntu/apps/tracker
    - require:
      - pip: pjtracker-requirements
