# Run required django commands before deployment

include:
  - app.environment

django-migrate:
  cmd.run:
    - name: /home/ubuntu/.virtualenvs/pjtracker/bin/python manage.py migrate --no-input --settings=tracker.settings.prod
    - cwd: /home/ubuntu/apps/tracker
    - require:
      - pip: pjtracker-requirements

django-collectstatic:
  cmd.run:
    - name: /home/ubuntu/.virtualenvs/pjtracker/bin/python manage.py collectstatic --no-input --settings=tracker.settings.prod
    - cwd: /home/ubuntu/apps/tracker
    - require:
      - pip: pjtracker-requirements