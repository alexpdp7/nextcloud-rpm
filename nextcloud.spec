Name:           nextcloud
Version:        20.0.0
Release:        1%{?dist}
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

BuildArch:      noarch

# For the systemd macros
%{?systemd_requires}
BuildRequires:  systemd

# expand pear macros on install
BuildRequires:  php-pear

# For sanity %%check
BuildRequires:       php-cli


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
Requires:       php-mysqlnd
Requires:       php-pgsql
Requires:       php-ldap
Requires:       php-smbclient
Requires:       php-imap
Requires:       php-gmp
Requires:       php-pecl-imagick
Requires:       php-pecl-memcached
Requires:       php-pecl-apcu
Requires:       php-pecl-redis5


# Need to label the httpd rw stuff correctly until base selinux policy updated
Requires(post):   %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

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
Requires:   php-mysqlnd

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

# Locate license files and put them sensibly in place
# find all using "find -name '*LICENSE*' -o -name '*COPYING*' | sort"
mv 3rdparty/aws/aws-sdk-php/LICENSE.md aws-LICENSE.md
mv 3rdparty/bantu/ini-get-wrapper/LICENSE bantu-LICENSE
mv 3rdparty/beberlei/assert/LICENSE beberlei-LICENSE
mv 3rdparty/christophwurst/id3parser/LICENSE christophwurst-LICENSE
mv 3rdparty/composer/LICENSE composer-LICENSE
mv 3rdparty/deepdiver1975/tarstreamer/LICENSE deepdiver1975-LICENSE
mv 3rdparty/deepdiver/zipstreamer/COPYING deepdiver-COPYING
mv 3rdparty/doctrine/annotations/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/cache/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/collections/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/common/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/dbal/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/event-manager/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/inflector/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/persistence/LICENSE doctrine-LICENSE
mv 3rdparty/doctrine/reflection/LICENSE doctrine-LICENSE
mv 3rdparty/egulias/email-validator/LICENSE egulias-LICENSE
mv 3rdparty/fgrosse/phpasn1/LICENSE fgrosse-LICENSE
mv 3rdparty/guzzlehttp/guzzle/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/promises/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/psr7/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/ringphp/LICENSE guzzlehttp-LICENSE
mv 3rdparty/guzzlehttp/streams/LICENSE guzzlehttp-LICENSE
mv 3rdparty/icewind/searchdav/LICENSE icewind-LICENSE
mv 3rdparty/interfasys/lognormalizer/COPYING interfasys-COPYING
mv 3rdparty/jeremeamia/SuperClosure/LICENSE.md jeremeamia-LICENSE
mv 3rdparty/justinrainbow/json-schema/LICENSE justinrainbow-LICENSE
mv 3rdparty/league/flysystem/LICENSE league-LICENSE
mv 3rdparty/league/uri-components/LICENSE league-LICENSE
mv 3rdparty/league/uri-interfaces/LICENSE league-LICENSE
mv 3rdparty/league/uri/LICENSE league-LICENSE
mv '3rdparty/LICENSE INFO' 3rdparty-LICENSE_INFO
mv 3rdparty/microsoft/azure-storage-blob/LICENSE microsoft-LICENSE
mv 3rdparty/microsoft/azure-storage-common/LICENSE microsoft-LICENSE
mv 3rdparty/mtdowling/jmespath.php/LICENSE mtdowling-LICENSE
mv 3rdparty/nikic/php-parser/LICENSE nikic-LICENSE
mv 3rdparty/paragonie/random_compat/LICENSE paragonie-LICENSE
mv 3rdparty/patchwork/jsqueeze/LICENSE.ASL20 patchwork-LICENSE-APACHE
mv 3rdparty/patchwork/jsqueeze/LICENSE.GPLv2 patchwork-LICENSE-GPL
mv 3rdparty/patchwork/utf8/LICENSE-APACHE patchwork-LICENSE-APACHE
mv 3rdparty/patchwork/utf8/LICENSE-GPL patchwork-LICENSE-GPL
mv 3rdparty/pear/console_getopt/LICENSE pear-LICENSE
mv 3rdparty/pear/pear_exception/LICENSE pear-LICENSE
mv 3rdparty/php-http/guzzle6-adapter/LICENSE php-http-LICENSE
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
mv 3rdparty/ramsey/uuid/LICENSE ramsey-LICENSE
mv 3rdparty/react/promise/LICENSE react-LICENSE
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
mv 3rdparty/symfony/polyfill-intl-idn/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-mbstring/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php56/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php72/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php73/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-php80/LICENSE symfony-LICENSE
mv 3rdparty/symfony/polyfill-util/LICENSE symfony-LICENSE
mv 3rdparty/symfony/process/LICENSE symfony-LICENSE
mv 3rdparty/symfony/routing/LICENSE symfony-LICENSE
mv 3rdparty/symfony/service-contracts/LICENSE symfony-LICENSE
mv 3rdparty/symfony/translation-contracts/LICENSE symfony-LICENSE
mv 3rdparty/symfony/translation/LICENSE symfony-LICENSE
mv 3rdparty/web-auth/cose-lib/LICENSE web-auth-LICENSE
mv 3rdparty/web-auth/metadata-service/LICENSE web-auth-LICENSE
mv 3rdparty/web-auth/webauthn-lib/LICENSE web-auth-LICENSE
mv apps/accessibility/composer/composer/LICENSE accessibility-LICENSE
mv apps/admin_audit/composer/composer/LICENSE admin_audit-LICENSE
mv apps/cloud_federation_api/composer/composer/LICENSE cloud_federation_api-LICENSE
mv apps/cloud_federation_api/LICENSE cloud_federation_api-LICENSE
mv apps/comments/composer/composer/LICENSE comments-LICENSE
mv apps/contactsinteraction/composer/composer/LICENSE contactsinteraction-LICENSE
mv apps/dav/composer/composer/LICENSE dav-LICENSE
mv apps/encryption/composer/composer/LICENSE encryption-LICENSE
mv apps/federatedfilesharing/composer/composer/LICENSE federatedfilesharing-LICENSE
mv apps/federation/composer/composer/LICENSE federation-LICENSE
mv apps/files/composer/composer/LICENSE files-LICENSE
mv apps/files_external/3rdparty/composer/LICENSE files_external-LICENSE
mv apps/files_external/3rdparty/icewind/smb/LICENSE.txt icewind-smb-LICENSE
mv apps/files_external/3rdparty/icewind/streams/LICENCE icewind-streams-LICENSE
mv apps/files_pdfviewer/js/pdfjs/LICENSE js-pdfjs-LICENSE
mv apps/files_pdfviewer/js/pdfjs/web/cmaps/LICENSE js-pdfjs-cmaps-LICENSE
mv apps/files_rightclick/COPYING files_rightclick-COPYING
mv apps/files_rightclick/LICENSE files_rightclick-LICENSE
mv apps/files_sharing/composer/composer/LICENSE files_sharing-LICENSE
mv apps/files_trashbin/composer/composer/LICENSE files_trashbin-LICENSE
mv apps/files_versions/composer/composer/LICENSE files_versions-LICENSE
mv apps/lookup_server_connector/composer/composer/LICENSE lookup_server_connector-LICENSE
mv apps/nextcloud_announcements/COPYING nextcloud_announcements-COPYING
mv apps/notifications/COPYING notifications-LICENSE
mv apps/oauth2/composer/composer/LICENSE oauth2-LICENSE
mv apps/password_policy/LICENSE password_policy-LICENSE
mv apps/photos/COPYING photos-COPYING
mv apps/privacy/COPYING privacy-COPYING
mv apps/provisioning_api/composer/composer/LICENSE provisioning_api-LICENSE
mv apps/recommendations/LICENSE recommendations-LICENSE
mv apps/serverinfo/COPYING serverinfo-LICENSE
mv apps/settings/composer/composer/LICENSE settings-LICENSE
mv apps/sharebymail/composer/composer/LICENSE sharebymail-LICENSE
mv apps/survey_client/COPYING survey_client-LICENSE
mv apps/systemtags/composer/composer/LICENSE systemtags-LICENSE
mv apps/text/COPYING text-COPYING
mv apps/theming/js/3rdparty/jscolor/LICENSE.txt jscolor-LICENSE
mv apps/twofactor_backupcodes/composer/composer/LICENSE twofactor_backupcodes-LICENSE
mv apps/updatenotification/composer/composer/LICENSE updatenotification-LICENSE
mv apps/user_ldap/composer/composer/LICENSE user_ldap-LICENSE
mv apps/user_ldap/vendor/ui-multiselect/MIT-LICENSE js-jqueryui-multiselect-LICENSE
mv apps/user_status/composer/composer/LICENSE user_status-LICENSE
mv apps/viewer/COPYING viewer-COPYING
mv apps/workflowengine/composer/composer/LICENSE workflowengine-LICENSE
mv COPYING nextcloud-LICENSE
mv core/fonts/LICENSE_OFL.txt fonts-LICENSE
mv core/vendor/zxcvbn/LICENSE.txt zxcvbn-LICENSE
mv lib/composer/composer/LICENSE composer-LICENSE


%check
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

for f in {*.php,*.html,occ,robots.txt}; do
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
touch '%{_sysconfdir}/%{name}/CAN_INSTALL'
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
