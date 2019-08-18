# NLDAS2 Hourly Data Bulk Downloader
python script to bulk download NLDAS hourly files from hydro1.gesdisc.eosdis.nasa.gov

## Requirements
* python 3.7
* requests
* tqdm

## Usage
download_nldas_forcings.py <FromDate YYYY-MM-DD> <ToDate YYYY-MM-DD> <username> <password> <output dir>
									[-h] [-o, --output_dir OUTPUT_DIR]
									from_date to_date username password
  
  the following arguments are required: from_date, to_date, username, password
  
ex: 

```bash
$ python download_nldas_forcings.py 2011-08-01 2012-08-01 username password 
```

## Description
Given a start date and end date, create links for each of the hourly forcings data files.

Create a session to the https NASA data server at https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002/

Download each of the grib (.grb) files to ./nldas-from_date.to.to_date
ex:
 ./nldas-2011-08-01.to.2012-08-01

User can specify output directory by specifying with -o flag
ex:
```bash
$ python download_nldas_forcings.py 2011-08-01 2012-08-01 username password -o nldas_downloads
```

## Anaconda environment setup
to use the included environment.yml files
```bash
$ conda env create --file environment.yml
```