# nldas_downloads
python script to bulk download NLDAS hourly files from hydro1.gesdisc.eosdis.nasa.gov

## Requirements
* python 3.7
* requests
* tqdm

## Usage
$ python download_nldas_forcings.py <FromDate YYYY-MM-DD> <ToDate YYYY-MM-DD> <username> <password> <output dir>
									[-h] [-o, --output_dir OUTPUT_DIR]
									from_date to_date username password
  
  the following arguments are required: from_date, to_date, username, password

