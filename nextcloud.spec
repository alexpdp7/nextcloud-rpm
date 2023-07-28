Name:           nextcloud
Version:        27.0.1
Release:        1%{?dist}
Summary:        Private file sync and share server
License:        AGPLv3+ and MIT and BSD and ASL 2.0 and WTFPL and CC-BY-SA and GPLv3+ and Adobe
URL:            http://nextcloud.com
Source0:        https://download.nextcloud.com/server/releases/%{name}-%{version}.tar.bz2

# basic nextcloud config.php, nextcloud's
# initial setup will fill out other settings appropriately
Source1:        %{name}-config.php
# Systemd timer for background jobs
Source2:       %{name}-systemd-timer.service
Source3:       %{name}-systemd-timer.timer
# httpd config files
Source100:      %{name}-httpd.conf
Source101:      %{name}-access-httpd.conf.avail
Source102:      %{name}-auth-any.inc
Source103:      %{name}-auth-local.inc
Source104:      %{name}-auth-none.inc
Source105:      %{name}-defaults.inc
# nginx/php-fpm  config files
Source200:      %{name}-default-nginx.conf
Source201:      %{name}-conf-nginx.conf
Source202:      %{name}-php-fpm.conf
# packaging notes and doc
Source300:      %{name}-README.fedora
Source301:      %{name}-mysql.txt
Source302:      %{name}-postgresql.txt
Source303:      %{name}-MIGRATION.fedora

# Remove updater version check, we know that updates across more than one
# version are possible
Patch0:         0000-disable-update-version-check.patch
# Change occ shebang to /usr/bin/php
Patch1:         0001-mangle-shebang.patch

BuildArch:      noarch
# For the systemd macros
%if 0%{?fedora} > 29
BuildRequires:  systemd-rpm-macros
%else
BuildRequires:  systemd
%endif
# expand pear macros on install
BuildRequires:  php-pear

# Require one webserver and database backend
Requires:       %{name}-webserver = %{version}-%{release}
Requires:       %{name}-database = %{version}-%{release}
# Require php CLI for occ command
Requires:       php-cli
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
Requires:       php-ldap
Requires:       php-smbclient
Requires:       php-gmp
Requires:       php-process
Requires:       php-pecl-imagick
Requires:       php-pecl-memcached
Requires:       php-pecl-apcu
Requires:       php-pecl-redis5
# For systemd support during install/uninstall
%{?systemd_requires}
# the CA cert bundle is linked to from the config dir
Requires:       %{_sysconfdir}/pki/tls/certs/ca-bundle.crt

