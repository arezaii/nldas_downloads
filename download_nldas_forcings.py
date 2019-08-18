# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:00:14 2019

@author: Ahmad Rezaii
"""

import datetime
import argparse
import os
import requests
import tqdm


BASE_URL='https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002'


#Parse the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('from_date',
                    help="Start Date/Time Format (inclusive) YYYY-MM-DD",
                    type=datetime.date.fromisoformat)

parser.add_argument('to_date',
                    help="End Date/Time (inclusive) Format YYYY-MM-DD",
                    type=datetime.date.fromisoformat)

parser.add_argument('username',
                    help=("Username to access data from "
                          "https://disc.gsfc.nasa.gov/data-access"))

parser.add_argument('password',
                    help=("Password to access data from "
                          "https://disc.gsfc.nasa.gov/data-access"))

parser.add_argument('-o, --output_dir', dest='output_dir',
                    help=("Output Directory "
                    "(default ./nldas-<from_date>.to.<to_date>"),
                    required=False)

args = parser.parse_args()

#validate the arguments
if (args.to_date < args.from_date):
    raise ValueError("from_date must be less than or equal to to_date")

if (args.output_dir is None):
    output_dir = os.path.join(os.curdir,
                              f'nldas-{args.from_date}.to.{args.to_date}')
else:
    output_dir = os.path.join(os.curdir,args.output_dir)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)



def get_url_list(from_date, to_date):
    """
    create a list of URLs to download based on the date range
    """
    date_diff = to_date - from_date
    target_dates=[]
    download_urls=[]

    for i in range(date_diff.days + 1):
        target_dates.append((from_date + datetime.timedelta(days=i)))

    for i in range(len(target_dates)):
        for j in range(24):
            download_urls.append((f'{BASE_URL}/{target_dates[i].year}/'
                                  f'{target_dates[i].timetuple().tm_yday:03d}/'
                                  f'NLDAS_FORA0125_H.A{target_dates[i].year}'
                                  f'{target_dates[i].month:02d}'
                                  f'{target_dates[i].day:02d}.{j:02d}00.002.grb'
                                  ))

    return download_urls


# overriding requests.Session.rebuild_auth to mantain headers when redirected

class SessionWithHeaderRedirection(requests.Session):
    """
    adapted from
    https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
    """

    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

   # Overrides from the library to keep headers when redirected to or from
   # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and \
    			redirect_parsed.hostname != self.AUTH_HOST and \
                original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


def download_files_from_url(urls, output_dir):
    """
    visit and download the files from the
    for the list of urls for the files we wish to retrieve
    """
    responses = []
   
    # display progress bar (thanks tqdm!) and download the files
    for url in tqdm.tqdm(urls, ncols=80):
        # extract the filename from the url to be used when saving the file
        filename = url[url.rfind('/')+1:]

        try:
            # submit the request using the session
            response = session.get(url, stream=True)
            responses.append(response)

            # raise an exception in case of http errors
            response.raise_for_status()

            # save the file
            with open(os.path.join(output_dir,filename), 'wb') as fd:
                fd.write(response.content)

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print(e)

    return responses


# create session with the user credentials that will be used to authenticate
#access to the data

session = SessionWithHeaderRedirection(args.username, args.password)

urls = get_url_list(args.from_date, args.to_date)

file_count = len(urls)
download_size = file_count * 3

print(f'Proceeding to download {file_count} files...')
print(f'Downloading approx. {download_size} KB')


download_files_from_url(urls, output_dir)
