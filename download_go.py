import feedparser
import requests

download_url = lambda version: f'https://golang.org/dl/{version}.linux-amd64.tar.gz'

def get_latest_url():
    feed_url = "https://github.com/golang/go/releases.atom"
    feed_data = feedparser.parse(feed_url)
    top_entry = feed_data.entries[0]
    top_id = top_entry.id.split('/')[-1]
    version = top_id
    return download_url(version)

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

if __name__ == '__main__':
    gourl = get_latest_url()
    download_file(gourl)
