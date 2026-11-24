
# NextPYP Client

A Python client for the NextPYP website.

The NextPYP Python Client allows you to connect to and exchange data with the NextPYP website using the very
same APIs that NextPYP uses internally. These APIs allow accessing every function of the website available
to browser clients, including listening to real-time updates from the server.


## Install

```shell
pip install nextpyp-client
```

Then see [Getting Started](https://nextpyp.app/nextpyp-client) to request an app token and make your first calls.


## Versions

The client's version matches the NextPYP API version it speaks: client `2.2.x` works with NextPYP websites
whose API is `2.2` or newer, up to the next major version. `Client.is_compatible()` checks a website for you.


## Documentation

The newest version of the documentation is available online at:

https://nextpyp.app/nextpyp-client

Documentation sources are available in the `doc/src` folder.

You can build the documentation with the command:
```shell
tox run -e doc
```
Then the full HTML documentation will appear at `doc/build/html/index.html`

Building the documentation requires the [tox](https://tox.wiki) tool.
