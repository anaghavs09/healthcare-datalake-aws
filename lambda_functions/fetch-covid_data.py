import json
import urllib3
import boto3
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# Your S3 bucket name
BUCKET_NAME = 'healthcare-datalake-anagha'

def lambda_handler(event, context):
    """
    Fetch COVID-19 data from disease.sh API and save to S3
    """
    
    print("Starting COVID data fetch from disease.sh...")
    
    try:
        # Use disease.sh API - reliable COVID data source
        http = urllib3.PoolManager()
        
        # Get global summary data
        url = 'https://disease.sh/v3/covid-19/countries'
        
        print(f"Fetching data from: {url}")
        response = http.request('GET', url)
        
        if response.status != 200:
            raise Exception(f"Failed to fetch data. Status code: {response.status}")
        
        print(f"Data fetched successfully! Status: {response.status}")
        
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"raw/covid/disease-sh-countries_{timestamp}.json"
        
        # Upload to S3
        print(f"Uploading to S3: {filename}")
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=response.data,
            ContentType='application/json'
        )
        
        print(f"Successfully uploaded to s3://{BUCKET_NAME}/{filename}")
        
        # Verify upload
        try:
            head_response = s3.head_object(Bucket=BUCKET_NAME, Key=filename)
            file_size = head_response['ContentLength'] / 1024  # KB
            print(f"✅ Verified! File size: {file_size:.2f} KB")
        except Exception as verify_error:
            print(f"Warning: Could not verify upload: {verify_error}")
        
        # Parse to count countries
        data = json.loads(response.data.decode('utf-8'))
        country_count = len(data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'COVID data successfully fetched and stored',
                'filename': filename,
                'countries': country_count,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error fetching COVID data',
                'error': str(e)
            })
        }
