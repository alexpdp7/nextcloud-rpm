Name:           nextcloud
Version:        10.0.4
Release:        7%{?dist}
Summary:        Private file sync and share server

License:        AGPLv3+ and MIT and BSD and ASL 2.0 and WTFPL and CC-BY-SA and GPLv3+ and Adobe
URL:            http://nextcloud.com

Source0:        https://download.nextcloud.com/server/releases/%{name}-%{version}.tar.bz2

Source1:        %{name}-httpd.conf
Source2:        %{name}-access-httpd.conf.avail

Source200:        %{name}-default-nginx.conf
Source201:        %{name}-conf-nginx.conf
Source202:        %{name}-php-fpm.conf
Source203:        %{name}-el7-php-fpm.conf

# Config snippets
Source100:      %{name}-auth-any.inc
Source101:      %{name}-auth-local.inc
Source102:      %{name}-auth-none.inc
Source103:      %{name}-defaults.inc
# packaging notes and doc
Source3:        %{name}-README.fedora
Source4:        %{name}-mysql.txt
Source5:        %{name}-postgresql.txt
Source6:        %{name}-MIGRATION.fedora
# config.php containing just settings we want to specify, nextcloud's
# initial setup will fill out other settings appropriately
Source7:        %{name}-config.php

# Our autoloader for core
Source8:        %{name}-fedora-autoloader.php

# Systemd timer for background jobs
Source10:       %{name}-systemd-timer.service
Source11:       %{name}-systemd-timer.timer

# Stop OC from trying to do stuff to .htaccess files. Just calm down, OC.
# Distributors are on the case.
Patch1:         %{name}-9.1.0-dont_update_htacess.patch

# Remove explicit load of dropbox
Patch2:         %{name}-9.1.0-dropbox-autoloader.patch

# Remove explicit load of google
Patch3:         %{name}-9.1.0-google-autoloader.patch

# Remove explicit load of aws
Patch4:         %{name}-9.1.0-amazon-autoloader.patch

# Disable the integrity checking whilst a better way to deal with it is found
Patch5:         %{name}-9.1.0-default_integrity_check_disabled.patch

# Apply the backport patches to support PHP7.1 and don't complain
Patch6:         %{name}-463e2ea-php71-backport.patch
Patch7:         %{name}-b129d5d-php71-backport.patch
Patch8:         %{name}-10.0.3-dont-check-php-version.patch

# Direct the admin to the correct cli command for upgrades
Patch9:         %{name}-10.0.4-correct-cli-upgrade.patch

BuildArch:      noarch

# For the systemd macros
%{?systemd_requires}
BuildRequires:  systemd

# expand pear macros on install
BuildRequires:  php-pear

