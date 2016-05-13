"""
requires pdftotext via poppler: https://poppler.freedesktop.org/
"""

from pathlib import Path
from subprocess import Popen, PIPE

import requests
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)
PDF_URL = 'https://fbnewsroomus.files.wordpress.com/2016/05/rss-urls.pdf'
PDF_PATH = DATA_DIR.joinpath(Path(PDF_URL).name) # e.g. data/rss-urls.pdf
CSV_PATH = DATA_DIR.joinpath(PDF_PATH.stem + '.csv') # e.g. data/rss-urls.csv

# download the remote file
print("Downloading", PDF_URL)
resp = requests.get(PDF_URL)
with PDF_PATH.open('wb') as wf:
    print("Writing to", PDF_PATH)
    wf.write(resp.content)

rows = []
with Popen(['pdftotext', '-layout', str(PDF_PATH), '-'], stdout=PIPE, universal_newlines=True) as p:
    for txt in p.stdout:
        line = txt.strip()
        print(i, line)
        if ' ' in line:
            rows.append(line.split(' '))
        else:
            rows[-1][-1] += line


