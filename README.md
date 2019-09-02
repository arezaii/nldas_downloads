# NLDAS2 Data Bulk Downloader
python script to bulk download NLDAS files from https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS
can download hourly or monthly data

## Requirements
* python 3.7
* requests
* tqdm

## Usage
usage: download_nldas_forcings.py [-h] --from_date FROM_DATE --to_date TO_DATE
                                  --username USERNAME --password PASSWORD
                                  [--output_dir OUTPUT_DIR] [--hourly]
                                  [--monthly]
				  
the following arguments are required: --from_date/-fd, --to_date/-td, --username/-u, --password/-p

  
ex: 

```bash
$ python download_nldas_forcings.py -fd=2011-08-01 -td=2012-08-01 -u=username -p=password -H
```

## Description
Given a start date and end date, create either hourly or monthly links for each of the forcings data files.

Create a session to the https NASA data server at https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/

Download each of the grib (.grb) files to ./nldas-from_date.to.to_date
ex:
 ./nldas-2011-08-01.to.2012-08-01

User can specify output directory by specifying with -o flag
ex:
```bash
$ python download_nldas_forcings.py -fd 2011-08-01 -td 2012-08-01 -u username -p password -H -o nldas_downloads
```

## Anaconda environment setup
to use the included environment.yml files
```bash
$ conda env create --file environment.yml
```

## Troubleshooting

If you are getting HTTP back (~3KB) instead of grib files (~1.8MB), make sure you have added the application "NASA GESDISC DATA ARCHIVE" 
in your https://urs.earthdata.nasa.gov account under applications>authorized apps
