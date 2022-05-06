# Zluri Assignment - Large file processor

## Choice of DB :
MongoDB would be ideal choice here, for faster writes with bulk_write APIs available. Solution uploaded is for mysql.
For MongoDB, just a quick manual steps were used

## Steps to run (Mongo)

Catalog collection is created
> use zluri

create catalog collection
> db.createCollection("catalog")

create unique index of SKU
> db.catalog.createIndex( { sku: 1 }, { unique: true } )

Run bulk upload using Mongo Compass, directly uploading whole CSV in less than 30 seconds on Mac Pro, 16 GB

Run aggregate query
> db.catalog.aggregate([{"$group":{_id:"$name",count:{$sum:1}}},{$sort:{count:-1}}])

Screenshots in mongo folder


## Steps to run (MySQL)

### Step 1 : Create required DB tables
Two tables needs to be created in mysql with below scripts

**Catalog** table : Stores valid product items 
> CREATE TABLE `catalog` (
  `sku` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `updatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `createdAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

**error_catalog** : stores rows where atleast one column value is missing

>CREATE TABLE `error_catalog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1547050 DEFAULT CHARSET=latin1;

### Step 2 : Run file_processor.py
mysql connector for python is required to run script. Use - pip install mysql-connector-python

## Results
- No. of records created (insert + update) in **catalog table - 466693**
- No. of records with **missing data - 364832**

![Catalog Sample Data](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/catalog_sample.png)

![Rows with missing data](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/catalog_with_missing_data.png)

**DB insert with parallel processing < 100 seconds** on Mac Pro, 16 GB RAM, 12 Cores
![Runtime](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/runtime.png)


**Aggregate query with no. of rows with same name**
![Aggregate Query](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/count_by_name.png)

## Points Achieved
- Non blocking parallel ingestion
- update existing product in catalog, based on sku during insert
- ingestion in single table
- Runtime < 2 mins
- OOPS with Flake 8 formatting convention

## Pending Items
- None

## Improvements
- Creating DockerFile for single step deployment
- Handle records with missing data - rows with missing description can be inserted in catalog table based on inference of separation by dash (-) for sku
- Clean single quotes, double quotes for description
- Test with bigger files to test scaling
- Test cases for validation of records

## References 
- https://nurdabolatov.com/parallel-processing-large-file-in-python
