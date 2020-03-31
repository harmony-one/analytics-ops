# Harmony Analytics Ops
This is the main repo for all ops handled by the analytics machine.

## Installation
Clone this repo and while in the root of this repo, run: 
```
pip3 install . && chmod +x ./go.py
```
> Note that this assumes python3 and pip3 is installed

## Usage
All useful commands are executed from the python CLI: `./go.py`.

1) To download the latest 2 batches of logs, execute the following command:
```
./go.py log download stn --count 2
```
> Note that this assumes that the analytics machine has the proper credentials for s3

2) To download a specific file, execute the following command:
```
./go.py log download-from-path s3://harmony-benchmark/logs/2020/03/27/001302 --exclude "*" --include "zerolog-validator-*-2020-03-25T*.gz" 
```
 
3) To protect a notebook, execute the following command:
```
./go.py notebook protect Test.ipynb 
```
> Note that the `.ipynb` is optional. Moreover, the CLI will iterate through 
> nested directories to find all files that match the given name.

4) To share a notebook, execute the following command:
```
./go.py notebook share Test.ipynb 
```
> Note that the `.ipynb` is optional

5) To protect a file or directory, execute the following command:
```
./go.py notebook protect-path ~/jupyter/Test.ipynb 
```

6) To share a file or directory, execute the following command:
```
./go.py notebook share-path ~/jupyter/Test.ipynb 
```

7) To publish a notebook, execute the following command:
```
./go.py notebook publish Test.ipynb 
```
> Note that the `.ipynb` is optional. Moreover, the CLI will iterate through 
> nested directories to find all files that match the given name.