# For sanity %%check
BuildRequires:       php-cli
BuildRequires:       php-composer(sabre/dav)  >= 3.0.9
BuildRequires:       php-composer(sabre/dav)  < 4.0
BuildRequires:       php-composer(doctrine/dbal) >= 2.5.4
BuildRequires:       php-composer(doctrine/dbal) < 3
BuildRequires:       php-composer(mcnetic/zipstreamer) >= 1.0
BuildRequires:       php-composer(mcnetic/zipstreamer) < 2.0
BuildRequires:       php-composer(phpseclib/phpseclib) >= 2.0
BuildRequires:       php-composer(phpseclib/phpseclib) < 3.0
BuildRequires:       php-composer(rackspace/php-opencloud) >= 1.9.2
BuildRequires:       php-composer(rackspace/php-opencloud) < 2.0
BuildRequires:       php-composer(jeremeamia/superclosure) >= 2.1.0
BuildRequires:       php-composer(jeremeamia/superclosure) < 3.0
BuildRequires:       php-composer(bantu/ini-get-wrapper) >= 1.0.1
BuildRequires:       php-composer(bantu/ini-get-wrapper) < 2.0
BuildRequires:       php-composer(natxet/CssMin) >= 3.0.4
BuildRequires:       php-composer(natxet/CssMin) < 4.0
BuildRequires:       php-composer(punic/punic) >= 1.6.3
BuildRequires:       php-composer(punic/punic) < 2.0
%if 0%{?el7}
BuildRequires:       php-pear(Archive_Tar) >= 1.3
BuildRequires:       php-pear(Archive_Tar) < 2.0
%else
BuildRequires:       php-composer(pear/archive_tar) >= 1.4.1
BuildRequires:       php-composer(pear/archive_tar) < 2.0
%endif
BuildRequires:       php-composer(patchwork/utf8) >= 1.2.6
BuildRequires:       php-composer(patchwork/utf8) < 2.0
BuildRequires:       php-composer(symfony/console) >= 2.8.3
BuildRequires:       php-composer(symfony/console) < 3.0.0
BuildRequires:       php-composer(symfony/event-dispatcher) >= 2.8.3
BuildRequires:       php-composer(symfony/event-dispatcher) < 3.0.0
BuildRequires:       php-composer(symfony/routing) >= 2.8.1
BuildRequires:       php-composer(symfony/routing) < 3.0.0
BuildRequires:       php-composer(symfony/process) >= 2.8.1
BuildRequires:       php-composer(symfony/process) < 3.0.0
BuildRequires:       php-composer(pimple/pimple) >= 3.0.2
BuildRequires:       php-composer(pimple/pimple) < 4.0
%if 0%{?fedora} < 18 && 0%{?rhel} < 8
BuildRequires:       php-composer(ircmaxell/password-compat) >= 1.0.0
BuildRequires:       php-composer(ircmaxell/password-compat) < 2.0
%endif
BuildRequires:       php-composer(nikic/php-parser) >= 1.4.1
BuildRequires:       php-composer(nikic/php-parser) < 2.0
BuildRequires:       php-composer(icewind/streams) >= 0.4.1
BuildRequires:       php-composer(icewind/streams) < 1.0
BuildRequires:       php-composer(swiftmailer/swiftmailer) >= 5.4.1
BuildRequires:       php-composer(swiftmailer/swiftmailer) < 6.0
BuildRequires:       php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:       php-composer(guzzlehttp/guzzle) < 6.0
BuildRequires:       php-composer(league/flysystem) >= 1.0.20
BuildRequires:       php-composer(league/flysystem) < 2.0
%if 0%{?el7}
BuildRequires:       php-pear(Console_Getopt) > 1.3
BuildRequires:       php-pear(Console_Getopt) < 2.0
BuildRequires:       php-pear(PEAR) > 1.9
%else
BuildRequires:       php-composer(pear/pear-core-minimal) >= 1.10.1
%endif
BuildRequires:       php-composer(interfasys/lognormalizer) >= 1.0
BuildRequires:       php-composer(interfasys/lognormalizer) < 2.0
BuildRequires:       php-composer(owncloud/tarstreamer) >= 0.1
BuildRequires:       php-composer(owncloud/tarstreamer) < 1.0
BuildRequires:       php-composer(patchwork/jsqueeze) >= 2.0
BuildRequires:       php-composer(patchwork/jsqueeze) < 3.0
BuildRequires:       php-composer(symfony/polyfill-php70) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php70) < 2.0
BuildRequires:       php-composer(symfony/polyfill-php55) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php55) < 2.0
BuildRequires:       php-composer(symfony/polyfill-php56) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php56) < 2.0
BuildRequires:       php-composer(lukasreschke/id3parser) >= 0.0.1
BuildRequires:       php-composer(lukasreschke/id3parser) < 1.0.0
BuildRequires:       php-composer(icewind/smb) >= 1.1.0
BuildRequires:       php-composer(icewind/smb) < 2.0
BuildRequires:       php-pecl(smbclient) >= 0.8.0
BuildRequires:       php-pecl(smbclient) < 2
BuildRequires:       php-composer(google/apiclient) >= 1.1.7
# Note: 1.1.8 has BC breaks
BuildRequires:       php-composer(google/apiclient) < 1.1.8
BuildRequires:       php-composer(aws/aws-sdk-php) >= 2.7.5
BuildRequires:       php-composer(aws/aws-sdk-php) < 3.0.0
BuildRequires:       php-composer(symfony/yaml) >= 2.6.0
BuildRequires:       php-composer(symfony/yaml) < 3.0.0
BuildRequires:       php-pear(pear.dropbox-php.com/Dropbox)
BuildRequires:       php-composer(onelogin/php-saml) >= 2.9.0
BuildRequires:       php-composer(onelogin/php-saml) < 3.0

Requires:       %{name}-webserver = %{version}-%{release}
Requires:       %{name}-database = %{version}-%{release}

