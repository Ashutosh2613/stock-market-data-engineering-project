
-- This code establishes connection between aws-s3 bucket and snowflake 
-- Also created snowpipe to automate the process

--db for project
CREATE DATABASE stocks_db
CREATE SCHEMA stocks_schema
CREATE SCHEMA aws_stage
-- table to load data
CREATE TABLE stocks_db.stocks_schema.stocks_data(
stock     string ,       
timestamp  string ,  
open   float  ,
close   float  , 
low   float  ,
high  float,
volume  float
)

--connecting aws_s3 with snowflake 
create storage integration aws_s3_int
    type = external_stage
    storage_provider = s3
    storage_aws_role_arn = 'Put your arn'
    enabled = true
    storage_allowed_locations = ( 's3://your-bucket-name' )
     comment = 'cretaing connection to aws for stocks project';

desc storage integration aws_s3_int
create schema file_formats

create file format stocks_db.file_formats.csv_format
TYPE = 'csv'

desc file format stocks_db.file_formats.csv_format

alter file format stocks_db.file_formats.csv_format
set skip_header = 1

create or replace stage aws_stage.csv_folder
url = 's3://your-bucket-name/folder-name'
storage_integration = aws_s3_int
file_format = stocks_db.file_formats.csv_format

list @aws_stage.csv_folder

copy into stocks_db.stocks_schema.stocks_data
from @aws_stage.csv_folder

select * from stocks_db.stocks_schema.stocks_data

create or replace schema stocks_db.pipes

create pipe stocks_db.pipes.stocks_pipe 
auto_ingest = true
as
copy into stocks_db.stocks_schema.stocks_data
from @aws_stage.csv_folder


desc pipe stocks_db.pipes.stocks_pipe 




