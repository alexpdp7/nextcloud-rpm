Name:           nextcloud
Version:        21.0.0
Release:        2%{?dist}
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
Provides: bundled(php-composer(icewind/smb)) = 3.2.7
Provides: bundled(php-composer(icewind/streams)) = 0.7.1
Provides: bundled(php-composer(aws/aws-sdk-php)) = 3.171.21
Provides: bundled(php-composer(bantu/ini-get-wrapper)) = 1.0.1
Provides: bundled(php-composer(beberlei/assert)) = 3.3.0
Provides: bundled(php-composer(brick/math)) = 0.9.1
Provides: bundled(php-composer(christophwurst/id3parser)) = 0.1.1
Provides: bundled(php-composer(composer/package-versions-deprecated)) = 1.11.99.1
Provides: bundled(php-composer(deepdiver/zipstreamer)) = 2.0.0
Provides: bundled(php-composer(deepdiver1975/tarstreamer)) = 2.0.0
Provides: bundled(php-composer(doctrine/cache)) = 1.10.2
Provides: bundled(php-composer(doctrine/dbal)) = 3.0.0
Provides: bundled(php-composer(doctrine/event-manager)) = 1.1.1
Provides: bundled(php-composer(doctrine/lexer)) = 1.2.1
Provides: bundled(php-composer(egulias/email-validator)) = 2.1.25
Provides: bundled(php-composer(fgrosse/phpasn1)) = 2.2.0
Provides: bundled(php-composer(giggsey/libphonenumber-for-php)) = 8.12.16
Provides: bundled(php-composer(giggsey/locale)) = 1.9
Provides: bundled(php-composer(guzzlehttp/guzzle)) = 7.2.0
Provides: bundled(php-composer(guzzlehttp/promises)) = 1.4.0
Provides: bundled(php-composer(guzzlehttp/psr7)) = 1.7.0
Provides: bundled(php-composer(guzzlehttp/uri-template)) = 0.2.0
Provides: bundled(php-composer(icewind/searchdav)) = 2.0.0
Provides: bundled(php-composer(icewind/streams)) = 0.7.2
Provides: bundled(php-composer(justinrainbow/json-schema)) = 5.2.10
Provides: bundled(php-composer(league/flysystem)) = 1.1.3
Provides: bundled(php-composer(league/mime-type-detection)) = 1.7.0
Provides: bundled(php-composer(league/uri)) = 6.4.0
Provides: bundled(php-composer(league/uri-interfaces)) = 2.2.0
Provides: bundled(php-composer(microsoft/azure-storage-blob)) = 1.5.2
Provides: bundled(php-composer(microsoft/azure-storage-common)) = 1.5.1
Provides: bundled(php-composer(mtdowling/jmespath.php)) = 2.6.0
Provides: bundled(php-composer(nextcloud/lognormalizer)) = 1.0.0
Provides: bundled(php-composer(nikic/php-parser)) = 4.10.4
Provides: bundled(php-composer(opis/closure)) = 3.6.1
Provides: bundled(php-composer(patchwork/jsqueeze)) = 2.0.5
Provides: bundled(php-composer(pear/archive_tar)) = 1.4.12
Provides: bundled(php-composer(pear/console_getopt)) = 1.4.3
Provides: bundled(php-composer(pear/pear-core-minimal)) = 1.10.10
Provides: bundled(php-composer(pear/pear_exception)) = 1.0.1
Provides: bundled(php-composer(php-ds/php-ds)) = 1.3.0
Provides: bundled(php-composer(php-http/guzzle7-adapter)) = 0.1.1
Provides: bundled(php-composer(php-http/httplug)) = 2.2.0
Provides: bundled(php-composer(php-http/promise)) = 1.1.0
Provides: bundled(php-composer(php-opencloud/openstack)) = 3.1.0
Provides: bundled(php-composer(phpseclib/phpseclib)) = 2.0.30
Provides: bundled(php-composer(pimple/pimple)) = 3.3.1
Provides: bundled(php-composer(psr/container)) = 1.0.0
Provides: bundled(php-composer(psr/http-client)) = 1.0.1
Provides: bundled(php-composer(psr/http-factory)) = 1.0.1
Provides: bundled(php-composer(psr/http-message)) = 1.0.1
Provides: bundled(php-composer(psr/log)) = 1.1.3
Provides: bundled(php-composer(punic/punic)) = 1.6.5
Provides: bundled(php-composer(ralouphie/getallheaders)) = 3.0.3
Provides: bundled(php-composer(ramsey/collection)) = 1.1.1
Provides: bundled(php-composer(ramsey/uuid)) = 4.1.1
Provides: bundled(php-composer(sabre/dav)) = 4.1.4
Provides: bundled(php-composer(sabre/event)) = 5.1.2
Provides: bundled(php-composer(sabre/http)) = 5.1.1
Provides: bundled(php-composer(sabre/uri)) = 2.2.1
Provides: bundled(php-composer(sabre/vobject)) = 4.3.3
Provides: bundled(php-composer(sabre/xml)) = 2.2.3
Provides: bundled(php-composer(scssphp/scssphp)) = 1.4.1
Provides: bundled(php-composer(spomky-labs/base64url)) = 2.0.4
Provides: bundled(php-composer(spomky-labs/cbor-php)) = 2.0.1
Provides: bundled(php-composer(stecman/symfony-console-completion)) = 0.11.0
Provides: bundled(php-composer(swiftmailer/swiftmailer)) = 6.2.5
Provides: bundled(php-composer(symfony/console)) = 4.4.19
Provides: bundled(php-composer(symfony/event-dispatcher)) = 4.4.19
Provides: bundled(php-composer(symfony/event-dispatcher-contracts)) = 1.1.9
Provides: bundled(php-composer(symfony/polyfill-ctype)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-iconv)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-intl-grapheme)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-intl-idn)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-intl-normalizer)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-mbstring)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-php72)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-php73)) = 1.22.0
Provides: bundled(php-composer(symfony/polyfill-php80)) = 1.22.0
Provides: bundled(php-composer(symfony/process)) = 4.4.19
Provides: bundled(php-composer(symfony/routing)) = 4.4.19
Provides: bundled(php-composer(symfony/service-contracts)) = 2.2.0
Provides: bundled(php-composer(symfony/translation)) = 4.4.19
Provides: bundled(php-composer(symfony/translation-contracts)) = 2.3.0
Provides: bundled(php-composer(thecodingmachine/safe)) = 1.3.3
Provides: bundled(php-composer(web-auth/cose-lib)) = 3.3.1
Provides: bundled(php-composer(web-auth/metadata-service)) = 3.3.1
Provides: bundled(php-composer(web-auth/webauthn-lib)) = 3.3.1

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
Requires:       php

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

