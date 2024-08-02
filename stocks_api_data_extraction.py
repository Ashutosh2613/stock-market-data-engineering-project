import json
import urllib3
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey=BGPEQ8T5S9GS5KE9'
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    data = json.loads(response.data.decode('utf-8'))
    print(data)
    
    client = boto3.client('s3')
    filename = "raw_stock_data" + str(datetime.now()) + ".json"
    client.put_object(
        Bucket = "stock-market-bucket-ashutosh",
        Key = "raw-data/to-processed/"+ filename,
        Body = json.dumps(data)
        
        )
    
    
