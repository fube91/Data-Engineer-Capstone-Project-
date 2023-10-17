SELECT * FROM creditcard_capstone.cdw_sapp_branch;
SELECT * FROM creditcard_capstone.cdw_sapp_credit_card;
SELECT * FROM creditcard_capstone.cdw_sapp_customer;

creditcard visualization sql

/*Find and plot which transaction type has the highest transaction count. */
SELECT TRANSACTION_TYPE, COUNT(*) AS transaction_count
FROM cdw_sapp_credit_card
GROUP BY TRANSACTION_TYPE
ORDER BY transaction_count DESC

/*Find and plot which state has a high number of customers. */
SELECT CUST_STATE, COUNT(SSN) AS number_of_customers
FROM cdw_sapp_customer
GROUP BY CUST_STATE
ORDER BY number_of_customers DESC

/*Find and plot the sum of all transactions for the top 10 customers, and which customer has the highest transaction amount. */
SELECT cc.CUST_SSN, c.FIRST_NAME, c.LAST_NAME, SUM(cc.TRANSACTION_VALUE) AS total_transaction_amount
FROM cdw_sapp_credit_card cc
INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN
GROUP BY cc.CUST_SSN, c.FIRST_NAME, c.LAST_NAME
ORDER BY total_transaction_amount DESC
LIMIT 10

Loan application visualization sql

/* Percentage of applications approved for self-employed applicants */
SELECT Application_Status, Self_Employed, COUNT(*) as count
FROM cdw_sapp_loan_application
WHERE Self_Employed = 'Yes'
GROUP BY Application_Status, Self_Employed;

/* Percentage of rejection for married male applicants */
SELECT Application_Status, COUNT(*) as count
FROM cdw_sapp_loan_application
WHERE Married = 'Yes' AND Gender = 'Male'
GROUP BY Application_Status;

/* Top three months with the largest volume of transaction data */
SELECT 
    SUBSTRING(TIMEID, 1, 4) AS year, 
    SUBSTRING(TIMEID, 5, 2) AS month,  
    SUM(transaction_value) AS total 
FROM cdw_sapp_credit_card 
GROUP BY year, month
ORDER BY total DESC 
LIMIT 3;

/*Branch with highest total dollar value of healthcare transactions*/
SELECT BRANCH_CODE, 
       SUM(transaction_value) AS Total_Transaction_Value
FROM cdw_sapp_credit_card 
WHERE TRANSACTION_TYPE = 'healthcare' 
GROUP BY BRANCH_CODE 
ORDER BY Total_Transaction_Value DESC 
LIMIT 1;