# find all remaining using "find -name '*LICENCE*' -name '*LICENSE*' -o -name '*COPYING*' | sort"
mv 3rdparty/aws/aws-sdk-php/LICENSE.md aws-LICENSE.md
mv 3rdparty/bantu/ini-get-wrapper/LICENSE bantu-LICENSE
mv 3rdparty/beberlei/assert/LICENSE beberlei-LICENSE
mv 3rdparty/brick/math/LICENSE brick-LICENSE
mv 3rdparty/christophwurst/id3parser/LICENSE christophwurst-LICENSE
mv 3rdparty/composer/package-versions-deprecated/LICENSE composer-LICENSE
mv 3rdparty/deepdiver1975/tarstreamer/LICENSE deepdiver1975-LICENSE
mv 3rdparty/deepdiver/zipstreamer/COPYING deepdiver-COPYING
mv 3rdparty/doctrine/cache/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/dbal/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/event-manager/LICENSE doctrine-LICENSE
mv 3rdparty/egulias/email-validator/LICENSE egulias-LICENSE
mv 3rdparty/fgrosse/phpasn1/LICENSE fgrosse-LICENSE
mv 3rdparty/giggsey/libphonenumber-for-php/LICENSE giggsey-LICENSE
mv 3rdparty/giggsey/locale/LICENSE giggsey-LICENSE
mv 3rdparty/guzzlehttp/guzzle/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/promises/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/psr7/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/uri-template/LICENSE.md guzzlehttp-LICENSE
mv 3rdparty/icewind/searchdav/LICENSE icewind-LICENSE
mv 3rdparty/justinrainbow/json-schema/LICENSE justinrainbow-LICENSE
mv 3rdparty/league/flysystem/LICENSE league-LICENSE
mv 3rdparty/league/mime-type-detection/LICENSE league-LICENSE
mv 3rdparty/league/uri-interfaces/LICENSE league-LICENSE
mv 3rdparty/league/uri/LICENSE league-LICENSE
mv '3rdparty/LICENSE INFO' 3rdparty-LICENSE_INFO
mv 3rdparty/microsoft/azure-storage-blob/LICENSE microsoft-LICENSE
mv 3rdparty/microsoft/azure-storage-common/LICENSE microsoft-LICENSE
mv 3rdparty/mtdowling/jmespath.php/LICENSE mtdowling-LICENSE
mv 3rdparty/nextcloud/lognormalizer/COPYING lognormalizer-LICENSE
mv 3rdparty/nikic/php-parser/LICENSE nikic-LICENSE
mv 3rdparty/opis/closure/LICENSE opis-LICENSE
mv 3rdparty/patchwork/jsqueeze/LICENSE.ASL20 patchwork-LICENSE-APACHE
mv 3rdparty/patchwork/jsqueeze/LICENSE.GPLv2 patchwork-LICENSE-GPL
mv 3rdparty/pear/console_getopt/LICENSE pear-LICENSE
mv 3rdparty/pear/pear_exception/LICENSE pear-LICENSE
mv 3rdparty/php-ds/php-ds/LICENSE php-ds-LICENSE
mv 3rdparty/php-http/guzzle7-adapter/LICENSE php-http-LICENSE
mv 3rdparty/php-http/httplug/LICENSE php-http-LICENSE
mv 3rdparty/php-http/promise/LICENSE php-http-LICENSE
mv 3rdparty/php-opencloud/openstack/LICENSE php-opencloud-LICENSE
mv 3rdparty/phpseclib/phpseclib/LICENSE phpseclib-LICENSE
mv 3rdparty/psr/container/LICENSE psr-LICENSE
mv 3rdparty/psr/http-client/LICENSE psr-LICENSE
mv 3rdparty/psr/http-factory/LICENSE psr-LICENSE
mv 3rdparty/psr/http-message/LICENSE psr-LICENSE
mv 3rdparty/psr/log/LICENSE psr-LICENSE
mv 3rdparty/punic/punic/LICENSE.txt punic-LICENSE.txt
mv 3rdparty/punic/punic/UNICODE-LICENSE.txt punic-UNICODE-LICENSE
mv 3rdparty/ralouphie/getallheaders/LICENSE ralouphie-LICENSE
mv 3rdparty/ramsey/collection/LICENSE ramsey-LICENSE
mv 3rdparty/ramsey/uuid/LICENSE ramsey-LICENSE
mv 3rdparty/sabre/dav/lib/DAV/Browser/assets/openiconic/ICON-LICENSE sabre-ICON-LICENSE
mv 3rdparty/sabre/dav/LICENSE sabre-LICENSE
mv 3rdparty/sabre/event/LICENSE sabre-LICENSE
mv 3rdparty/sabre/http/LICENSE sabre-LICENSE
mv 3rdparty/sabre/uri/LICENSE sabre-LICENSE
mv 3rdparty/sabre/vobject/LICENSE sabre-LICENSE
mv 3rdparty/sabre/xml/LICENSE sabre-LICENSE
mv 3rdparty/scssphp/scssphp/LICENSE.md scssphp-LICENSE.md
mv 3rdparty/spomky-labs/base64url/LICENSE spomky-labs-LICENSE
mv 3rdparty/spomky-labs/cbor-php/LICENSE spomky-labs-LICENSE
mv 3rdparty/stecman/symfony-console-completion/LICENCE stecman-LICENSE
mv 3rdparty/symfony/console/LICENSE symfony-LICENSE
mv 3rdparty/symfony/event-dispatcher-contracts/LICENSE symfony-LICENSE
mv 3rdparty/symfony/event-dispatcher/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-ctype/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-iconv/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-intl-grapheme/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-intl-idn/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-intl-normalizer/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-mbstring/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php72/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php73/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php80/LICENSE symfony-LICENSE
mv 3rdparty/symfony/process/LICENSE symfony-LICENSE
mv 3rdparty/symfony/routing/LICENSE symfony-LICENSE
mv 3rdparty/symfony/service-contracts/LICENSE symfony-LICENSE
mv 3rdparty/symfony/translation-contracts/LICENSE symfony-LICENSE
mv 3rdparty/symfony/translation/LICENSE symfony-LICENSE
mv 3rdparty/thecodingmachine/safe/LICENSE thecodingmachine-LICENSE
mv 3rdparty/web-auth/cose-lib/LICENSE web-auth-LICENSE
mv 3rdparty/web-auth/metadata-service/LICENSE web-auth-LICENSE
mv 3rdparty/web-auth/webauthn-lib/LICENSE web-auth-LICENSE
mv apps/cloud_federation_api/LICENSE cloud_federation_api-LICENSE
mv apps/files_external/3rdparty/icewind/smb/LICENSE.txt icewind-LICENSE
mv apps/files_external/3rdparty/icewind/streams/LICENCE icewind-LICENSE
mv apps/files_pdfviewer/js/pdfjs/LICENSE js-pdfjs-LICENSE
mv apps/files_pdfviewer/js/pdfjs/web/cmaps/LICENSE js-pdfjs-cmaps-LICENSE
mv apps/files_rightclick/COPYING files_rightclick-COPYING
mv apps/files_rightclick/LICENSE files_rightclick-LICENSE
mv apps/nextcloud_announcements/COPYING nextcloud_announcements-COPYING
mv apps/notifications/COPYING notifications-LICENSE
mv apps/password_policy/LICENSE password_policy-LICENSE
mv apps/photos/COPYING photos-COPYING
mv apps/privacy/COPYING privacy-COPYING
mv apps/recommendations/LICENSE recommendations-LICENSE
mv apps/serverinfo/COPYING serverinfo-LICENSE
mv apps/survey_client/COPYING survey_client-LICENSE
mv apps/text/COPYING text-COPYING
mv apps/theming/js/3rdparty/jscolor/LICENSE.txt jscolor-LICENSE
mv apps/user_ldap/vendor/ui-multiselect/MIT-LICENSE js-jqueryui-multiselect-LICENSE
mv apps/viewer/COPYING viewer-COPYING
mv COPYING nextcloud-LICENSE
mv core/fonts/LICENSE_OFL.txt fonts-LICENSE
mv core/vendor/zxcvbn/LICENSE.txt zxcvbn-LICENSE

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
install -Dpm 644 %{SOURCE202} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf

# Install the systemd timer
install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/nextcloud-cron.service
install -Dpm 644 %{SOURCE3} %{buildroot}%{_unitdir}/nextcloud-cron.timer

%post httpd
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :

%postun httpd
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
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
* Wed Feb 24 2021 Christopher Engelhard <ce@lcts.de> - 21.0.0-2
- Drop dependency on php-imap. Fixes RHBZ #1933023

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

* Mon Oct 26 2020 Christopher Engelhard <ce@lcts.de> - 20.0.1-1
- Update to Nextcloud 20.0.1

* Sun Oct 11 2020 Christopher Engelhard <ce@lcts.de> - 20.0.0-1
- Update to Nextcloud 20.0.0

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
