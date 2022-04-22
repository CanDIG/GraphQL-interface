# CanDIG-Katsu Ingestion

This repo houses the Katsu data generating script(s) & functions.

## Current State

The scripts were designed with testing for the Beacon implementation in mind and as such, require the use of both an instance of the CanDIG variants service as well as an instance of the Katsu metadata service. The data located within the CanDIG server should be the data ingested when building the variants service's Docker container. This data is the same data downloaded via the instructions for data ingestion in the [variants service documentation](https://candig-server.readthedocs.io/en/v1.5.0-alpha/data.html#reads-variants-and-references-data) and the [GraphQL Data Collection documentation](https://github.com/CanDIG/GraphQL-interface/blob/master/docs/GraphQLDataCollection.md#candig-data-collection--ingestion).

## Files

### build_data.py

The `build_data.py` file is the main script to be run for our Katsu data generation. It'll call the `candig_to_katsu.py` file to transfer patient information from the CanDIG variants service to the Katsu metadata service, and then will generate patient clinical records for each patient added to Katsu. This includes mCODEpackets, phenopackets, geneticSpecimen information among others.

### candig_to_katsu.py

This file transfers patient information from the variants service to the Katsu metadata service. The current `candig_to_katsu.py` script searches the variants service for the third database to find its data. This is becasue the Docker initialization of the variants service had the variant data in its third database, and as such, if you change the order of data download, or if you only download the variants data, then you will need to modify this. Change the index of the database searched within the `get_dataset_id` function for this purpose.

### create_meta.py

This file houses several functions that are related to uploading meta information to the Katsu metadata service. This includes creating the tables for phenopackets and mcodepackets and POSTing them to the Katsu metadata service, among other functions.

### defaults.py

This file houses several default values such as the default HOST and PORT information for the Katsu Metadata service and CanDIG variants service. It also houses default values for the data generator such as a list of default procedures and conditions.

### generate_data.py

This file houses the functions related to generating random data for the Katsu metadata service, like random dates, random mcodepacket data, etc.

### get_data.py

This file houses functions related to GETting information from the CanDIG variants service and Katsu metadata service.

### post_data.py

This file houses functions related to POSTing data to the CanDIG variants service and Katsu metadata service.

## Usage

### Dependencies

- aiohttp==3.8.1

### Quick Start

To use the generator, we can follow the instructions present in the `GraphQLDataCollection.md` file within the `docs` subdirectory. Essentially follow the steps listed below:

> This process will connect CanDIG variant data with Katsu Patient Information and will generate random mCODE Packet Information as well as phenopacket Information for testing purposes. Ensure you already have the canDIG variant data ingested. This would already be done for you if you installed the canDIG V1 server through the provided [dockerfile](helpers/candig-server/Dockerfile) (such as if you followed the instructions in installing via `docker-compose` from the [GraphQLIntroduction File](GraphQLIntroduction.md)). If not, [download and ingest that data first](#canDIG), or the following steps will not be of use to you. Note that a set of commands that will be needed for this ingestion are listed at the end of this section.
>
> ### Variant Patient Data Collection & Ingestion
>
> 1. Create a virtual environment called `venv` in your root `projects` directory.
> 2. Activate the virtual environment.
> 3. Move to the root `GraphQL-interface` Repository.
> 4. Install the required dependencies:
>    - `pip install -r requirements.txt`
> 5. Ensure that the `DEFAULT_HOST, DEFAULT_KATSU_PORT & DEFAULT_CANDIG_PORT` variables in [defaults.py](helpers/CanDig-Katsu-Ingestion/defaults.py) are set to the proper values for your machine.
> 6. Run the Ingestion Script!
>
> Full list of commands (start in the root `projects` directory):
>
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> cd GraphQL-interface
> pip install -r requirements.txt
> python3 ./docs/helpers/CanDig-Katsu-Ingestion/build_data.py
> ```
>
> This process will take several minutes and once completed, should add around 300 variant records to Katsu, adding phenopacket and mcodepacket data for each of the patients as well. Note that there are several data points (there should be 6 individuals, plus their respective mCODE and phenopackets) which will print an error message due to incomplete data. This is normal and is an artifact of the CanDIG variant data, so you can ignore such messages.

## Technical Debt

- Move this to its own repository to make it easier to use.
- Make better use of async python using `asyncio.gather()` for example instead of `for` loop within `build_data.py`.
- Refactor layout of files in this folder to make more logical sense.
- Change python imports between files to be `import filename` instead of `from filename import *` so that it is clear which function comes from which file.
- Change script use case to generate data for arbitrary patients, not just those linked to in the CanDIG variants service.
