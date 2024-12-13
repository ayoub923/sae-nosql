# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:16:23 2024

@author: ayoub
"""

# Importation des modules utilisés
import sqlite3
import pandas

# Création de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# Récupération du contenu de Customers avec une requête SQL
customers = pandas.read_sql_query("SELECT * FROM Customers;", conn)
print(customers)


# Lister les clients n'ayant jamais fait de commande 
   


#nocom = pandas.read_sql_query("SELECT * from ORDERS join Customers WHERE customerNumber IS NULL;",conn)
#print(nocom)



# QUESTION 2 

#Pour chaque employé, le nombre de clients, le nombre de commandes et le montant total de celles-ci ;

employe = pandas.read_sql_query("""
                               SELECT 
                                   e.employeeNumber ,
                                   e.firstName ,
                                   e.lastName ,
                                   COUNT(DISTINCT c.customerNumber) AS numberofcustomers,                
                                   COUNT(DISTINCT o.orderNumber) AS numberoforders,
                                   SUM(p.amount) AS totalamount 
                               
                               from Employees e
                               left join Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                               left join orders o ON c.customerNumber = o.customerNumber
                               left join payments p on o.customerNumber = p.customerNumber
                               GROUP BY e.employeeNumber, e.firstName, e.lastName;
                               """,
                               conn)
print(employe)
                               
                               
                               
                               
# QUESTION 4

q4 = pandas.read_sql_query      ("""
                                 SELECT 
                                     P.productName, 
                                     COUNT(DISTINCT OD.orderNumber) AS numberOfOrders, 
                                     SUM(OD.quantityOrdered) AS totalQuantityOrdered,
                                     COUNT(DISTINCT O.customerNumber) AS numberOfCustomers
                                     
                                FROM OrderDetails OD
                                JOIN Orders O ON OD.orderNumber = O.orderNumber
                                JOIN Products P ON OD.productCode = P.productCode
                                GROUP BY P.productName
                                ORDER BY P.productName;

                                 """,conn)      
                                 
                                 
print(q4)
                              

# customers 
# question 6 

q6 = pandas.read_sql_query ("""
                            SELECT
                                P.productLine, 
                                C.country, 
                                COUNT(O.orderNumber) AS numberOfOrders
                            FROM Orders O
                            JOIN Customers C ON O.customerNumber = C.customerNumber
                            JOIN OrderDetails OD ON O.orderNumber = OD.orderNumber
                            JOIN Products P ON OD.productCode = P.productCode
                            GROUP BY P.productLine, C.country
                            ORDER BY P.productLine, C.country;
                            
                            """,conn)
                            
print(q6)




q8 =pandas.read_sql_query(""" 
                          SELECT 
                              P.productName, 
                              AVG(OD.priceEach - P.buyPrice) AS averageMargin
                          FROM OrderDetails OD
                          JOIN Products P ON OD.productCode = P.productCode
                          GROUP BY P.productName
                          ORDER BY averageMargin DESC
                          LIMIT 10;
                          """,conn)
print(q8)



q10 = pandas.read_sql_query("""
    SELECT 
        c.customerNumber,
        c.customerName,
        SUM(od.quantityOrdered * od.priceEach) AS totalOrderAmount,
        SUM(p.amount) AS totalPaidAmount
    FROM Customers c
    LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
    LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
    LEFT JOIN Payments p ON c.customerNumber = p.customerNumber
    GROUP BY c.customerNumber, c.customerName
    HAVING SUM(p.amount) > SUM(od.quantityOrdered * od.priceEach);
""", conn)


pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)  # Assure une largeur d'affichage suffisante
pandas.set_option('display.max_colwidth', None)
# Afficher les résultats obtenus
print(q10)

# Fermeture de la connexion : IMPORTANT à faire dans un cadre professionnel
conn.close()