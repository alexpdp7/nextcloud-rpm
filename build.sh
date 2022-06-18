#!/bin/sh

set -ue

mkdir -p SRPMS RPMS

podman build . -t build
podman run -it \
	-w /root/rpmbuild/SOURCES/ \
	-v $(pwd)/SRPMS:/root/rpmbuild/SRPMS/ \
	-v $(pwd)/RPMS:/root/rpmbuild/RPMS/ \
	--security-opt label=disable \
	build:latest rpmbuild $1 nextcloud.spec