# Core PHP libs/extensions required by OC core
Requires:       php-curl
Requires:       php-dom
Requires:       php-exif
Requires:       php-fileinfo
Requires:       php-gd
Requires:       php-iconv
Requires:       php-json
Requires:       php-ldap
Requires:       php-mbstring
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-session
Requires:       php-simplexml
Requires:       php-xmlwriter
Requires:       php-spl
Requires:       php-zip
Requires:       php-filter

### External PHP libs required by OC core


# "doctrine/dbal": "2.5.4"
# pulls in doctrine/common as a strict requires
# which pulls in doctrine/{annotations,inflector,cache,collections,lexer} as strict requires
Requires:       php-composer(doctrine/dbal) >= 2.5.4
Requires:       php-composer(doctrine/dbal) < 3

#"mcnetic/zipstreamer": "^1.0"
Requires:       php-composer(mcnetic/zipstreamer) >= 1.0
Requires:       php-composer(mcnetic/zipstreamer) < 2.0

# "phpseclib/phpseclib": "2.0.0"
Requires:       php-composer(phpseclib/phpseclib) >= 2.0
Requires:       php-composer(phpseclib/phpseclib) < 3.0

#Requires:       php-composer(rackspace/php-opencloud) >= 1.9.2
# pulls in guzzle/http as a strict requires
# guzzle/http package include common, parser and stream too
Requires:       php-composer(rackspace/php-opencloud) >= 1.9.2
Requires:       php-composer(rackspace/php-opencloud) < 2.0

# "jeremeamia/superclosure": "2.1.0"
Requires:       php-composer(jeremeamia/superclosure) >= 2.1.0
Requires:       php-composer(jeremeamia/superclosure) < 3.0

# "bantu/ini-get-wrapper": "v1.0.1"
Requires:       php-composer(bantu/ini-get-wrapper) >= 1.0.1
Requires:       php-composer(bantu/ini-get-wrapper) < 2.0

# "natxet/CssMin": "dev-master"
Requires:       php-composer(natxet/CssMin) >= 3.0.4
Requires:       php-composer(natxet/CssMin) < 4.0

# "punic/punic": "1.6.3"
Requires:       php-composer(punic/punic) >= 1.6.3
Requires:       php-composer(punic/punic) < 2.0

# "pear/archive_tar": "1.4.1"
# archive_tar is in base el7 and doesn't have the fedora php-composer provides
%if 0%{?el7}
Requires:       php-pear(Archive_Tar) >= 1.3
Requires:       php-pear(Archive_Tar) < 2.0
%else
Requires:       php-composer(pear/archive_tar) >= 1.4.1
Requires:       php-composer(pear/archive_tar) < 2.0
%endif

# "patchwork/utf8": "1.2.6"
Requires:       php-composer(patchwork/utf8) >= 1.2.6
Requires:       php-composer(patchwork/utf8) < 2.0

# "symfony/console": "2.8.3"
Requires:       php-composer(symfony/console) >= 2.8.3
Requires:       php-composer(symfony/console) < 3.0.0
# "symfony/event-dispatcher": "2.8.3"
Requires:       php-composer(symfony/event-dispatcher) >= 2.8.3
Requires:       php-composer(symfony/event-dispatcher) < 3.0.0
# "symfony/routing": "2.8.1"
Requires:       php-composer(symfony/routing) >= 2.8.1
Requires:       php-composer(symfony/routing) < 3.0.0
# "symfony/process": "2.8.1"
Requires:       php-composer(symfony/process) >= 2.8.1
Requires:       php-composer(symfony/process) < 3.0.0

# "pimple/pimple": "3.0.2"
Requires:       php-composer(pimple/pimple) >= 3.0.2
Requires:       php-composer(pimple/pimple) < 4.0

%if 0%{?fedora} < 18 && 0%{?rhel} < 8
# "ircmaxell/password-compat": "1.0.*"
Requires:       php-composer(ircmaxell/password-compat) >= 1.0.0
Requires:       php-composer(ircmaxell/password-compat) < 2.0
%endif

# "nikic/php-parser": "1.4.1"
Requires:       php-composer(nikic/php-parser) >= 1.4.1
Requires:       php-composer(nikic/php-parser) < 2.0

# "icewind/Streams": "0.4.1"
Requires:       php-composer(icewind/streams) >= 0.4.1
Requires:       php-composer(icewind/streams) < 1.0

# "swiftmailer/swiftmailer": "@stable"
# Version 5.4.1 for autoloader in /usr/share/php
Requires:       php-composer(swiftmailer/swiftmailer) >= 5.4.1
Requires:       php-composer(swiftmailer/swiftmailer) < 6.0

