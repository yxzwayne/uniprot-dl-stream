import re
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ChunkedEncodingError, ConnectionError, Timeout, RequestException
from urllib3.exceptions import ProtocolError
import logging

# Setup logging
logging.basicConfig(filename='download.log', level=logging.INFO)

re_next_link = re.compile(r'<(.+)>; rel="next"')
retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):
    while batch_url:
        try:
            response = session.get(batch_url, timeout=10)
            response.raise_for_status()
            total = response.headers["x-total-results"]
            yield response, total
            batch_url = get_next_link(response.headers)
        except (ChunkedEncodingError, ProtocolError, ConnectionError, Timeout, RequestException) as e:
            logging.error(f"Encountered a network error: {e}, retrying...")
            continue  # This will cause the loop to retry the current batch_url

save_file_name = "prot.aol.tsv"
url = "https://rest.uniprot.org/uniparc/search?fields=upi%2Csequence&format=tsv&query=%28protease%29&size=500"

progress = 0
with open(save_file_name, "w") as f:
    for batch, total in get_batch(url):
        lines = batch.text.splitlines()
        if not progress:
            print(lines[0], file=f)
        for line in lines[1:]:
            print(line, file=f)
        progress += len(lines[1:])
        print(f"{progress} / {total}")
        logging.info(f"Progress: {progress} / {total}")
        print(f"{progress} / {total}")