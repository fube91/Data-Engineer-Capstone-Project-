#pip install mysql.connector
#pip install mysql-connector-python
#pip install credentials
from credentials import mysql_username, mysql_password
import mysql.connector
import pymysql
import credentials

# Setup database connection
conn = pymysql.connect(host='localhost', user=mysql_username, password=mysql_password, database='creditcard_capstone')
cursor = conn.cursor()


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

def check_account_details(ssn):
    query = "SELECT * FROM cdw_sapp_customer WHERE SSN = %s"
    cursor.execute(query, (ssn,))
    details = cursor.fetchone()
    if details:
        print("Account details: ", details)
    else:
        print("No details found for the given SSN.")

def modify_account_details(ssn):
    new_address = input("Enter new address: ")
    query = "UPDATE cdw_sapp_customer SET ADDRESS = %s WHERE SSN = %s"
    cursor.execute(query, (new_address, ssn))
    conn.commit()
    print("Address updated successfully.")

def generate_monthly_bill(cc_no, month, year):
    query = """
            SELECT SUM(TRANSACTION_VALUE) 
            FROM cdw_sapp_credit_card 
            WHERE CUST_CC_NO = %s AND TIMEID LIKE %s
            """
    cursor.execute(query, (cc_no, f'{year}-{month}%'))
    bill = cursor.fetchone()[0]
    print(f"Monthly bill for card {cc_no} for {month}/{year}: {bill}")

def display_transactions_by_dates(ssn, start_date, end_date):
    query = """
            SELECT * FROM cdw_sapp_credit_card 
            WHERE CUST_SSN = %s AND TIMEID BETWEEN %s AND %s
            ORDER BY TIMEID DESC
            """
    cursor.execute(query, (ssn, start_date, end_date))
    for row in cursor:
        print(row)

if __name__ == "__main__":
    
    # Simple console menu
    while True:
        print("1: Display transactions by zip code for a month and year.")
        print("2: Display number and total values for a transaction type.")
        print("3: Display number and total values for branches in a state.")
        print("4: Check account details of a customer.")
        print("5: Modify account details of a customer.")
        print("6: Generate monthly bill for a card number.")
        print("7: Display transactions for a card number between two dates.")
        print("8: Exit.")
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

        if choice == "4":
            customer_ssn = input("Enter customer SSN: ")
            check_account_details(customer_ssn)

        elif choice == "5":
            customer_ssn = input("Enter customer SSN: ")
            modify_account_details(customer_ssn)
            print("Account details modified successfully!")

        elif choice == "6":
            card_no = input("Enter credit card number: ")
            month = input("Enter month (in format MM): ")
            year = input("Enter year (in format YYYY): ")
            generate_monthly_bill(card_no, month, year)

        elif choice == "7":
            customer_ssn = input("Enter customer SSN: ")
            start_date = input("Enter start date (in format YYYY-MM-DD): ")
            end_date = input("Enter end date (in format YYYY-MM-DD): ")
            display_transactions_by_dates(customer_ssn, start_date, end_date)

        elif choice == "8":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    conn.close()
