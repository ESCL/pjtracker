# Install python3 and pip

python3:
  pkg.installed:
    - name: python3

pip3:
  pkg.installed:
    - name: python-pip
    - require:
      - pkg: python3

pip3-update:
  cmd.run:
    - name: pip install -U pip
    - require:
      - pkg: pip3
