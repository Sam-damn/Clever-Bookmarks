"""
All functions needed to steer and execute downloads of web documents.
"""


import logging
import random

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

import certifi

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from .settings import DEFAULT_CONFIG
from .utils import decode_response


NUM_CONNECTIONS = 50
MAX_REDIRECTS = 2

# globals 
HTTP_POOL = None
NO_CERT_POOL = None
RETRY_STRATEGY = None

DEFAULT_HEADERS = urllib3.util.make_headers(accept_encoding=True)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
DEFAULT_HEADERS['User-Agent'] = USER_AGENT

LOGGER = logging.getLogger(__name__)

RawResponse = namedtuple('RawResponse', ['data', 'status', 'url'])


def _parse_config(config):
    'Read and extract HTTP header strings from the configuration file.'
    # load a series of user-agents
    myagents = config.get('DEFAULT', 'USER_AGENTS').strip() or None
    if myagents is not None and myagents != '':
        myagents = myagents.split("\n")
    
    mycookie = config.get('DEFAULT', 'COOKIE') or None
    return myagents, mycookie


def _determine_headers(config, headers=None):
    'Internal function to decide on user-agent string.'
    if config != DEFAULT_CONFIG:
        myagents, mycookie = _parse_config(config)
        headers = {}
        if myagents is not None:
            rnumber = random.randint(0, len(myagents) - 1)
            headers['User-Agent'] = myagents[rnumber]
        if mycookie is not None:
            headers['Cookie'] = mycookie
    return headers or DEFAULT_HEADERS


def _send_request(url, no_ssl, config):
    "Internal function to robustly send a request (SSL or not) and return its result."
    # customize headers
    global HTTP_POOL, NO_CERT_POOL, RETRY_STRATEGY
    if not RETRY_STRATEGY:
        RETRY_STRATEGY = urllib3.util.Retry(
            total=0,
            redirect=MAX_REDIRECTS, # raise_on_redirect=False,
            connect=0,
            backoff_factor=config.getint('DEFAULT', 'DOWNLOAD_TIMEOUT')/2,
            status_forcelist=[
                429, 499, 500, 502, 503, 504, 509, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
            ],
        )
    try:
        # TODO: read by streaming chunks (stream=True, iter_content=xx)
        # so we can stop downloading as soon as MAX_FILE_SIZE is reached
        if no_ssl is False:
            # define pool
            if not HTTP_POOL:
                HTTP_POOL = urllib3.PoolManager(retries=RETRY_STRATEGY, timeout=config.getint('DEFAULT', 'DOWNLOAD_TIMEOUT'), ca_certs=certifi.where(), num_pools=NUM_CONNECTIONS)  # cert_reqs='CERT_REQUIRED'
            # execute request
            response = HTTP_POOL.request('GET', url, headers=_determine_headers(config))

        else:
            # define pool
            if not NO_CERT_POOL:
                NO_CERT_POOL = urllib3.PoolManager(retries=RETRY_STRATEGY, timeout=config.getint('DEFAULT', 'DOWNLOAD_TIMEOUT'), cert_reqs='CERT_NONE', num_pools=NUM_CONNECTIONS)
            # execute request
            response = NO_CERT_POOL.request('GET', url, headers=_determine_headers(config))
    except urllib3.exceptions.SSLError:
        LOGGER.warning('retrying after SSLError: %s', url)
        return _send_request(url, True, config)
    except Exception as err:
        LOGGER.error('download error: %s %s', url, err) 
    else:
        # necessary for standardization
        return RawResponse(response.data, response.status, response.geturl())
    # catchall
    return None



def _handle_response(url, response, decode, config):
    'Internal function to run safety checks on response result.'
    if response.status != 200:
        LOGGER.error('not a 200 response: %s for URL %s', response.status, url)
    elif response.data is None or len(response.data) < config.getint('DEFAULT', 'MIN_FILE_SIZE'):
        LOGGER.error('too small/incorrect for URL %s', url)
        # raise error instead?
    elif len(response.data) > config.getint('DEFAULT', 'MAX_FILE_SIZE'):
        LOGGER.error('too large: length %s for URL %s', len(response.data), url)
        # raise error instead?
    else:
        return decode_response(response.data) if decode is True else response
    # catchall
    return None


def fetch_url(url, decode=True, no_ssl=False, config=DEFAULT_CONFIG):
    """Fetches page using urllib3 and decodes the response.

    Args:
        url: URL of the page to fetch.
        decode: Decode response instead of returning urllib3 response object (boolean).
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        config: Pass configuration values for output control.

    Returns:
        RawResponse object: data (headers + body), status (HTML code as string) and url
        or None in case the result is invalid or there was a problem with the network.

    """
    LOGGER.debug('sending request: %s', url)
    response = _send_request(url, no_ssl, config)
   
    if response is not None and response != '':

        return _handle_response(url, response, decode, config)
        
    LOGGER.debug('request failed: %s', url)
    return None