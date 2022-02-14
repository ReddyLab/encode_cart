## Requirements
* Python 3.6+
* [requests](https://docs.python-requests.org/en/latest/)

## Installation
Clone the repository with `git clone https://github.com/ReddyLab/encode_cart.git` then change into the repository directory. Optionally, you can create a virtual environment. Finally, run `pip install -r requirements.txt`.

## Run

`python encode_cart.py --name "Cart Name" --authfile auth_file.txt --accessions accession_file.txt`

### Arguments
* --name/-n: The name of the cart
* --auth_file/-f: A file with your access key access key id
* --accessions/-a: A file with a list of accession ids
* --test: Use the test server instead of production.

#### Auth File
This file should have just one line, with your Access key ID and Access key on it, separated by a space. Example:

    7SD5D1D7 ertyuiol7kjnbvcd4rt

#### Accession File
This file should have one access ID per line. The accession IDs should be of the format `/accession-type/ID/`. Example File:

    /functional-characterization-experiments/ENCSR476KHP/
    /experiments/ENCSR216YPQ/

