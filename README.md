# Zluri Assignment - Large file processor

## Steps to run

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
No. of records inserted in **catalog table - 466693**
No. of records with **missing data - 364832**

![Catalog Sample Data](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/catalog_sample.png)
![Rows with missing data](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/catalog_with_missing_data.png)
**DB insert with parallel processing completed in approx 2.5 minutes** on Mac Pro, 16 GB RAM


**Aggregate query with no. of rows with same name**
![Aggregate Query](https://github.com/anmolmore/zluri_data_engineer/blob/main/results/count_by_name.png)
## Points Achieved
- Non blocking parallel ingestion
- update existing product in catalog, based on sku during insert
- ingestion in single table
- OOPS with Flake 8 formatting convention

## Pending Items
- Total no. of rows mismatch, validation required to identify missing chunk
- Reduce insertion time to less than 2 minutes

## Improvements
- Creating DockerFile for single step deployment
- Handle records with missing data - rows with missing description can be inserted in catalog table
- Clean single quotes, double quotes for description
- Test with bigger files to test scaling
- Test cases for validation of records