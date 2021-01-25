from django.middleware.gzip import GZipMiddleware
from django.utils.cache import patch_vary_headers
from django.utils.regex_helper import _lazy_re_compile

from .compress import brotli_compress, brotli_compress_stream

re_accepts_brotli = _lazy_re_compile(r"\bbr\b")


class ResponseCompressionMiddleware:
    """
    Almost direct copy of Django's GZipMiddleware. If the request accepts brotli encoding, the response is compressed
    with brotli. If not, we use Django's GZipMiddleware which compresses the response with gzip if the request accepts
    it.
    """
    def process_response(self, request, response):
        # It's not worth attempting to compress really short responses.
        if not response.streaming and len(response.content) < 200:
            return response

        # Avoid compressing if we've already got a content-encoding.
        if response.has_header("Content-Encoding"):
            return response

        patch_vary_headers(response, ("Accept-Encoding",))

        accept_encoding = request.META.get("HTTP_ACCEPT_ENCODING", "")
        if not re_accepts_brotli.search(accept_encoding):
            gzip_middleware = GZipMiddleware()
            return gzip_middleware.process_response(request, response)

        if response.streaming:
            # Delete the `Content-Length` header for streaming content, because
            # we won't know the compressed size until we stream it.
            response.streaming_content = brotli_compress_stream(response.streaming_content)
            del response["Content-Length"]
        else:
            # Return the compressed content only if it's actually shorter.
            compressed_content = brotli_compress(response.content)
            if len(compressed_content) >= len(response.content):
                return response
            response.content = compressed_content
            response["Content-Length"] = str(len(response.content))

        # If there is a strong ETag, make it weak to fulfill the requirements
        # of RFC 7232 section-2.1 while also allowing conditional request
        # matches on ETags.
        etag = response.get("ETag")
        if etag and etag.startswith('"'):
            response["ETag"] = "W/" + etag
        response["Content-Encoding"] = "br"

        return response