# Bundled composer libraries
# many of these can be unbundled
Provides: bundled(php-composer(amphp/amp)) = 2.6.2
Provides: bundled(php-composer(amphp/byte-stream)) = 1.8.1
Provides: bundled(php-composer(amphp/parallel)) = 1.4.1
Provides: bundled(php-composer(amphp/parser)) = 1.0.0
Provides: bundled(php-composer(amphp/process)) = 1.1.4
Provides: bundled(php-composer(amphp/serialization)) = 1.0.0
Provides: bundled(php-composer(amphp/sync)) = 1.4.2
Provides: bundled(php-composer(darsyn/ip)) = 4.1.0
Provides: bundled(php-composer(league/flysystem)) = 2.5.0
Provides: bundled(php-composer(league/mime-type-detection)) = 1.11.0
Provides: bundled(php-composer(psr/log)) = 1.1.4
Provides: bundled(php-composer(rubix/ml)) = 20
Provides: bundled(php-composer(rubix/tensor)) = 2.2.3
Provides: bundled(php-composer(symfony/polyfill-mbstring)) = 1.26.0
Provides: bundled(php-composer(symfony/polyfill-php73)) = 1.26.0
Provides: bundled(php-composer(symfony/polyfill-php80)) = 1.26.0
Provides: bundled(php-composer(composer/semver)) = 3.2.5
Provides: bundled(php-composer(composer/xdebug-handler)) = 2.0.2
Provides: bundled(php-composer(doctrine/annotations)) = 1.13.2
Provides: bundled(php-composer(doctrine/lexer)) = 1.2.1
Provides: bundled(php-composer(friendsofphp/php-cs-fixer)) = 2.19.2
Provides: bundled(php-composer(nextcloud/coding-standard)) = 0.5.0
Provides: bundled(php-composer(php-cs-fixer/diff)) = 1.3.1
Provides: bundled(php-composer(psr/cache)) = 1.0.1
Provides: bundled(php-composer(psr/container)) = 1.1.1
Provides: bundled(php-composer(psr/event-dispatcher)) = 1.0.0
Provides: bundled(php-composer(psr/log)) = 1.1.4
Provides: bundled(php-composer(symfony/console)) = 5.3.7
Provides: bundled(php-composer(symfony/deprecation-contracts)) = 2.4.0
Provides: bundled(php-composer(symfony/event-dispatcher)) = 5.3.7
Provides: bundled(php-composer(symfony/event-dispatcher-contracts)) = 2.4.0
Provides: bundled(php-composer(symfony/filesystem)) = 5.3.4
Provides: bundled(php-composer(symfony/finder)) = 5.3.7
Provides: bundled(php-composer(symfony/options-resolver)) = 5.3.7
Provides: bundled(php-composer(symfony/polyfill-ctype)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-intl-grapheme)) = 1.23.1
Provides: bundled(php-composer(symfony/polyfill-intl-normalizer)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-mbstring)) = 1.23.1
Provides: bundled(php-composer(symfony/polyfill-php70)) = 1.20.0
Provides: bundled(php-composer(symfony/polyfill-php72)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-php73)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-php80)) = 1.23.1
Provides: bundled(php-composer(symfony/process)) = 5.3.7
Provides: bundled(php-composer(symfony/service-contracts)) = 2.4.0
Provides: bundled(php-composer(symfony/stopwatch)) = 5.3.4
Provides: bundled(php-composer(symfony/string)) = 5.3.7
Provides: bundled(php-composer(christian-riesen/base32)) = 1.6.0
Provides: bundled(php-composer(rullzer/easytotp)) = 0.1.4
Provides: bundled(php-composer(icewind/smb)) = 3.5.2
Provides: bundled(php-composer(icewind/streams)) = 0.7.4
Provides: bundled(php-composer(aws/aws-crt-php)) = 1.0.2
Provides: bundled(php-composer(aws/aws-sdk-php)) = 3.242.1
Provides: bundled(php-composer(bantu/ini-get-wrapper)) = 1.0.1
Provides: bundled(php-composer(beberlei/assert)) = 3.3.1
Provides: bundled(php-composer(brick/math)) = 0.9.2
Provides: bundled(php-composer(christophwurst/id3parser)) = 0.1.4
Provides: bundled(php-composer(cweagans/composer-patches)) = 1.7.1
Provides: bundled(php-composer(deepdiver/zipstreamer)) = 2.0.0
Provides: bundled(php-composer(deepdiver1975/tarstreamer)) = 2.0.0
Provides: bundled(php-composer(doctrine/cache)) = 2.1.1
Provides: bundled(php-composer(doctrine/dbal)) = 3.1.4
Provides: bundled(php-composer(doctrine/deprecations)) = 0.5.3
Provides: bundled(php-composer(doctrine/event-manager)) = 1.1.1
Provides: bundled(php-composer(doctrine/lexer)) = 1.2.3
Provides: bundled(php-composer(egulias/email-validator)) = 3.1.1
Provides: bundled(php-composer(fgrosse/phpasn1)) = 2.3.0
Provides: bundled(php-composer(fusonic/linq)) = 1.1.0
Provides: bundled(php-composer(fusonic/opengraph)) = 2.2.0
Provides: bundled(php-composer(giggsey/libphonenumber-for-php)) = 8.12.38
Provides: bundled(php-composer(giggsey/locale)) = 2.1
Provides: bundled(php-composer(guzzlehttp/guzzle)) = 7.5.0
Provides: bundled(php-composer(guzzlehttp/promises)) = 1.5.2
Provides: bundled(php-composer(guzzlehttp/psr7)) = 2.4.3
Provides: bundled(php-composer(guzzlehttp/uri-template)) = 0.2.0
Provides: bundled(php-composer(icewind/searchdav)) = 3.0.1
Provides: bundled(php-composer(icewind/streams)) = 0.7.5
Provides: bundled(php-composer(justinrainbow/json-schema)) = 5.2.10
Provides: bundled(php-composer(laravel/serializable-closure)) = 1.2.0
Provides: bundled(php-composer(league/uri)) = 6.4.0
Provides: bundled(php-composer(league/uri-interfaces)) = 2.2.0
Provides: bundled(php-composer(mexitek/phpcolors)) = 1.0.4
Provides: bundled(php-composer(microsoft/azure-storage-blob)) = 1.5.4
Provides: bundled(php-composer(microsoft/azure-storage-common)) = 1.5.2
Provides: bundled(php-composer(mlocati/ip-lib)) = 1.18.0
Provides: bundled(php-composer(mtdowling/jmespath.php)) = 2.6.1
Provides: bundled(php-composer(nextcloud/lognormalizer)) = 1.0.0
Provides: bundled(php-composer(nikic/php-parser)) = 4.10.5
Provides: bundled(php-composer(opis/closure)) = 3.6.3
Provides: bundled(php-composer(pear/archive_tar)) = 1.4.14
Provides: bundled(php-composer(pear/console_getopt)) = 1.4.3
Provides: bundled(php-composer(pear/pear-core-minimal)) = 1.10.10
Provides: bundled(php-composer(pear/pear_exception)) = 1.0.2
Provides: bundled(php-composer(php-ds/php-ds)) = 1.3.0
Provides: bundled(php-composer(php-http/guzzle7-adapter)) = 1.0.0
Provides: bundled(php-composer(php-http/httplug)) = 2.2.0
Provides: bundled(php-composer(php-http/promise)) = 1.1.0
Provides: bundled(php-composer(php-opencloud/openstack)) = 3.1.0
Provides: bundled(php-composer(phpseclib/phpseclib)) = 2.0.38
Provides: bundled(php-composer(pimple/pimple)) = 3.5.0
Provides: bundled(php-composer(psr/container)) = 1.1.1
Provides: bundled(php-composer(psr/event-dispatcher)) = 1.0.0
Provides: bundled(php-composer(psr/http-client)) = 1.0.1
Provides: bundled(php-composer(psr/http-factory)) = 1.0.1
Provides: bundled(php-composer(psr/http-message)) = 1.0.1
Provides: bundled(php-composer(psr/log)) = 1.1.4
Provides: bundled(php-composer(punic/punic)) = 1.6.5
Provides: bundled(php-composer(ralouphie/getallheaders)) = 3.0.3
Provides: bundled(php-composer(ramsey/collection)) = 1.1.3
Provides: bundled(php-composer(ramsey/uuid)) = 4.1.1
Provides: bundled(php-composer(sabre/dav)) = 4.4.0
Provides: bundled(php-composer(sabre/event)) = 5.1.4
Provides: bundled(php-composer(sabre/http)) = 5.1.5
Provides: bundled(php-composer(sabre/uri)) = 2.2.2
Provides: bundled(php-composer(sabre/vobject)) = 4.4.2
Provides: bundled(php-composer(sabre/xml)) = 2.2.5
Provides: bundled(php-composer(scssphp/scssphp)) = 1.8.1
Provides: bundled(php-composer(spomky-labs/base64url)) = 2.0.4
Provides: bundled(php-composer(spomky-labs/cbor-php)) = 2.0.1
Provides: bundled(php-composer(stecman/symfony-console-completion)) = 0.11.0
Provides: bundled(php-composer(swiftmailer/swiftmailer)) = 6.3.0
Provides: bundled(php-composer(symfony/console)) = 4.4.30
Provides: bundled(php-composer(symfony/css-selector)) = 5.4.11
Provides: bundled(php-composer(symfony/deprecation-contracts)) = 2.5.2
Provides: bundled(php-composer(symfony/dom-crawler)) = 5.4.11
Provides: bundled(php-composer(symfony/event-dispatcher)) = 4.4.30
Provides: bundled(php-composer(symfony/event-dispatcher-contracts)) = 1.1.9
Provides: bundled(php-composer(symfony/http-foundation)) = 5.4.10
Provides: bundled(php-composer(symfony/polyfill-ctype)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-iconv)) = 1.27.0
Provides: bundled(php-composer(symfony/polyfill-intl-grapheme)) = 1.23.1
Provides: bundled(php-composer(symfony/polyfill-intl-idn)) = 1.27.0
Provides: bundled(php-composer(symfony/polyfill-intl-normalizer)) = 1.27.0
Provides: bundled(php-composer(symfony/polyfill-mbstring)) = 1.27.0
Provides: bundled(php-composer(symfony/polyfill-php72)) = 1.27.0
Provides: bundled(php-composer(symfony/polyfill-php73)) = 1.23.0
Provides: bundled(php-composer(symfony/polyfill-php80)) = 1.26.0
Provides: bundled(php-composer(symfony/process)) = 4.4.30
Provides: bundled(php-composer(symfony/routing)) = 4.4.30
Provides: bundled(php-composer(symfony/service-contracts)) = 2.4.0
Provides: bundled(php-composer(symfony/translation)) = 4.4.41
Provides: bundled(php-composer(symfony/translation-contracts)) = 2.4.0
Provides: bundled(php-composer(thecodingmachine/safe)) = 1.3.3
Provides: bundled(php-composer(web-auth/cose-lib)) = 3.3.9
Provides: bundled(php-composer(web-auth/metadata-service)) = 3.3.9
Provides: bundled(php-composer(web-auth/webauthn-lib)) = 3.3.9
Provides: bundled(php-composer(doctrine/lexer)) = 1.2.1
Provides: bundled(php-composer(symfony/polyfill-intl-idn)) = 1.22.1
Provides: bundled(php-composer(symfony/polyfill-intl-normalizer)) = 1.22.1
Provides: bundled(php-composer(symfony/polyfill-php72)) = 1.22.1

