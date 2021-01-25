# Django Response Compression

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/laactech/django-require-login/blob/master/LICENSE.md)

Combined Brotli and GZip compression for Django HTTP responses

This middleware copies Django's GZipMiddleware but adds Brotli compression. Brotli is
[supported](https://caniuse.com/?search=brotli) by most major browsers. If the request does not allow Brotli encoding,
the middleware falls back to Django's GZipMiddleware. Read Django's GZipMiddleware
[documentation](https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.gzip) to understand how
this middleware works and heed the warnings.

## Supported Versions

* Python 3.6, 3.7, 3.8, 3.9
* Django 2.2, 3.0, 3.1

## Installation and Setup

Install via pip.

```sh
pip install django-response-compression
```

Add the `ResponseCompressionMiddleware` to your Django middleware:

```python
MIDDLEWARE = [
    # ...
    'response_compression.middleware.ResponseCompressionMiddleware',
    # ...
]
```

Remove Django's GZipMiddleware if you added it.

**Read the GZipMiddleware [documentation](https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.gzip)
for notes about middleware ordering**

If you want to compress specific responses, use the decorator on your views.

```python
from response_compression.decorators import compress_response


@compress_response
def my_view(request):
    ...
```

Both the middleware and decorator are compatible with Django REST Framework responses.

The default brotli compression level is 4, and you can customize the brotli compression level by adding this to
django's settings:

```python
RESPONSE_COMPRESSION_BROTLI_LEVEL = 5
```


## Security

If you believe you've found a bug with security implications, please do not disclose this
issue in a public forum.

Email us at [support@laac.dev](mailto:support@laac.dev)

## Contribute

See [CONTRIBUTING.md](https://github.com/laactech/django-response-compression/blob/master/CONTRIBUTING.md)
