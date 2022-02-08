# Katsu Data Collection

## Synthea Ingestion

To collect sample Katsu Data, we will ingest the Synthea Cancer MCode Data. This is especially helpful for machine learning analysis with GraphQL, such as with the federated-learning repository.

1. Download the Synthea Dataset from the [HL7 Confluence Page](https://confluence.hl7.org/display/COD/mCODE+Test+Data)
   - Choose the Dataset labeled: **Approx. 2,000 Patient Records with 10 Years of Medical History**
2. Unzip the collected folder and move the `10yrs` folder into the federated-learning directory
3. Ingest the data within the 10yrs folder. Note that this might take several minutes to complete.

### Synthea Ingestion Code

```
cp 10yrs/female/* 10yrs/male/* 10yrs/assorted/* 10yrs
rm -r 10yrs/female 10yrs/male 10yrs/assorted
./ingestion_scripts/init.sh -l -d 10yrs test_proj test_dataset test_table mcodepacket
```