# OpenIconic icons bundled via sabre-dav
Provides:       bundled(openiconic-fonts) = 1.0.0
# jscolor bundled via themeing app
Provides:       bundled(jscolor) = 2.0.4
# jquery-ui-multiselect bundled via user_ldap app
Provides:       bundled(jquery-ui-multiselect) = 0.3.1
# zxcvbn bundled via core
Provides:       bundled(zxcvbn) = 4.4.2

%description
NextCloud gives you universal access to your files through a web interface or
WebDAV. It also provides a platform to easily view & sync your contacts,
calendars and bookmarks across all your devices and enables basic editing right
on the web. NextCloud is extendable via a simple but powerful API for
applications and plugins.


%package httpd
Summary:        Httpd integration for NextCloud
Provides:       %{name}-webserver = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
# PHP dependencies
Requires:       php-fpm httpd

%description httpd
%{summary}.


%package nginx
Summary:        Nginx integration for NextCloud
Provides:       %{name}-webserver = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
# PHP dependencies
Requires:       php-fpm nginx

%description nginx
%{summary}.


%package mysql
Summary:        MySQL database support for NextCloud
Provides:       %{name}-database = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
# From getSupportedDatabases, mysql => pdo, mysql
Requires:       php-mysqlnd

%description mysql
This package ensures the necessary dependencies are in place for NextCloud to
work with MySQL / MariaDB databases. It does not require a MySQL / MariaDB
server to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as NextCloud itself, you must
also install and enable a MySQL / MariaDB server package. See README.mysql for
more details.

