# Packaging Notes

Nextcloud has a fairly quick release cadence. Luckily they follow a strick system of alph-beta-rc-final releases and differences between major versions aren't huge so this rarely causes problems.
## Versions/Branches/Modules/Releases
### Upstream versioning
Upstream uses semantic versioning `major.minor.bugfix` for their version numbers. Contrary to what one might expect, they generally only push releases to their `stable` release channel after the first bugfix release `x.y.1`.
### In Fedora
`rawhide` generally contains whatever the latest non-rc release upstream is, including the `x.y.0` initial releases of a new major version.
Fedora releases stay on whatever major version they inherited from `rawhide` at branching as much as possible. Since nextcloud's and Fedora's release schedule don't entirely sync up, this means that occasionally a Fedora release might ship a `x.y.0` or EOL'd version of nextcloud for a brief time, but this is the best tradeoff between keeping Fedora in sync with upstream and minimizing disruptions within one Fedora release. Users who are unhappy with that can choose modules to work around that.
Module streams `nextcloud-X` ship the current release of major version `X`. Module stream `nextcloud-stable` should be rebased to a new major version only after the `x.y.1` bugfix release, in keeping with what upstream considers it's stable branch.
### Security fixes
Upstream is very conscientious with publishing and fixing CVEs discovered in their code. They generally backport fixes to all but very minor vulnerabilities to all supported versions, so it is generally safe not to change major versions within one Fedora release, even if a vulnerability has been discovered. Impacted users can always choose to upgrade via modules.
## Tarballs
Release tarballs are located at https://download.nextcloud.com/server/releases while prerelease tarballs are located ata https://download.nextcloud.com/server/prereleases/ . It generally takes about a day after the release annoucement for tarballs to actually appear in those directories.
## Bundled dependencies
Nextcloud ships a lot of bundled composer libraries, but these are easy to unbundle. The repos `utils` directory contains a script `get-composer-requires.py` that will output all required libraries/versions as well as if they're already available in the Fedora repositories or need to be added, by scanning the `composer.json` files shipped with the nextcloud sources.
