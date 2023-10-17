# Data-Engineer-Capstone-Project-
Per Scholas DE Capstone

This Capstone Project requires working with the following technologies to manage an ETL process for a Loan Application dataset and a Credit Card dataset: Python (Pandas, advanced modules, e.g., Matplotlib), SQL, Apache Spark (Spark Core, Spark SQL), and Python Visualization and Analytics libraries. 

Based on the workflow diagram provided, one is expected to do the following:
Extraction Phase (E): Data from various sources (like CDW_SAPP_CUSTOMER, CDW_SAPP_CREDITCARD, and CDW_SAPP_BRANCH) are extracted as JSON files.

API & Transformation Phase (T): Data from the CDW_SAPP_LOAN is exposed via a Data API Endpoint, which is consumed by a Python Rest API. This data, along with the extracted data from the aforementioned sources, is processed by Apache Spark (PySpark) for transformation.

Load Phase (L): The transformed data is then loaded into a database.

Consumption Phase: Once loaded into the database, the data can be accessed and processed by various means:

Through a Python program, presumably for further data processing or manipulation (as indicated by the path labeled C).
For data analysis and visualization (as indicated by the path labeled D).

![Alt text](image-1.png)