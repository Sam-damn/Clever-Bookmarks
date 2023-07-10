import logging
import re

# if brotli is installed
try:
    import brotli
except ImportError:
    brotli = None

from difflib import SequenceMatcher
from functools import lru_cache
from gzip import decompress
from html import unescape
from itertools import islice
from unicodedata import normalize

# CChardet is faster and can be more accurate
try:
    from cchardet import detect as cchardet_detect
except ImportError:
    cchardet_detect = None
from charset_normalizer import from_bytes

from lxml.html import HtmlElement, HTMLParser, fromstring

# response types
from urllib3.response import HTTPResponse


LOGGER = logging.getLogger(__name__)

UNICODE_ALIASES = {'utf-8', 'utf_8'}

DOCTYPE_TAG = re.compile("^< ?! ?DOCTYPE.+?/ ?>", re.I)


def isutf8(data):
    """Simple heuristic to determine if a bytestring uses standard unicode encoding"""
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    return True


def handle_compressed_file(filecontent):
    """Tell if a file's magic number corresponds to the GZip format
       and try to decode it. Alternatively, try Brotli if the package
       is installed."""
    if isinstance(filecontent, bytes):
        # source: https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
        if filecontent[:2] == b'\x1f\x8b':
            # decode GZipped data
            try:
                filecontent = decompress(filecontent)
            except (EOFError, OSError):
                logging.warning('invalid GZ file')
        # try brotli
        elif brotli is not None:
            try:
                filecontent = brotli.decompress(filecontent)
            except brotli.error:
                pass  # logging.debug('invalid Brotli file')
    return filecontent


def detect_encoding(bytesobject):
    """"Read all input or first chunk and return a list of encodings"""
    # alternatives: https://github.com/scrapy/w3lib/blob/master/w3lib/encoding.py
    # unicode-test
    if isutf8(bytesobject):
        return ['utf-8']
    guesses = []
    # additional module
    if cchardet_detect is not None:
        cchardet_guess = cchardet_detect(bytesobject)['encoding']
        if cchardet_guess is not None:
            guesses.append(cchardet_guess.lower())
    # try charset_normalizer on first part, fallback on full document
    detection_results = from_bytes(bytesobject[:15000]) or from_bytes(bytesobject)
    # return alternatives
    if len(detection_results) > 0:
        guesses.extend([r.encoding for r in detection_results])
    # it cannot be utf-8 (tested above)
    return [g for g in guesses if g not in UNICODE_ALIASES]


def decode_response(response):
    """
        Read the urllib3 object corresponding to the server response,
       check if it could be GZip and eventually decompress it, then
       try to guess its encoding and decode it to return a unicode string 

    """
    # urllib3 response object / bytes switch
    resp_content = response if isinstance(response, bytes) else response.data
    return decode_file(resp_content)


def decode_file(filecontent):
    """Guess bytestring encoding and try to decode to Unicode string.
       Resort to destructive conversion otherwise."""
    # init
    if isinstance(filecontent, str):
        return filecontent
    htmltext = None
    # GZip and Brotli test
    filecontent = handle_compressed_file(filecontent)
    # encoding
    for guessed_encoding in detect_encoding(filecontent):
        try:
            htmltext = filecontent.decode(guessed_encoding)
        except (LookupError, UnicodeDecodeError): # VISCII: lookup
            LOGGER.warning('wrong encoding detected: %s', guessed_encoding)
            htmltext = None
        else:
            break
    # return original content if nothing else succeeded
    return htmltext or str(filecontent, encoding='utf-8', errors='replace')

