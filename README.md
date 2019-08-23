# currency-arbitrage-exercise


Invoking Local :
serverless invoke local --function DataCollection
serverless invoke local --function DataCollection --path test/mock_data_collection.json

serverless invoke local --function ExRatesRetrieval
serverless invoke local --function ExRatesRetrieval --path test/mock_ex_rates_retrieval_with_date.json
serverless invoke local --function ExRatesRetrieval --path test/mock_ex_rates_retrieval.json

serverless invoke local --function ExPathRecommendation
serverless invoke local --function ExPathRecommendation --path test/mock_ex_path_recommendation.json