# "guzzlehttp/guzzle": "5.3.0"
# pulls in guzzlehttp/ringphp as strict requires
# ringphp pulls in guzzlehttp/streams and react/promise as strict requires
Requires:       php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:       php-composer(guzzlehttp/guzzle) < 6.0

# "league/flysystem": "1.0.20"
Requires:       php-composer(league/flysystem) >= 1.0.20
Requires:       php-composer(league/flysystem) < 2.0


# "pear/pear-core-minimal": "v1.10.1"
# this includes pear/console_getopt and pear/PEAR
%if 0%{?el7}
Requires:       php-pear(Console_Getopt) > 1.3
Requires:       php-pear(Console_Getopt) < 2.0
Requires:       php-pear(PEAR) > 1.9
%else
Requires:       php-composer(pear/pear-core-minimal) >= 1.10.1
%endif

# "interfasys/lognormalizer": "v1.0"
Requires:       php-composer(interfasys/lognormalizer) >= 1.0
Requires:       php-composer(interfasys/lognormalizer) < 2.0

# "deepdiver1975/TarStreamer": "v0.1.0"
# Despite the difference in name this is correct
# https://github.com/owncloud/3rdparty/tree/master/deepdiver1975/tarstreamer
Requires:       php-composer(owncloud/tarstreamer) >= 0.1
Requires:       php-composer(owncloud/tarstreamer) < 1.0

# "patchwork/jsqueeze": "^2.0"
Requires:       php-composer(patchwork/jsqueeze) >= 2.0
Requires:       php-composer(patchwork/jsqueeze) < 3.0

# "sabre/dav" : "3.0.9"
# pulls in sabre event, http and vobject, xml, uri as strict requires
Requires:       php-composer(sabre/dav)  >= 3.0.9
Requires:       php-composer(sabre/dav)  < 4.0

# symfony/polyfill-mbstring is not in composer.json but is in the 3rdparty folder
# we don't need it though as we ship mbstring itself

# "symfony/polyfill-php70": "^1.0",
# pulls in s strict requires of paragonie/random_compat
Requires:       php-composer(symfony/polyfill-php70) >= 1.0
Requires:       php-composer(symfony/polyfill-php70) < 2.0
# "symfony/polyfill-php55": "^1.0",
Requires:       php-composer(symfony/polyfill-php55) >= 1.0
Requires:       php-composer(symfony/polyfill-php55) < 2.0
# "symfony/polyfill-php56": "^1.0"
Requires:       php-composer(symfony/polyfill-php56) >= 1.0
Requires:       php-composer(symfony/polyfill-php56) < 2.0

# "lukasreschke/id3parser": "^0.0.1"
Requires:       php-composer(lukasreschke/id3parser) >= 0.0.1
Requires:       php-composer(lukasreschke/id3parser) < 1.0.0

### For dependencies of apps/files_external

## SMB/CIFS external storage stuff

#"icewind/smb": "1.1.0"
# note that streams is a dep but already required by core anyway
Requires:       php-composer(icewind/smb) >= 1.1.0
Requires:       php-composer(icewind/smb) < 2.0
# This makes smb external storage usable in performance
# and doesn't break things like encryption due to timeouts
Requires:       php-pecl(smbclient) >= 0.8.0
Requires:       php-pecl(smbclient) < 2


# Requiring so that the shipped external smb storage works
# The net command is needed and enabling smb tests for smbclient command
Requires:       samba-common-tools
Requires:       samba-client

## Note these next bits are not listed in composer but manually dropped in place

## Dropbox external storage
Requires:       php-pear(pear.dropbox-php.com/Dropbox)

## Google Drive external storage
## Note: 1.1.8 has BC breaks
Requires:       php-composer(google/apiclient) >= 1.1.7
Requires:       php-composer(google/apiclient) < 1.1.8

## AWS S3 external storage
Requires:       php-composer(aws/aws-sdk-php) >= 2.7.0
Requires:       php-composer(aws/aws-sdk-php) < 3.0.0

## For dependency of apps/gallery
# "symfony/yaml": "~2.6"
Requires:       php-composer(symfony/yaml) >= 2.6.0
Requires:       php-composer(symfony/yaml) < 3.0.0

