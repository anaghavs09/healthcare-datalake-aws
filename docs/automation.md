# Lambda Automation Configuration

## EventBridge Trigger

**Trigger Name:** daily-covid-data-collection  
**Type:** Schedule expression  
**Schedule:** rate(1 day) - Runs every 24 hours  
**Target:** Lambda function `fetch-covid-data`  
**Status:** Enabled ✅

## What Happens Automatically

1. EventBridge triggers Lambda every 24 hours
2. Lambda fetches COVID data from disease.sh API (227 countries)
3. Data saved to S3: `s3://healthcare-datalake-anagha-2024/raw/covid/`
4. Filename format: `disease-sh-countries_YYYY-MM-DD_HH-MM-SS.json`
5. CloudWatch logs execution results

## Monitoring

- **CloudWatch Logs:** Lambda execution logs
- **S3 Bucket:** Check `raw/covid/` for new files daily
- **Lambda Metrics:** Invocations, duration, errors

