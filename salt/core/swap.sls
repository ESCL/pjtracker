# Create a swap file

create-swapfile:
  cmd.run:
    - name: fallocate -l 1G /var/swapfile
    - unless: test -e /var/swapfile

mk-swap:
  cmd.wait:
    - name: mkswap /var/swapfile
    - watch:
      - cmd: create-swapfile

mount-swap:
  mount.swap:
    - name: /var/swapfile
    - watch:
      - cmd: mk-swap