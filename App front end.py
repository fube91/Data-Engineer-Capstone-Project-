#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install mysql-connector-python')
get_ipython().system('pip install sqlalchemy mysql-connector-python')
import pymysql
import mysql.connector
from mysql.connector import Error
import mysql.connector
from credentials import mysql_username, mysql_password


# In[20]:


import pymysql

# Setup database connection
conn = pymysql.connect(host='localhost', user=mysql_username, password=mysql_password, database='creditcard_capstone')
cursor = conn.cursor()


# In[21]:


def display_transactions(zip_code, month, year):
    query = ("""
            SELECT cc.TIMEID, cc.TRANSACTION_VALUE, cc.TRANSACTION_TYPE, cc.CUST_CC_NO,
            c.FIRST_NAME, c.LAST_NAME, cc.BRANCH_CODE, cc.TRANSACTION_ID
            FROM cdw_sapp_credit_card cc
            INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN
            WHERE c.CUST_ZIP = %s AND cc.TIMEID LIKE %s
            ORDER BY cc.TIMEID DESC
            """)
    cursor.execute(query, (zip_code, f'{year}-{month}%'))
    for row in cursor:
        print(row)

def display_values_for_transaction_type(transaction_type):
    query = ("""
            SELECT TRANSACTION_TYPE, COUNT(TRANSACTION_TYPE), SUM(TRANSACTION_VALUE)
            FROM cdw_sapp_credit_card
            WHERE TRANSACTION_TYPE = %s
            GROUP BY TRANSACTION_TYPE
            """)
    cursor.execute(query, (transaction_type,))
    result = cursor.fetchone()
    print(f"Number of {transaction_type} transactions: {result[1]}")
    print(f"Total value of {transaction_type} transactions: {result[2]}")

def display_values_for_branch_state(state):
    query = ("""
            SELECT COUNT(*), SUM(TRANSACTION_VALUE) 
            FROM cdw_sapp_credit_card 
            WHERE BRANCH_CODE IN 
            (SELECT BRANCH_CODE FROM cdw_sapp_branch WHERE BRANCH_STATE = %s)
            """)
    cursor.execute(query, (state,))
    result = cursor.fetchone()
    print(f"Number of transactions in state {state}: {result[0]}")
    print(f"Total value of transactions in state {state}: {result[1]}")

if __name__ == "__main__":
    # ... (The rest of your code remains unchanged)
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        port='3306',
        user= mysql_username,
        password= mysql_password,
        database='creditcard_capstone'
    )
    cursor = conn.cursor()

    # Simple console menu
    while True:
        print("1: Display transactions by zip code for a month and year.")
        print("2: Display number and total values for a transaction type.")
        print("3: Display number and total values for branches in a state.")
        print("4: Exit.")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            zip_code = input("Enter zip code: ")
            month = input("Enter month: ")
            year = input("Enter year: ")
            display_transactions(zip_code, month, year)
        elif choice == "2":
            transaction_type = input("Enter transaction type: ")
            display_values_for_transaction_type(transaction_type)
        elif choice == "3":
            state = input("Enter state: ")
            display_values_for_branch_state(state)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    conn.close()

