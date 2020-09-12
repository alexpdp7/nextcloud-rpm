#!/bin/bash

set -ue

copr_login=$1
copr_username=$2
copr_token=$3
copr_project=$4

copr_config=$(mktemp)

cat >$copr_config <<EOF
[copr-cli]
login = $copr_login
username = $copr_username
token = $copr_token
copr_url = https://copr.fedorainfracloud.org
EOF

docker run -it \
	-v $(pwd)/SRPMS:/root/rpmbuild/SRPMS/ \
	-v $copr_config:/root/.config/copr \
	build:latest copr-cli build $copr_project /root/rpmbuild/SRPMS/$(ls SRPMS)

rm $copr_config