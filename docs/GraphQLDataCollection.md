# Data Collection

In running and testing the GraphQL implementation, we will need to have sample data to work with. There will be sample data collected for both the CanDIG server and the Katsu Database, to facilitate experiments with both the federated-learning repository and with the CanDIG Beacon V1 API. Note that **FOR ALL** ingestion tasks, it is imperative that you have the respective servers already set up and running.

## Test Data Collection (Holistic)

If you want to test the GraphQL module or just want connected Katsu and CanDIG data without the hassle of searching through schemas to create your own data, the holistic approach described here should work best.

This process will connect CanDIG variant data with Katsu Patient Information and will generate random mCODE Packet Information as well as phenopacket Information for testing purposes. Ensure you already have the canDIG variant data ingested. This would already be done for you if you installed the canDIG V1 server through the provided [dockerfile](helpers/candig-server/Dockerfile) (such as if you followed the instructions in installing via `docker-compose` from the [GraphQLIntroduction File](GraphQLIntroduction.md)). Otherwise [download and ingest that data first](#canDIG), otherwise the following steps will not be of use to you. Note that a set of commands that will be needed for this ingestion are listed at the end of this section.

### Variant Patient Data Collection & Ingestion

1. Create a virtual environment called `venv` in your root `projects` directory.
2. Activate the virtual environment.
3. Move to the root `GraphQL-interface` Repository.
4. Install the required dependencies:
   - `pip install wheel pandas sklearn`
   - `pip install -r requirements.txt`
5. Ensure that the `DEFAULT_HOST, DEFAULT_KATSU_PORT & DEFAULT_CANDIG_PORT` variables in [defaults.py](helpers/CanDig-Katsu-Ingestion/defaults.py) are set to the proper values for your machine.
6. Run the Ingestion Script!

Full list of commands (start in the root `projects` directory):

```bash
python3 -m venv venv
source venv/bin/activate
cd GraphQL-interface
pip install wheel pandas sklearn
pip install -r requirements.txt
python3 ./docs/helpers/CanDig-Katsu-Ingestion/build_data.py
```

This process will take several minutes and once completed, should add around 300 variant records to Katsu, adding phenopacket and mcodepacket data for each of the patients as well. Note that there are several data points (there should be 6 individuals, plus their respective mCODE and phenopackets) which will print an error message due to incomplete data. This is normal and is an artifact of the CanDIG variant data, so you can ignore such messages.

## Separate Data Collection

If you want to install the data separately or are looking for a specific subset of the data, the following steps should be of use to you.

### Katsu Data Collection

If you want to generate the random Katsu Data, simply run the script described above from the root GraphQL directory, as described above. If you wish to collect and ingest other Katsu Data, such as the Synthea mCODE data, you will need to ensure you have the federated-learning repository cloned. The Katsu Data that will be ingested will be done through the federated-learning repository, since it contains many required ingestion scripts. The guide on ingesting Katsu Data is present in the [KatsuIngestion](KatsuIngestion.md) file.

<div id='canDIG'>

### CanDIG Data Collection & Ingestion

The required CanDIG data for this project is simply the CanDIG Variant Data that can be ingested through the steps located on the [CanDIG Documentation](https://candig-server.readthedocs.io/en/v1.5.0-alpha/data.html#reads-variants-and-references-data). If you set up the CanDIG Server using the `Dockerfile`, the data has already been ingested for you. Otherwise, the steps are noted below (Ensure you start from the candig-server directory). Note that `test_server` is simply the name of the `virtualenv` we used in setting up our CanDIG server; Yours may be called something different (though if you followed the [instructions](https://candig-server.readthedocs.io/en/v1.5.0-alpha/development.html#standalone-candig-server-setup) on the CanDIG Server Documentation, like us, then you should have a `virtualenv` named `test_server` as well). Note that the script below is modified from the test script present in the [CanDIG V1 Documentation](https://candig-server.readthedocs.io/en/v1.5.0-alpha/development.html#standalone-candig-server-setup). Additionally, we have also downloaded and ingested extra clinical metadata into the CanDIG server to display that the GraphQL service will not error out even if there are datasets that do not contain variant information.

```bash
cd test_server
source bin/activate

mkdir candig-example-data

wget https://raw.githubusercontent.com/CanDIG/candig-ingest/master/candig/ingest/mock_data/clinical_metadata_tier1.json
wget https://raw.githubusercontent.com/CanDIG/candig-ingest/master/candig/ingest/mock_data/clinical_metadata_tier2.json
ingest candig-example-data/registry.db mock1 clinical_metadata_tier1.json
ingest candig-example-data/registry.db mock2 clinical_metadata_tier2.json

wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/bigZips/hg19.fa.gz
gunzip hg19.fa.gz

wget https://github.com/CanDIG/test_data/releases/download/v1.0.0/group1.tar
wget https://github.com/CanDIG/test_data/releases/download/v1.0.0/group1_load.sh
wget https://github.com/CanDIG/test_data/releases/download/v1.0.0/group1_clinphen.json

tar xvf group1.tar

sed -i 's/GRCh37-lite/hg19a/' group1_load.sh
sed -i 's/registry.db/candig-example-data\/registry.db/' group1_load.sh

chmod +x group1_load.sh
ingest candig-example-data/registry.db test300 group1_clinphen.json
candig_repo add-referenceset candig-example-data/registry.db hg19.fa -d "hg19a reference genome" --name hg19a
bash ./group1_load.sh
```

The above script both downloads and ingests data for the canDIG V1 server. The first two `wget` & `ingest` commands download and ingest mock clinical data, that isn't attached to any variant data. This is for testing purposes to ensure that our GraphQL service doesn't throw errors if it searches through datasets with no variant information. The next `wget` command simply downloads a sample FASTA file that is a reference set for the variants we will ingest later on. It is then promptly unzipped. The following three `wget` commands download the variant data for all 300 test patients, they also download a setup script and a clinical metadata file. These files are available at the [canDIG github releases](https://github.com/CanDIG/sample-data-generator/releases), if you prefer to download them manually.

The script then unzips the downloaded files, modifies the files for minor name and filepath corrections, and finally uses the internal commands of candig-server to ingest the collected data.

Once the script is complete, you should now have three new datasets called `mock1, mock2 & test300` with the ingested data.
