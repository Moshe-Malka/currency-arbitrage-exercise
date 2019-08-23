# currency-arbitrage-exercise

**prerequisites :**
- [Python 3.7.X](https://www.python.org/downloads/ "Python 3.7.X")
- [NPM](https://nodejs.org/en/ "NPM")
- [Serverless Framework](https://serverless.com/ "Serverless Framework")
- [AWS Account](https://aws.amazon.com/ "AWS Account")
- Optional:
[AWS CLI](https://aws.amazon.com/cli/ "AWS CLI")

**Installation :**
1. `git clone https://github.com/Moshe-Malka/currency-arbitrage-exercise.git`
2. `cd currency-arbitrage-exercise && npm install`
3. setup a user in your AWS account and in cmd type
4. `serverless config credentials --provider aws --key <user key> --secret <user secret> --profile <profile name>`
5. change profile name in serverless.yml to the name you choose above.
6. manually load broker file to S3:
if AWS CLI installd - `aws s3 cp brokers.json s3://currency-arbitrage-brokers/brokers.json`
Otherwise - load file through AWS Console Management.
8. `sls deploy`


**Invoking Localy :**

------------

Data Collection Service:
- `sls invoke local --function DataCollection`
- `sls invoke local --function DataCollection --path test/mock_data_collection.json`

Exchange Rates Retrieval Service:
- `sls invoke local --function ExRatesRetrieval`
- `sls invoke local --function ExRatesRetrieval --path test/mock_ex_rates_retrieval_with_date.json`
- `sls invoke local --function ExRatesRetrieval --path test/mock_ex_rates_retrieval.json`

Exchange Path Recommendation Service:
- `sls invoke local --function ExPathRecommendation`
- `sls invoke local --function ExPathRecommendation --path test/mock_ex_path_recommendation.json`

**Deploying:**

------------
`sls deploy`