## For dependency of app/user_saml
# "onelogin/php-saml": "^2.9"
Requires:       php-composer(onelogin/php-saml) >= 2.9.0
Requires:       php-composer(onelogin/php-saml) < 3.0.0

# Need to label the httpd rw stuff correctly until base selinux policy updated
Requires(post):   %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

# Bundled javascript libraries in core vendor
# State of javascript in fedora right now is too painful to unbundle
Provides: bundled(js-base64) = 0.3.0
Provides: bundled(js-blueimp-md5) = 1.1.0
Provides: bundled(js-bootstrap/tooltip) = 3.3.6
Provides: bundled(js-clipboard) = 1.5.12
Provides: bundled(js-davclient)
Provides: bundled(js-es6-promise) = 2.3.0
Provides: bundled(js-handlebars) = 1.3.0
Provides: bundled(js-jcrop) = 0.9.12
Provides: bundled(js-jquery-ui) = 1.10
Provides: bundled(js-jsTimezoneDetect) = 1.0.6
Provides: bundled(js-moment) = 2.10.3
Provides: bundled(js-select2) = 3.4.8
Provides: bundled(js-snapjs) = 2.0.0
Provides: bundled(js-strengthify) = 0.5.1
Provides: bundled(js-zxcvbn) = gitf2a8cda13d
Provides: bundled(js-jquery) = 2.1.4
Provides: bundled(js-jquery-migrate) = 1.4.0
Provides: bundled(js-backbone) = 1.2.3
Provides: bundled(js-underscore) = 1.8.3
# bundled from files_pdfviewer
Provides: bundled(js-pdfjs) = 1.1.469
# bundled from files_theming
Provides: bundled(js-jscolor) = 2.0.4
# bundled from federatedfilesharing
Provides: bundled(js-gs-share)
# bundled from files_texteditor
Provides: bundled(js-ace)
# bundled from user_ldap
Provides: bundled(js-jquery-multiselect) = 1.13
# bundled from gallery
Provides: bundled(js-bigshot)
Provides: bundled(js-commonmark) = 0.22.0
Provides: bundled(js-dompurify) = 0.7.0
Provides: bundled(js-eventsource-polyfill) = 0.9.7
Provides: bundled(js-jquery-touchevents) = 1.0.1
Provides: bundled(js-jqueryui-touch-punch) = 0.2.3

%description
NextCloud gives you universal access to your files through a web interface or
WebDAV. It also provides a platform to easily view & sync your contacts,
calendars and bookmarks across all your devices and enables basic editing right
on the web. NextCloud is extendable via a simple but powerful API for
applications and plugins.


%package httpd
Summary:    Httpd integration for NextCloud

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:       php

%description httpd
%{summary}.


%package nginx
Summary:    Nginx integration for NextCloud

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:   php-fpm nginx

%description nginx
%{summary}.


%package mysql
Summary:    MySQL database support for NextCloud

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# From getSupportedDatabases, mysql => pdo, mysql
Requires:   php-pdo_mysql

%description mysql
This package ensures the necessary dependencies are in place for NextCloud to
work with MySQL / MariaDB databases. It does not require a MySQL / MariaDB
server to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as NextCloud itself, you must
also install and enable a MySQL / MariaDB server package. See README.mysql for
more details.

%package postgresql
Summary:    PostgreSQL database support for NextCloud

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# From getSupportedDatabases, pgsql => function, pg_connect
Requires:   php-pgsql

%description postgresql
This package ensures the necessary dependencies are in place for NextCloud to
work with a PostgreSQL database. It does not require the PostgreSQL server
package to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as NextCloud itself, you must
also install and enable the PostgreSQL server package. See README.postgresql
for more details.


%package sqlite
Summary:    SQLite 3 database support for NextCloud

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
# From getSupportedDatabases, pgsql => class, SQLite3
Requires:   php-sqlite3 php-pcre

%description sqlite
This package ensures the necessary dependencies are in place for NextCloud to
work with an SQLite 3 database stored on the local system.


%prep
%autosetup -n %{name} -p1

# patch backup files and .git stuff
find . -name \*.orig    -type f        -exec rm    {} \; -print
find . -name .gitignore -type f        -exec rm    {} \; -print
find . -name .github    -type d -prune -exec rm -r {} \; -print

# prepare package doc
cp %{SOURCE3} README.fedora
cp %{SOURCE4} README.mysql
cp %{SOURCE5} README.postgresql
cp %{SOURCE6} MIGRATION.fedora

