#!/bin/sh

set -ue

docker build . -t build
docker run -it \
	-w /root/rpmbuild/SOURCES/ \
	-v $(pwd)/SRPMS:/root/rpmbuild/SRPMS/ \
	-v $(pwd)/RPMS:/root/rpmbuild/RPMS/ \
	build:latest rpmbuild $1 nextcloud.spec