%package postgresql
Summary:        PostgreSQL database support for NextCloud
Provides:       %{name}-database = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
# From getSupportedDatabases, pgsql => function, pg_connect
Requires:       php-pgsql

%description postgresql
This package ensures the necessary dependencies are in place for NextCloud to
work with a PostgreSQL database. It does not require the PostgreSQL server
package to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as NextCloud itself, you must
also install and enable the PostgreSQL server package. See README.postgresql
for more details.


%package sqlite
Summary:        SQLite 3 database support for NextCloud
Provides:       %{name}-database = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
# From getSupportedDatabases, pgsql => class, SQLite3

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
cp %{SOURCE300} README.fedora
cp %{SOURCE301} README.mysql
cp %{SOURCE302} README.postgresql
cp %{SOURCE303} MIGRATION.fedora

# Locate license files and put them sensibly in place
# get rid of all composer licenses
find -wholename "*/composer/LICENSE" -exec mv {} composer-LICENSE \;

find . -mindepth 2 \( -name '*LICENSE*' -o -name '*LICENCE*' \) | { while read a ; do mv "$a" $(echo $a | sed "s_^./__" | tr "/ " "__" )-LICENSE ; done ; }
find . -mindepth 2 -name '*COPYING*' | { while read a ; do mv "$a" $(echo $a | sed "s_^./__" | tr "/ " "__" )-COPYING ; done ; }

