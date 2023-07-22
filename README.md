# WebDAV Server Comparison

I've ran the [Litmus](http://www.webdav.org/neon/litmus/) test suite against various WebDAV servers to test their compliancy to the spec. Here are the results:

|  | Apache | Nginx | Nginx w/ nginx-dav-ext-module | Sabre/dav | Sabre/dav w/ FSExt | Lighttpd | Chezdav | Rclone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **basic** |  |  |  |  |  |  |  |  |
| init | pass | pass | pass | pass | pass | pass | pass | pass |
| begin | pass | pass | pass | pass | pass | pass | pass | pass |
| options | pass | [FAIL](results/nginx.txt#L4 "(OPTIONS on base collection `/litmus/': 405 Not Allowed)") | pass | pass | pass | pass | pass | pass |
| put_get | pass | pass | pass | pass | pass | pass | pass | pass |
| put_get_utf8_segment | pass | pass | pass | pass | pass | pass | pass | pass |
| put_no_parent | pass | pass | pass | pass | pass | pass | pass | pass |
| mkcol_over_plain | pass | pass | pass | pass | pass | pass | pass | pass |
| delete | pass | pass | pass | pass | pass | pass | pass | pass |
| delete_null | pass | pass | pass | pass | pass | pass | pass | pass |
| delete_fragment | pass | [WARNING](results/nginx.txt#L11 "DELETE removed collection resource with Request-URI including fragment; unsafe") | [WARNING](results/nginx-dav-ext-module.txt#L11 "DELETE removed collection resource with Request-URI including fragment; unsafe") | pass | pass | pass | pass | pass |
| mkcol | pass | pass | pass | pass | pass | pass | pass | pass |
| mkcol_again | pass | pass | pass | pass | pass | pass | pass | [FAIL](results/rclone.txt#L13 "(MKCOL on existing collection should fail (RFC2518:8.3.1))") |
| delete_coll | pass | pass | pass | pass | pass | pass | pass | pass |
| mkcol_no_parent | pass | pass | pass | pass | pass | pass | pass | pass |
| mkcol_with_body | pass | pass | pass | pass | pass | pass | pass | pass |
| finish | pass | pass | pass | pass | pass | pass | pass | pass |
| **copymove** |  |  |  |  |  |  |  |  |
| init | pass | pass | pass | pass | pass | pass | pass | pass |
| begin | pass | pass | pass | pass | pass | pass | pass | pass |
| copy_init | pass | pass | pass | pass | pass | pass | pass | pass |
| copy_simple | pass | [WARNING](results/nginx.txt#L25 "COPY to new resource should give 201 (RFC2518:S8.8.5)") | [WARNING](results/nginx-dav-ext-module.txt#L25 "COPY to new resource should give 201 (RFC2518:S8.8.5)") | pass | pass | pass | pass | pass |
| copy_overwrite | pass | [FAIL](results/nginx.txt#L27 "(COPY overwrites collection: 409 Conflict)") | [FAIL](results/nginx-dav-ext-module.txt#L27 "(COPY overwrites collection: 409 Conflict)") | pass | pass | pass | pass | pass |
| copy_nodestcoll | pass | [WARNING](results/nginx.txt#L28 "COPY to non-existant collection '/litmus/nonesuch' gave '500 Internal Server Error' not 409 (RFC2518:S8.8.5)") | [WARNING](results/nginx-dav-ext-module.txt#L28 "COPY to non-existant collection '/litmus/nonesuch' gave '500 Internal Server Error' not 409 (RFC2518:S8.8.5)") | pass | pass | pass | pass | pass |
| copy_cleanup | pass | pass | pass | pass | pass | pass | pass | pass |
| copy_coll | pass | pass | pass | pass | pass | pass | pass | pass |
| copy_shallow | pass | pass | pass | pass | pass | pass | pass | pass |
| move | pass | [WARNING](results/nginx.txt#L33 "MOVE to new resource didn't give 201") | [WARNING](results/nginx-dav-ext-module.txt#L33 "MOVE to new resource didn't give 201") | pass | pass | pass | pass | pass |
| move_coll | pass | [FAIL](results/nginx.txt#L35 "(MOVE collection `/litmus/mvdest2/' over non-collection `/litmus/mvnoncoll' with overwrite: 409 Conflict)") | [FAIL](results/nginx-dav-ext-module.txt#L35 "(MOVE collection `/litmus/mvdest2/' over non-collection `/litmus/mvnoncoll' with overwrite: 409 Conflict)") | pass | pass | pass | pass | pass |
| move_cleanup | pass | pass | pass | pass | pass | pass | pass | pass |
| finish | pass | pass | pass | pass | pass | pass | pass | pass |
| **props** |  |  |  |  |  |  |  |  |
| init | pass | pass | pass | pass | pass | pass | pass | pass |
| begin | pass | pass | pass | pass | pass | pass | pass | pass |
| propfind_invalid | pass | [FAIL](results/nginx.txt#L43 "(PROPFIND with non-well-formed XML request body got 405 response not 400)") | pass | pass | pass | [FAIL](results/lighttpd.txt#L37 "(PROPFIND with non-well-formed XML request body got 415 response not 400)") | pass | pass |
| propfind_invalid2 | pass | [FAIL](results/nginx.txt#L44 "(PROPFIND with invalid namespace declaration in body (see FAQ) got 405 response not 400)") | [FAIL](results/nginx-dav-ext-module.txt#L44 "(PROPFIND with invalid namespace declaration in body (see FAQ) got 207 response not 400)") | pass | pass | [FAIL](results/lighttpd.txt#L38 "(PROPFIND with invalid namespace declaration in body (see FAQ) got 415 response not 400)") | pass | [FAIL](results/rclone.txt#L38 "(PROPFIND with invalid namespace declaration in body (see FAQ) got 207 response not 400)") |
| propfind_d0 | pass | [FAIL](results/nginx.txt#L45 "(No responses returned)") | pass | pass | pass | pass | pass | pass |
| propinit | pass | pass | pass | pass | pass | pass | pass | pass |
| propset | pass | [FAIL](results/nginx.txt#L47 "(PROPPATCH on `/litmus/prop': 405 Not Allowed)") | [FAIL](results/nginx-dav-ext-module.txt#L47 "(PROPPATCH on `/litmus/prop': 405 Not Allowed)") | [FAIL](results/sabredav.txt#L41 "(PROPPATCH on `/litmus/prop': http://localhost:8002/litmus/prop: 403 Forbidden") | pass | pass | pass | [FAIL](results/rclone.txt#L41 "(PROPPATCH on `/litmus/prop': http://localhost:8080/litmus/prop: 403 Forbidden") |
| propget | pass | [FAIL](results/nginx.txt#L68 "(PROPFIND on `/litmus/prop': 405 Not Allowed)") | [FAIL](results/nginx-dav-ext-module.txt#L68 "(No value given for property {http://example.com/kappa}somename)") | [FAIL](results/sabredav.txt#L64 "(No value given for property {http://example.com/kappa}somename)") | pass | pass | pass | [FAIL](results/rclone.txt#L64 "(No value given for property {http://example.com/kappa}somename)") |
| propextended | pass | pass | pass | pass | pass | pass | pass | pass |
| propmove | pass | SKIPPED | SKIPPED | SKIPPED | pass | pass | pass | SKIPPED |
| propdeletes | pass | SKIPPED | SKIPPED | SKIPPED | pass | pass | pass | SKIPPED |
| propreplace | pass | SKIPPED | SKIPPED | SKIPPED | pass | pass | pass | SKIPPED |
| propnullns | pass | SKIPPED | SKIPPED | SKIPPED | pass | [FAIL](results/lighttpd.txt#L50 "(PROPPATCH of property with null namespace (see FAQ))") | pass | SKIPPED |
| prophighunicode | pass | SKIPPED | SKIPPED | SKIPPED | pass | [FAIL](results/lighttpd.txt#L52 "(PROPPATCH of property with high unicode value)") | pass | SKIPPED |
| propremoveset | pass | SKIPPED | SKIPPED | SKIPPED | pass | [FAIL](results/lighttpd.txt#L54 "(PROPPATCH remove then set)") | pass | SKIPPED |
| propsetremove | pass | SKIPPED | SKIPPED | SKIPPED | pass | [FAIL](results/lighttpd.txt#L56 "(PROPPATCH remove then set)") | pass | SKIPPED |
| propvalnspace | pass | SKIPPED | SKIPPED | SKIPPED | pass | [FAIL](results/lighttpd.txt#L58 "(PROPPATCH of property with value defining namespace)") | pass | SKIPPED |
| propwformed | pass | pass | pass | pass | pass | pass | pass | pass |
| propmanyns | pass | [FAIL](results/nginx.txt#L67 "(PROPPATCH on `/litmus/prop': 405 Not Allowed)") | [FAIL](results/nginx-dav-ext-module.txt#L67 "(PROPPATCH on `/litmus/prop': 405 Not Allowed)") | [FAIL](results/sabredav.txt#L62 "(PROPPATCH on `/litmus/prop': http://localhost:8002/litmus/prop: 403 Forbidden") | pass | pass | pass | [FAIL](results/rclone.txt#L62 "(PROPPATCH on `/litmus/prop': http://localhost:8080/litmus/prop: 403 Forbidden") |
| propcleanup | pass | pass | pass | pass | pass | pass | pass | pass |
| finish | pass | pass | pass | pass | pass | pass | pass | pass |
| **locks** |  |  |  |  |  |  |  |  |
| init | pass | pass | pass | pass | pass | pass | pass | pass |
| begin | pass | pass | pass | pass | pass | pass | pass | pass |
| options | pass | [FAIL](results/nginx.txt#L76 "(OPTIONS on base collection `/litmus/': 405 Not Allowed)") | pass | pass | pass | pass | pass | pass |
| precond | pass | [SKIPPED](results/nginx.txt#L77 "(locking tests skipped,") | pass | pass | pass | pass | pass | pass |
| init_locks | pass |  | pass | pass | pass | pass | pass | pass |
| put | pass |  | pass | pass | pass | pass | pass | pass |
| lock_excl | pass |  | pass | pass | pass | pass | pass | pass |
| discover | pass |  | [FAIL](results/nginx-dav-ext-module.txt#L81 "(compare discovered lock: owner was NULL, expected 'litmus test suite')") | pass | pass | pass | pass | pass |
| refresh | pass |  | pass | pass | pass | pass | pass | pass |
| notowner_modify | pass |  | [WARNING](results/nginx-dav-ext-module.txt#L111 "PROPPATCH failed with 405 not 423") | pass | pass | pass | pass | pass |
| notowner_lock | pass |  | SKIPPED | pass | pass | pass | pass | SKIPPED |
| owner_modify | pass |  | [FAIL](results/nginx-dav-ext-module.txt#L110 "(PROPPATCH on locked resouce on `/litmus/lockcoll/lockme.txt': 405 Not Allowed)") | [FAIL](results/sabredav.txt#L105 "(PROPPATCH on locked resouce on `/litmus/lockcoll/lockme.txt': http://localhost:8002/litmus/lockcoll/lockme.txt: 403 Forbidden") | pass | pass | pass | [FAIL](results/rclone.txt#L105 "(PROPPATCH on locked resouce on `/litmus/lockcoll/lockme.txt': http://localhost:8080/litmus/lockcoll/lockme.txt: 403 Forbidden") |
| copy | pass |  | pass | pass | pass | pass | pass | pass |
| cond_put | pass |  | pass | SKIPPED | pass | pass | pass | pass |
| fail_cond_put | pass |  | [WARNING](results/nginx-dav-ext-module.txt#L92 "PUT failed with 423 not 412") | SKIPPED | pass | pass | pass | pass |
| cond_put_with_not | pass |  | pass | pass | pass | pass | pass | pass |
| cond_put_corrupt_token | [WARNING](results/apache.txt#L85 "PUT failed with 400 not 423") |  | pass | pass | pass | pass | pass | [WARNING](results/rclone.txt#L89 "PUT failed with 412 not 423") |
| complex_cond_put | pass |  | pass | SKIPPED | pass | pass | pass | pass |
| fail_complex_cond_put | pass |  | [FAIL](results/nginx-dav-ext-module.txt#L97 "(PUT with complex bogus conditional should fail with 412: 204 No Content)") | SKIPPED | pass | pass | pass | [FAIL](results/rclone.txt#L92 "(PUT with complex bogus conditional should fail with 412: 201 Created)") |
| unlock | pass |  | pass | pass | pass | pass | pass | pass |
| fail_cond_put_unlocked | pass |  | [FAIL](results/nginx-dav-ext-module.txt#L99 "(conditional PUT with invalid lock-token should fail: 204 No Content)") | pass | pass | pass | pass | pass |
| lock_shared | pass |  | [FAIL](results/nginx-dav-ext-module.txt#L100 "(requested lockscope not satisfied!  got shared, wanted exclusive)") | pass | pass | pass | pass | [FAIL](results/rclone.txt#L95 "(LOCK on `/litmus/lockme': 501 Not Implemented)") |
| double_sharedlock | pass |  | SKIPPED | pass | pass | pass | pass | SKIPPED |
| prep_collection | pass |  | pass | pass | pass | pass | pass | pass |
| lock_collection | pass |  | pass | pass | pass | pass | pass | pass |
| indirect_refresh | pass |  | pass | pass | pass | pass | pass | pass |
| unmapped_lock | [WARNING](results/apache.txt#L106 "LOCK on unmapped url returned 200 not 201 (RFC4918:S7.3)") |  | pass | pass | pass | pass | pass | pass |
| finish | pass |  | pass | pass | pass | pass | pass | pass |
| **http** |  |  |  |  |  |  |  |  |
| init | pass | pass | pass | pass | pass | pass | pass | pass |
| begin | pass | pass | pass | pass | pass | pass | pass | pass |
| expect100 | pass | pass | pass | pass | pass | pass | pass | pass |
| finish | pass | pass | pass | pass | pass | pass | pass | pass |

Some notes:

* Candidates with a lot of SKIPPEDs in the props section don't support custom properties. Custom properties are per-file key-value pairs that are stored in a database separate from the file system. Sabre/dav optionally supports custom properties through the `FSExt\Directory` class (see below).
* Tests with `cond` in their name mostly test the [`If` header](http://www.webdav.org/specs/rfc2518.html#HEADER_If). The `If` header is WebDAV's generalized version of HTTP's [`If-Match`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match) and [`If-None-Match`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-None-Match) headers. The `If-Match` and `If-None-Match` headers are strictly speaking not part of the WebDAV standard and thus not tested by Litmus but they can always be rewritten in terms of the more powerful `If` header.
* Nginx's built-in WebDAV implementation is quite poor and lacks basic methods such as `PROPFIND`, `OPTIONS` and `LOCK`. This is somewhat alleviated by using the [nginx-dav-ext-module](https://github.com/arut/nginx-dav-ext-module) but even with the module Nginx compares poorly to other implementations. Nevertheless, Nginx might be sufficient for your needs.

## Tested versions

All tests use [Litmus](http://www.webdav.org/neon/litmus/) version 0.13. The versions tested are generally those available on Debian 12 (bookworm).

* [Apache HTTP Server](https://httpd.apache.org/) version 2.4.57
* [Nginx](https://nginx.org/) version 1.22.1 with [nginx-dav-ext-module](https://github.com/arut/nginx-dav-ext-module) version 3.0.0
* [Sabre/dav](https://sabre.io/) version 1.8.12 running on Apache
* [Lighttpd](https://www.lighttpd.net/) version 1.4.69
* [Chezdav aka phởdav](https://wiki.gnome.org/phodav) version 3.0
* [Rclone](https://rclone.org/) version 1.60.1

## Saving results

Litmus writes a carriage return (`\r`) to stdout to overwrite the current line. This works in a terminal but leads to duplicate content when writing to a file. We can strip out anything that came before the carriage return with sed:

```
litmus -k http://localhost:8080 | sed 's/.*\r//' > results/rclone.txt
```

## Apache configuration

Apache requires the `dav` and `dav_fs` modules for WebDAV support. On Debian-based systems these can be enabled using the `a2enmod` command. I've used the following virtual host config for the test:

```apacheconf
DavLockDB /usr/local/apache2/var/DavLock
Listen 8001
<VirtualHost *:8001>
    DocumentRoot /var/www/webdav
    <Directory /var/www/webdav>
        DAV On
    </Directory>
</VirtualHost>
```

## Nginx configuration

I've used the following site config to test Nginx without the nginx-dav-ext-module:

```nginx
server {
    listen 80;
    root /var/www/webdav;
    dav_methods PUT DELETE MKCOL COPY MOVE;
}
```

The nginx-dav-ext-module needs to be installed before it can be used within Nginx. On Debian it can be installed via the `libnginx-mod-http-dav-ext` package. I've used the following site config to test Nginx with the nginx-dav-ext-module:

```nginx
dav_ext_lock_zone zone=foo:10m;
server {
    listen 80;
    root /var/www/webdav;
    dav_methods PUT DELETE MKCOL COPY MOVE;
    dav_ext_methods PROPFIND OPTIONS LOCK UNLOCK;
    dav_ext_lock zone=foo;

    # nginx-dav-ext-module only sets the class 2 flag instead of setting
    # both class 1 and class 2 flags as required by the standard.
    # This is a workaround until https://github.com/arut/nginx-dav-ext-module/pull/46 is merged.
    add_header DAV 1,2;
}
```

## Sabre/dav configuration

I mostly followed the [official guide](https://sabre.io/dav/gettingstarted/) to get started but instead of installing sabre/dav via composer I installed the Debian package `php-sabre-dav`. The Debian package is still on version 1.8.12 from 2015.

I've used the following virtual host config for Apache:

```apacheconf
Listen 8002
<VirtualHost *:8002>
    # Copied from https://sabre.io/dav/webservers/

    # The DocumentRoot is also required
    DocumentRoot /var/www/sabredav

    RewriteEngine On
    # This makes every request go to server.php
    RewriteRule ^/(.*)$ /server.php [L]

    # Output buffering needs to be off, to prevent high memory usage
    php_flag output_buffering off

    # This is also to prevent high memory usage
    php_flag always_populate_raw_post_data off

    # This is almost a given, but magic quotes is *still* on on some
    # linux distributions
    php_flag magic_quotes_gpc off

    # SabreDAV is not compatible with mbstring function overloading
    php_flag mbstring.func_overload off

</VirtualHost>
```

And the following `server.php`:

```php
<?php

// Copied from https://sabre.io/dav/gettingstarted/

use
    Sabre\DAV;

// The autoloader
require 'Sabre/autoload.php';

// Now we're creating a whole bunch of objects
$rootDirectory = new DAV\FS\Directory('public');

// The server object is responsible for making sense out of the WebDAV protocol
$server = new DAV\Server($rootDirectory);

// If your server is not on your webroot, make sure the following line has the
// correct information
$server->setBaseUri('/');

// The lock manager is reponsible for making sure users don't overwrite
// each others changes.
$lockBackend = new DAV\Locks\Backend\File('data/locks');
$lockPlugin = new DAV\Locks\Plugin($lockBackend);
$server->addPlugin($lockPlugin);

// This ensures that we get a pretty index in the browser, but it is
// optional.
$server->addPlugin(new DAV\Browser\Plugin());

// All we need to do now, is to fire up the server
$server->exec();
```

To enable support for custom properties the line in `server.php` using `FS\Directory` needs to be changed to use the `FSExt\Directory` class:

```php
$rootDirectory = new DAV\FSExt\Directory('public');
```

## Lighttpd configuration

Lighttpd requires the `webdav` module for WebDAV support which I've enabled using the `lighty-enable-mod` command. Additionally I've added the following config to `lighttpd.conf`:

```
webdav.activate = "enable"
```