mv 3rdparty/composer.json 3rdparty_composer.json
mv apps/files_external/3rdparty/composer.json files_external_composer.json
mv apps/gallery/composer.json gallery_composer.json
mv apps/user_saml/3rdparty/composer.json user_saml_composer.json

# Explicitly remove the bundled libraries we're aware of
pushd 3rdparty
rm -r doctrine/{annotations,cache,collections,common,dbal,inflector,lexer}
rm -r mcnetic/zipstreamer
rm -r phpseclib/phpseclib
rm -r rackspace/php-opencloud guzzle/{http,common,parser,stream}
rm -r jeremeamia/SuperClosure
rm -r bantu/ini-get-wrapper
rm -r natxet/CssMin
rm -r punic/punic
rm -r pear/archive_tar
rm -r patchwork/utf8
rm -r symfony/console
rm -r symfony/event-dispatcher
rm -r symfony/routing
rm -r symfony/process
rm -r pimple/pimple
rm -r ircmaxell/password-compat
rm -r nikic/php-parser
rm -r icewind/streams
rm -r swiftmailer/swiftmailer
rm -r guzzlehttp/{guzzle,ringphp,streams} react/promise
rm -r league/flysystem
rm -r pear/{pear-core-minimal,console_getopt,pear_exception}
rm -r interfasys/lognormalizer
rm -r deepdiver1975/tarstreamer
rm -r patchwork/jsqueeze
rm -r sabre/{dav,event,http,vobject,uri,xml}
rm -r symfony/polyfill-{php55,php56,php70,mbstring,util}
rm -r paragonie/random_compat
rm -r lukasreschke/id3parser
rm README.md

# remove composer stuff
rm -r composer*

# clean up any empty directories
find -type d -empty  -delete

# remove extraneous files now we've cleaned up
rm "LICENSE INFO" patches.txt

# add our Fedora autoloader
cp %{SOURCE8} ./autoload.php

# Set the vendor directory to macro based datadir in our autoloader
sed -i "s,##DATADIR##,%{_datadir}," autoload.php
popd


# remove files_external bundled libraries
rm -r apps/files_external/3rdparty/{icewind,Dropbox,google-api-php-client,aws-sdk-php,composer*}

# create autoloader, from composer.json, "require": {
#                "icewind/smb": "1.0.4",
#                "icewind/streams": "0.2"
# include stuff required directly but not in composer too
cat << 'EOF' | tee apps/files_external/3rdparty/autoload.php
<?php
require_once '%{_datadir}/php/Icewind/Streams/autoload.php';
require_once '%{_datadir}/php/Icewind/SMB/autoload.php';
require_once '%{_datadir}/pear/Dropbox/autoload.php';
if (file_exists('%{_datadir}/php/Google1/autoload.php')) {
    require_once '%{_datadir}/php/Google1/autoload.php';
} else {
    require_once '%{_datadir}/php/Google/autoload.php';
}
require_once '%{_datadir}/php/Aws/autoload.php';
EOF

# remove gallery external bundled libraries
rm -r apps/gallery/vendor/{symfony,composer*}
rm    apps/gallery/composer.lock

# create autoloader, from composer.json, "require": {
#                "symfony/yaml": "_2.6"
cat << 'EOF' | tee apps/gallery/vendor/autoload.php
<?php
require_once '%{_datadir}/php/Symfony/Component/Yaml/autoload.php';
EOF

# remove user_saml external bundled libraries
rm -r apps/user_saml/3rdparty/vendor/{composer*,onelogin}
rm apps/user_saml/3rdparty/composer.lock

# create autoloader
cat << 'EOF' | tee apps/user_saml/3rdparty/vendor/autoload.php
<?php
require_once '%{_datadir}/php/OneLogin/Saml2/autoload.php';
EOF

# clean up content
for f in {l10n.pl,init.sh,setup_owncloud.sh,image-optimization.sh,install_dependencies.sh}; do
    find . -name "$f" -delete
done

rm ./l10n/rm-old.sh
rm ./apps/gallery/build/after_failure.sh
rm ./apps/gallery/build/documentation/docpublisher.sh
rm ./apps/gallery/build/xdebug_install.sh

find -name '.tx' -print0 | xargs -0 rm -rf
find -name '.bower.json' -print0 | xargs -0 rm -rf

find . -size 0 -type f -delete