%check
# Make sure there are no license files left over
: Check for leftover license files
find . -mindepth 2 \( -name '*LICENSE*' -o -name '*LICENCE*' -o  -name '*COPYING*' \)
nb=$( find . -mindepth 2 \( -name '*LICENSE*' -o -name '*LICENCE*' -o  -name '*COPYING*' \) | wc -l )
if [ $nb -gt 0 ]
  then
  false Found unexpected licenses to verify
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

for f in {*.php,*.html,robots.txt}; do
    install -pm 644 "$f" %{buildroot}%{_datadir}/%{name}
done

# occ should be executable
install -pm 755 occ %{buildroot}%{_datadir}/%{name}

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

# nextcloud looks for ca-bundle.crt in config dir
ln -sf %{_sysconfdir}/pki/tls/certs/ca-bundle.crt %{buildroot}%{_sysconfdir}/%{name}/ca-bundle.crt

# set default config
install -pm 644 %{SOURCE1}    %{buildroot}%{_sysconfdir}/%{name}/config.php

# httpd config
install -Dpm 644 %{SOURCE100} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -Dpm 644 %{SOURCE101} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
install -Dpm 644 %{SOURCE102} %{SOURCE103} %{SOURCE104} %{SOURCE105} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/

# nginx config
install -Dpm 644 %{SOURCE200} \
    %{buildroot}%{_sysconfdir}/nginx/default.d/%{name}.conf
install -Dpm 644 %{SOURCE201} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf

# php-fpm config
install -Dpm 644 %{SOURCE202} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf

# Install the systemd timer
install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/nextcloud-cron.service
install -Dpm 644 %{SOURCE3} %{buildroot}%{_unitdir}/nextcloud-cron.timer

%post httpd
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
/usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :

%postun httpd
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
fi

%post nginx
/usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
/usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :

%postun nginx
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
fi

%files
%doc AUTHORS README.fedora MIGRATION.fedora config/config.sample.php
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
%{_sysconfdir}/httpd/conf.d/%{name}*.inc
%config(noreplace) %{_sysconfdir}/php-fpm.d/%{name}.conf

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
* Fri Jul 28 2023 Alex Corcoles <alex@corcoles.net> - 27.0.1-1
- Update to Nextcloud 27.0.1
- Deal with licenses automatically
- Get latest provided/bundles from Fedora package
- Now requires PHP 8.0! Use the corresponding Remi module

* Thu Dec 8 2022 Alex Corcoles <alex@corcoles.net> - 25.0.2-1
- Update to Nextcloud 25.0.2

* Sat Nov 5 2022 Alex Corcoles <alex@corcoles.net> - 25.0.1-1
- Update to Nextcloud 25.0.1

* Wed Oct 12 2022 Alex Corcoles <alex@corcoles.net> - 24.0.6-1
- Update to Nextcloud 24.0.6
- Also incorporate latest updates from Fedora package

* Sat Sep 10 2022 Alex Corcoles <alex@corcoles.net> - 24.0.5-1
- Update to Nextcloud 24.0.5
- Also incorporate latest updates from Fedora package

* Sat Aug 14 2022 Alex Corcoles <alex@corcoles.net> - 24.0.4-1
- Update to Nextcloud 24.0.4

* Mon Jul 18 2022 Alex Corcoles <alex@corcoles.net> - 24.0.3-1
- Update to Nextcloud 24.0.3

* Sat Jun 25 2022 Alex Corcoles <alex@corcoles.net> - 24.0.2-1
- Update to Nextcloud 24.0.2

* Sat Jun 18 2022 Alex Corcoles <alex@corcoles.net> - 24.0.1-1
- Update to Nextcloud 24.0.1

* Thu Mar 31 2022 Alex Corcoles <alex@corcoles.net> - 23.0.3-1
- Update to Nextcloud 23.0.3

