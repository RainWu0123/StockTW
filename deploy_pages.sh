#!/bin/bash
set -euo pipefail
cd /home/ubuntu/investment
cp spa.html index.html

GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/netlify_deploy -o IdentitiesOnly=yes' git add -A
GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/netlify_deploy -o IdentitiesOnly=yes' git commit -m "publish: force index.html = spa.html for Pages"
GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/netlify_deploy -o IdentitiesOnly=yes' git push
