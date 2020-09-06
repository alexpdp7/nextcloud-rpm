FROM centos:8
RUN dnf install -y rpm-build
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf install -y https://rpms.remirepo.net/enterprise/remi-release-8.rpm
RUN dnf module install -y php:remi-7.4
RUN dnf install -y php-pear
COPY nextcloud-19.0.0.tar.bz2 /root/rpmbuild/SOURCES/
COPY nextcloud /root/rpmbuild/SOURCES/
