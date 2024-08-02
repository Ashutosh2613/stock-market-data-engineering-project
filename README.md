# Stock Market Data Engineering Project
### Introduction 
This project demonstrates a data engineering pipeline for stock market data using AWS and Snowflake. The pipeline extracts stock data from the Alpha Vantage API, processes the data using AWS Lambda functions, stores the data in an S3 bucket, and loads the data into Snowflake using Snowpipe.
### Architecture 

![project](https://github.com/user-attachments/assets/f4b6d919-e356-4bef-9310-ce2f98996338)

### Architecture Overview
1. Data Extraction: An AWS Lambda function extracts stock data from the Alpha Vantage API.<br/>

2. Storing Data: The extracted raw data is stored in an S3 bucket.<br/>

3. Data Transformation: Another AWS Lambda function is triggered to transform the raw data stored in S3.<br/>

4. Loading Data into Snowflake: The transformed data is then loaded into Snowflake using Snowpipe.<br/>
### Components 

1. Alpha Vantage API: Provides stock market data. The data is available from year 2001 - 2020 , enter your email to get free api which will allow 25 hits per day. <br/>

2. AWS Lambda: Used for data extraction and transformation.<br/>

3. Amazon S3: Stores raw and transformed data.<br/>

4. Snowflake: Stores the final processed data.<br/>

5. Snowpipe: Automates the loading of data into Snowflake.<br/>

