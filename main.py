import os
import sys
import time
import concurrent.futures
import httpx
from urllib.parse import urlparse
import logging


# CURRENTLY MANUALLY SET. UPDATE AS ARGS OR ENVIRONMENT VARIABLES
log_to_screen = True
log_to_file = True
log_dir_path = './.itwaisi/logs'
log_filename = 'app.log'
log_file_path = os.path.join(log_dir_path, log_filename)


# CHECK IF LOG DIRECTORY EXISTS OR NOT
if not os.path.exists(log_dir_path):
    
    # CREATE LOG DIRECTORY IF IT DOES NOT EXIST
    os.makedirs(log_dir_path, True) 

# CREATE LOGGER
logger = logging.getLogger('StressLogger')

# SET DEFAULT LOGGING LEVEL
logger.setLevel(logging.DEBUG)

# LOGGING FORMAT
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# LOG TO SCREEN IF ENABLED
if log_to_screen:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# LOG TO FILE IF ENABLED
if log_to_file:
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# FUNCTION: PARSE SYSTEM ARGS AND SET DEFAULT VALUE
def parse_arg(arg_list, arg_key, def_value=None):
    return next((arg.split('=')[1] for arg in arg_list if arg.startswith(f'{arg_key}=')), def_value)


# FUNCTION: CONVERT SYSTEM ARG FROM STRING TO INTEGER
def parse_int_string(data):
    return int(data) if data.isdigit() else None


# FUNCTION: CONVERT SYSTEM ARG FROM STRING TO BOOLEAN
def parse_boolean(data):
    return True if data.lower() == 'true' or data == '1' else False


# FUNCTION: GET SYSTEM ARGS
def get_args():
    
    arg_list = sys.argv

    # URL TO REQUEST
    ARG_URL = parse_arg(arg_list, 'url', None)
    print(f'[STRESS TEST] :: ARG_URL :: {ARG_URL}\r\n')
    logger.info(f'[LOG: STRESS TEST] :: ARG_URL :: {ARG_URL}\r\n')
    
    # NUMBER OF REQUESTS TO CALL
    ARG_REQUESTS = parse_int_string(parse_arg(arg_list, 'requests', None))
    print(f'[STRESS TEST] :: ARG_REQUESTS :: {ARG_REQUESTS}\r\n')

    # NUMBER OF WORKERS
    ARG_WORKERS = parse_int_string(parse_arg(arg_list, 'workers', None))
    print(f'[STRESS TEST] :: ARG_WORKERS :: {ARG_WORKERS}\r\n')
    
    # SERVER IP RUNNING STRESS TEST
    ARG_SERVER_IP = parse_arg(arg_list, 'ip', None)
    print(f'[STRESS TEST] :: ARG_SERVER_IP :: {ARG_SERVER_IP}\r\n')

    # USE VPN
    ARG_VPN = parse_boolean(parse_arg(arg_list, 'vpn', True))
    print(f'[STRESS TEST] :: ARG_VPN :: {ARG_VPN}\r\n')
    
    
    
    url_check_ip = 'https://httpbin.org/anything'
    # url_check_ip = 'https://icanhazip.com'

    # Parse the URL
    parsed_url = urlparse(url_check_ip)

    # Extract the domain name (netloc)
    domain = parsed_url.netloc

    # If you want to remove 'www.' if present
    header_host = domain.lstrip('www.')

    headers = {
        'Host': header_host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
    }

    try:
        response = httpx.get(url_check_ip, headers=headers, timeout=10)
        response.raise_for_status()

    except httpx.RequestError as e:
        print(f'[STRESS TEST] :: An error occurred while requesting :: {e.request.url}')
        print(e)
    
    except httpx.HTTPStatusError as e:
        print(f'[STRESS TEST] :: HTTP error occurred')
        print(e)

    except Exception as e:  # Catch any other unexpected exceptions
        print(f'[STRESS TEST] :: An unexpected error occurred')
        print(e)

    else:
        # RESPONSE DATA
        print('[STRESS TEST] :: Request Headers')
        print(response.request.headers, '\r\n')
        print('[STRESS TEST] :: Response Headers')
        print(response.headers, '\r\n')

        # TEST
        # current_ip = ''

        # HTTPBIN
        current_ip = response.json()['origin']

        # ICANHAZIP
        # current_ip = response.content.decode(encoding='utf-8').strip()
    
    # print(f'arg vpn {ARG_VPN}')
    
    if ARG_VPN and ARG_SERVER_IP == current_ip:
        print(f'[STRESS TEST] :: IP Matches :: Must Use VPN :: {current_ip}\r\n')
        exit(0)
    else:
        print(f'[STRESS TEST] :: IP Not Checked :: VPN Not In Use :: {current_ip}\r\n')
        return {
            'url': ARG_URL,
            'requests': ARG_REQUESTS,
            'workers': ARG_WORKERS,
            'server_ip': ARG_SERVER_IP,
        }
    


def main():
    
    args = get_args()
    
    print('[STRESS TEST] :: Start')
    
    # TEMP EXIT
    # exit(0)
    
    # get time before the requests are sent
    start = int(time.time())
    
    # input URLs/IPs array
    urls = []
    
    # output content of each request as string in an array
    responses = []
    
    # create an list of 5000 sites to test with
    counter_url = 0
    for y in range(args['requests']):
        counter_url += 1
        print(f'[STRESS TEST] :: Add URL {counter_url} times')
        urls.append(args['url'])
    
    def send(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0'
        }
        content = httpx.get(url, headers=headers).content
        responses.append(content)
        print(f'[STRESS TEST] :: (send) :: Append scraped content to list :: {url}')
        print(content)
        print(f'[STRESS TEST] :: (send) :: End :: {url}')
    
    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=args['workers']) as executor:
        futures = []
        for index, url in enumerate(urls):
            futures.append(executor.submit(send, url))
            print(f'[STRESS TEST] :: Add (future submit) to list {index}/urls.length :: {url}')
    '''
    
    ''''''
    with concurrent.futures.ThreadPoolExecutor(max_workers=args['workers']) as executor:
        futures = []
        for index, url in enumerate(urls):
            futures.append(executor.submit(send, url))
            print(f'[STRESS TEST] :: Add (future submit) to list {index}/{len(urls)} :: {url}')
        for future in concurrent.futures.as_completed(futures):
            responses.append(future.result())
            print(f'[STRESS TEST] :: Add (future result) to list {index}/{len(urls)} :: {url}')
    ''''''
    
    end = int(time.time()) # get time after stuff finishes

    # get average requests per second
    elapsed_time = end - start
    if elapsed_time == 0:
        rate = 'Infinity'  # Or you can set it to 0
    else:
        rate = str(round(len(urls) / elapsed_time, 0))

    print(f'[STRESS TEST] :: {rate}/sec')


if __name__ == '__main__':
    main()