# let's not ship upstream's 'updatenotification' app, which has zero chance of working and
# a big chance of blowing things up
rm -dr apps/updatenotification
# also remove the actual updater
rm -r updater

# Locate license files and put them sensibly in place
mv apps/files_pdfviewer/vendor/pdfjs/LICENSE js-pdfjs-LICENSE
mv apps/files_pdfviewer/vendor/pdfjs/web/cmaps/LICENSE js-pdfjs-cmaps-LICENSE
mv apps/files_retention/LICENSE files_retention-LICENSE
mv apps/gallery/COPYING gallery-LICENSE
mv apps/gallery/js/vendor/bigshot/LICENSE.txt js-bigshot-LICENSE
mv apps/gallery/js/vendor/commonmark/LICENSE js-commonmark-LICENSE
mv apps/gallery/js/vendor/dompurify/LICENSE js-dompurify-LICENSE
mv apps/gallery/js/vendor/eventsource-polyfill/LICENSE js-eventsource-polyfill-LICENSE
mv apps/notifications/COPYING notifications-LICENSE
mv apps/password_policy/LICENSE password_policy-LICENSE
mv apps/serverinfo/COPYING serverinfo-LICENSE
mv apps/survey_client/COPYING survey_client-LICENSE
mv apps/theming/js/3rdparty/jscolor/LICENSE.txt js-jscolor-LICENSE
mv apps/user_ldap/vendor/ui-multiselect/MIT-LICENSE js-jqueryui-multiselect-LICENSE
mv COPYING-AGPL nextcloud-LICENSE
mv core/fonts/LICENSE.txt fonts-LICENSE
mv core/vendor/backbone/LICENSE js-backbone-LICENSE
mv core/vendor/base64/LICENSE js-base64-LICENSE
mv core/vendor/davclient.js/LICENSE js-davclient-LICENSE
mv core/vendor/es6-promise/LICENSE js-es6-promise-LICENSE
mv core/vendor/jcrop/MIT-LICENSE.txt js-jcrop-LICENSE
mv core/vendor/jquery/MIT-LICENSE.txt js-jquery-LICENSE
mv core/vendor/jquery-ui/MIT-LICENSE.txt js-jquery-ui-LICENSE
mv core/vendor/jsTimezoneDetect/LICENCE.txt js-jsTimezoneDetect-LICENSE
mv core/vendor/moment/LICENSE js-moment-LICENSE
mv core/vendor/select2/LICENSE js-select2-LICENSE
mv core/vendor/strengthify/LICENSE js-strengthify-LICENSE
mv core/vendor/underscore/LICENSE js-underscore-LICENSE
mv core/vendor/zxcvbn/LICENSE.txt js-zxcvbn-LICENSE
mv lib/composer/composer/LICENSE composer-LICENSE

%check
# files_external checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty | wc -l)
if [ $nb -gt 1  ]; then
  false apps/files_external/3rdparty must only have autoload.php
fi

if grep -r 3rdparty %{buildroot}%{_datadir}/%{name}/apps/files_external \
   | grep -v 3rdparty/autoload.php | grep -v signature.json; then
   false App files_external needs to be adapted
fi

php %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty/autoload.php

# gallery checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/gallery/vendor | wc -l)
if [ $nb -gt 1  ]; then
  false apps/gallery/vendor must only have autoload.php
fi

php %{buildroot}%{_datadir}/%{name}/apps/gallery/vendor/autoload.php

# user_saml checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/user_saml/3rdparty/vendor | wc -l)
if [ $nb -gt 1  ]; then
  false apps/user_saml/3rdparty/vendor must only have autoload.php
fi

php %{buildroot}%{_datadir}/%{name}/apps/user_saml/3rdparty/vendor/autoload.php

# core checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/3rdparty | wc -l)
if [ $nb -gt 1  ]; then
  false core 3rdparty must only have autoload.php
fi

php %{buildroot}%{_datadir}/%{name}/3rdparty/autoload.php

# There should not be an composer.json files remaining
nb=$(find -name 'composer.*' | wc -l)
if [ $nb -gt 0 ]
  then
  false found unexpected composer.json files
fi

# Make sure there are no license files left over
nb=$( find . -mindepth 2 \( -name '*LICENSE*' -o -name '*LICENCE*' -o  -name '*COPYING*' \) | wc -l )
if [ $nb -gt 0 ]
  then
  false found unexpected licenses to verify
