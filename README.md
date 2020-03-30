# Harmony Analytics Ops
This is the main repo for all ops handled by the analytics machine.

## Installation
While in the root of this repo, run: 
```
pip3 install . && chmod +x ./go.py
```
> Note that this assumes python3 and pip3 is installed

## Usage
All useful commands are executed from the python CLI: `./go.py`.
> Note that there is an assumption that the current working directory is the root of this repo.
> Some checks are done to check for said assumption. 

1) To download the latest 2 batches of logs, execute the following command:
```
./go.py download_logs stn --count 2
```
> Note that this assumes that the analytics machine has the proper credentials for s3
 
