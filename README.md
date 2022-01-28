# Fedora Package

This repo contains a collection of RPM specs for some packages I maintain or use.

* `copr/` - RPM specs for packages I maintain on Copr: https://copr.fedorainfracloud.org/coprs/chenxiaolong/
* `not-uploaded/` - RPM specs for packages I use, but don't intend to upload to any public repo

## Building

1. Download the sources

    ```bash
    spectool -g <package>.spec
    ```

2. Build the SRPM

    ```bash
    mock --resultdir results-srpm --buildsrpm --spec <package>.spec --sources .
    ```

3. Build the RPMs

    ```bash
    mock --resultdir results-rpm --rebuild results-srpm/<package>-<version>-<release>.src.rpm
    ```

    `sbctl`, in particular, will also need `--enable-network`.

## Licenses

The packaging files are licensed under the same terms as the software being packaged. Please see the individual `.spec` files for the license.
