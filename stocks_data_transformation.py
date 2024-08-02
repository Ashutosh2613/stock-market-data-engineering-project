import json
import pandas as pd
import boto3
from datetime import datetime
from io import StringIO

def stock_fun(data):
  data_list = []
  stock =  data['Meta Data']['2. Symbol']
  for timestamp,value in data['Time Series (5min)'].items():
    timestamp = timestamp
    open = value['1. open']
    close  =  value['4. close']
    low = value['3. low']
    high = value['4. close']
    volume = value['5. volume']
    data_dict = {'stock':stock,'timestamp':timestamp,'open':open,'close':close,'low':low,'high':high,'volume':volume}
    data_list.append(data_dict)
  return data_list


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "stock-market-bucket-ashutosh"
    Key = "raw-data/to-processed/"
    stock_list = []
    stock_key = []
    for file in s3.list_objects(Bucket = Bucket,Prefix = Key)['Contents']:
      file_key = file['Key']
      if file_key.split('.')[-1] == 'json':
        response = s3.get_object(Bucket = Bucket, Key = file_key)
        content = response['Body']
        jsonObject = json.loads(content.read())
        # print(jsonObject)
        stock_list.append(jsonObject)
        stock_key.append(file_key)
        
        # print(stock_list)
        
    for data in stock_list:
      stock_trf = stock_fun(data)
      data_df = pd.DataFrame(stock_trf)
      print(data_df)
      data_df.drop_duplicates(subset = ['timestamp'])
      # print(data_df)
      data_df_key = "transformed-data/transformed_stock_data" + str(datetime.now()) + ".csv"
      data_df_buffer = StringIO()
      data_df.to_csv(data_df_buffer,index = False)
      data_content = data_df_buffer.getvalue()
      # print(data_content)
      s3.put_object(Bucket = Bucket, Key = data_df_key, Body = data_content)
      
      s3_resource = boto3.resource('s3')
      for key in stock_key:
        copy_source = {'Bucket': Bucket, 'Key':key}
        s3_resource.meta.client.copy(copy_source,Bucket,'raw-data/processed/'+ key.split('/')[-1])
        s3_resource.Object(Bucket,key).delete()
      
      
      
    
    
    
    