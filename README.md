# RealEstateProjectArchitecture

![AWS Real-estate Project Architecture](https://user-images.githubusercontent.com/73848656/168917513-56982bb7-98a7-4006-892c-db930b032071.JPG)

# Explanation
This is a project I created to get familiar with AWS services. Based off the location put into the lambda function, homes for sale and disaster declarations are returned and Put into S3 bucket objects. A population dataset is downloaded from census.gov and also used in creating the final dashboard. Within the two notebooks, I cleaned, filtered, and analyzed the datasets with in spark dataframes. Then I wrote those datasets to another S3 bucket. Finally, using these filtered datasets and the census population dataset, I created a dashboard in AWS Quicksite.

# Requirements
## AWS Lambda Function
My "real-estate-data-retrieval" function uses Python 3.8

Must have execution role that allows you to Put Object in S3

Uses two layers 
  1. Pandas: arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-pandas:48
  2. Requests: arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-requests:28

## AWS Quicksite

Must have permission to Get Object from S3 (Role)

## AWS EMR
Must have permission to Put and Get Object from your S3 bucket (Policy)

Both Notebooks use a PySpark Kernel 

Both Notebooks use the Pandas Library
  sc.install_pypi_packages("pandas==0.25.0")
  
# Dashbaord (Tooltips only show in Quicksite)
![image](https://user-images.githubusercontent.com/73848656/168955267-e6c0f09e-cf9a-4e02-832d-c8e962dc269c.png)
![image](https://user-images.githubusercontent.com/73848656/168955317-b08fc146-f3c6-4c60-b436-c7abd6e65241.png)
![image](https://user-images.githubusercontent.com/73848656/168955345-d2892e6f-2ac0-45f3-890c-9aefdf198755.png)
![image](https://user-images.githubusercontent.com/73848656/168955362-05eae9f1-2b94-4689-b655-bd08d7c2617d.png)

# Ideas for the future

Make a seperate API request, for every home for sale returned, that shows similar homes in that area that have already sold. In the real-estate market these are called 'Comps'. Then filter those responses by: bedroom, bathroom, sqrft, and price sold. This could be useful if you want to purchase a home for a lower price because it has less (beds, baths, sqrft) then another home that has sold for much less or it could be useful for selling a home for a higher price because it has more (beds, baths, sqrft) then another home that has sold for more.