* Sat Jan 29 2022 Alex Corcoles <alex@corcoles.net> - 23.0.0-1
- Update to Nextcloud 23.0.0

* Sat Nov 13 2021 Alex Corcoles <alex@corcoles.net> - 22.2.1-1
- Update to Nextcloud 22.2.1

* Fri Sep 17 2021 Alex Corcoles <alex@corcoles.net> - 22.1.1-1
- Update to Nextcloud 22.1.1

* Fri Aug 20 2021 Alex Corcoles <alex@corcoles.net> - 22.1.0-1
- Update to Nextcloud 22.1.0

* Tue Jul  6 2021 Christopher Engelhard <ce@lcts.de> - 22.0.0-1
- Update to 22.0.0

* Fri Jul 2 2021 Alex Corcoles <alex@corcoles.net> - 21.0.3-1
- Update to Nextcloud 21.0.3

* Wed Jun 30 2021 Christopher Engelhard <ce@lcts.de> - 21.0.2-1
- Update to 21.0.2, fixes RHBZ 1977202 / CVE-2021-22915
- Include php-fpm config in httpd subpackage
- Set php memory limit to 512MB (RHBZ 1933529)
- Add Referrer-policy no-referrer to nginx config (RHBZ 1933530)

* Sat May 22 2021 Alex Corcoles <alex@corcoles.net> - 21.0.2-1
- Update to Nextcloud 21.0.2
- Rebase with Fedora to pick up:
  Wed Feb 24 2021 Christopher Engelhard <ce@lcts.de> - 21.0.0-2
  Drop dependency on php-imap. Fixes RHBZ #1933023

* Fri Apr 9 2021 Alex Corcoles <alex@corcoles.net> - 21.0.1-1
- Update to Nextcloud 21.0.1

* Wed Feb 24 2021 Christopher Engelhard <ce@lcts.de> - 21.0.0-1
- Update to 21.0.0

* Sat Feb 20 2021 Christopher Engelhard <ce@lcts.de> - 20.0.7-1
- Update to 20.0.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Christopher Engelhard <ce@lcts.de> - 20.0.5-1
- Update to 20.0.5

* Mon Dec 28 2020 Christopher Engelhard <ce@lcts.de> - 20.0.4-2
- Remove duplicate dependencies on database drivers
- Remove syslinux related stuff, as these are included in
  the syslinux policy
- Add Provides: for bundled libraries

* Thu Dec 17 2020 Christopher Engelhard <ce@lcts.de> - 20.0.4-1
- Update to 20.0.4

* Thu Dec 10 2020 Christopher Engelhard <ce@lcts.de> - 20.0.3-1
- Update to 20.0.3

* Thu Nov 19 2020 Christopher Engelhard <ce@lcts.de> - 20.0.2-1
- Update to 20.0.2

* Sat Nov 14 2020 Christopher Engelhard <ce@lcts.de> - 20.0.2-0.1.rc1
- Update to 20.0.2RC1

* Wed Nov 11 2020 Christopher Engelhard <ce@lcts.de> - 20.0.1-3
- Remove CentOS/RHEL 7 support from spec file

* Tue Nov 10 2020 Christopher Engelhard <ce@lcts.de> - 20.0.1-2
- Add dependencies on php-cli (for occ) and php-process (for posix)
- Remove unneeded BR on php-cli
- Add patch to allow updates across more than one major version

* Sat Oct 24 2020 Alex Corcoles <alex@corcoles.net> - 20.0.1-1
- Update to Nextcloud 20.0.1

* Sun Oct 04 2020 Alex Corcoles <alex@corcoles.net> - 20.0.0-1
- Update to Nextcloud 20.0.0

* Sat Sep 12 2020 Alex Corcoles <alex@corcoles.net> - 19.0.3-1
- Update to Nextcloud 19.0.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 28 2020 Ivan Chavero <ichavero@redhat.com> - 19.0.0-1
- Update to Nextcloud 19.0.0
- Update licenses

* Thu Apr 30 2020 Ivan Chavero <ichavero@redhat.com> - 18.0.4-1
- Update to Nextcloud 18.0.4

* Sat Feb 08 2020 Ivan Chavero <ichavero@redhat.com> - 18.0.0-1
- Refactor spec file
- Update to Nextcoud 18.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

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