fi


%build
# Nothing to build


%install
install -dm 755 %{buildroot}%{_datadir}/%{name}

# create nextcloud datadir
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
# create writable app dir for appstore
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/apps
# create nextcloud sysconfdir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# install content
for d in $(find . -mindepth 1 -maxdepth 1 -type d | grep -v config); do
    cp -a "$d" %{buildroot}%{_datadir}/%{name}
done

for f in {*.php,*.xml,*.html,occ,robots.txt}; do
    install -pm 644 "$f" %{buildroot}%{_datadir}/%{name}
done

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

# nextcloud looks for ca-bundle.crt in config dir
ln -sf %{_sysconfdir}/pki/tls/certs/ca-bundle.crt %{buildroot}%{_sysconfdir}/%{name}/ca-bundle.crt

# set default config
install -pm 644 %{SOURCE7}    %{buildroot}%{_sysconfdir}/%{name}/config.php

# httpd config
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
install -Dpm 644 %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/

# nginx config
install -Dpm 644 %{SOURCE200} \
    %{buildroot}%{_sysconfdir}/nginx/default.d/%{name}.conf
install -Dpm 644 %{SOURCE201} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf

%if 0%{?el7}
install -Dpm 644 %{SOURCE203} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf
%else
install -Dpm 644 %{SOURCE202} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf
%endif

# Install the systemd timer
install -Dpm 644 %{SOURCE10} %{buildroot}%{_unitdir}/nextcloud-cron.service
install -Dpm 644 %{SOURCE11} %{buildroot}%{_unitdir}/nextcloud-cron.timer

%post httpd
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :

%postun httpd
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
fi

%post nginx
%if 0%{?el7}
  # Work around missing php session directory for php-fpm in el7 bz#1338444
  if [ ! -d /var/lib/php/session ]
    then
    mkdir /var/lib/php/session
  fi
  /usr/bin/chown apache /var/lib/php/session
%endif
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :

%postun nginx
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
fi

# the selinux policies only cover owncloud right now
# once this package is accepted pull request for selinux-policy to add
# these will be made
%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_sysconfdir}/%{name} || :
restorecon -R %{_localstatedir}/lib/%{name} || :

%postun
if [ $1 -eq 0  ] ; then
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%doc AUTHORS README.fedora MIGRATION.fedora config/config.sample.php
%doc *_composer.json

%license *-LICENSE

%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
# contains sensitive data (dbpassword, passwordsalt)
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.php
# need the symlink in confdir but it's not config
%{_sysconfdir}/%{name}/ca-bundle.crt

%{_datadir}/%{name}
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}
# user data must not be world readable
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/data
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/apps

%{_unitdir}/nextcloud-cron.service
%{_unitdir}/nextcloud-cron.timer

%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
%{_sysconfdir}/httpd/conf.d/*.inc

%files nginx
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/%{name}.conf

%files mysql
%doc README.mysql
%files postgresql
%doc README.postgresql
%files sqlite


%changelog
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  9 2019 Remi Collet <remi@remirepo.net> - 10.0.4-6
- drop dependency on php-password-compat #1658730
- allow php-smbclient 1.0.0 #1663672
- allow doctrine/dbal 2.x

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 10.0.4-2
- Add max versions to dependencies to limit each to 1 major version
- Update some dependencies to use php-composer(*) instead of package names
- Prepare for php-composer(google/apiclient) version 2 and new version 1 package

* Tue Feb 28 2017 James Hogarth <james.hogarth@gmail.com> - 10.0.4-1
- update to 10.0.4
- Add migration from owncloud documentation
- Add systemd timer for background jobs

* Wed Feb 08 2017 James Hogarth <james.hogarth@gmail.com> - 10.0.3-1
- update to 10.0.3

* Thu Oct 06 2016 James Hogarth <james.hogarth@gmail.com> - 10.0.1-1
- update to 10.0.1

* Mon Aug 01 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.53-5
- Use lua to have a common srpm between epel7 and fedora

* Fri Jul 29 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.53-4
- Don't unbundle javascript on EPEL7 due to versioning issues

* Fri Jul 29 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.53-3
- Unbundle javascript libraries from core where possible

* Tue Jul 26 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.53-2
- Update the autoloader to use the path from the approved package

* Tue Jul 19 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.53-1
- New release 9.0.53

* Thu Jul 14 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.52-1
- Initial nextcloud build
