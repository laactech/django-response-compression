from typing import Generator

from brotli import Compressor, compress
from django.conf import settings

BROTLI_COMPRESSION_LEVEL = getattr(settings, "RESPONSE_COMPRESSION_BROTLI_LEVEL", 4)


def brotli_compress(content: bytes, compression_level: int = BROTLI_COMPRESSION_LEVEL) -> bytes:
    return compress(content, quality=compression_level)


def brotli_compress_stream(
    sequence: Generator[bytes, bytes, None], compression_level: int = BROTLI_COMPRESSION_LEVEL
) -> Generator[bytes, bytes, None]:
    yield b""
    compressor = Compressor(quality=compression_level)
    process = compressor.process
    for item in sequence:
        out = process(item)
        if out:
            yield out
    out = compressor.finish()
    if out:
        yield out
