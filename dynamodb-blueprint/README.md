# To create table

aws dynamodb create-table --cli-input-json file://~/environment/dynamodb-blueprint/dynamodb-customer.json

# To populate table with sample data
aws dynamodb batch-write-item --request-items file://~/environment/dynamodb-blueprint/populate-customer.json

# to scan table
aws dynamodb scan --table-name customer
