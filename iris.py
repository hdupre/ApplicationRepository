import mysql.connector as mc
import pandas as pd
import numpy as np
import unittest
from sklearn import datasets as ds

def main():
    # Usage example. 
     
    #Change get_credentials() with your password.
    creds = get_credentials()
    iris = Iris(creds) # Create a MySQL database called data602
    iris.load() # Load Iris data from sklearn and pump it into IRIS_DATA table
    iris.display_gt(140) # Display to the screen all rows with ID greater than 140
    
    iris2 = Iris(creds,dbname='anotherone') # Creates a 2nd MySQL database called anotherone, you now have 2 databases (one server still, tho)
    iris2.load() # Load Iris data
    iris2.del_observations([0,1,2]) # Delete observations that have id equal to 0, 1 or 2

    iris.update_observation(0,'stuff',5) # Change observation id 0 to a different label

    iris.close() # Close connection
    iris2.close() # Close connection

# Change password
def get_credentials():
    return {'user':'root','password':'********'}

class Iris:
    def __init__(self,creds,dbname='data602',new=True):
        self.__conn = mc.connect(host='127.0.0.1', user=creds['user'],passwd=creds['password']) # connect and store the connection object 
        self.__dbname = dbname # store the database name
        self.cursor = self.__conn.cursor()

        if new:
            # if new, create database / table
            self.__create()
            
        else:
            # else make sure to USE the right database
            self.cursor.execute("USE " + self.__dbname)


    # Drop the database and create a new one with a new table
    def __create(self):


        self.cursor.execute("DROP DATABASE IF EXISTS " + self.__dbname)
        self.cursor.execute("CREATE DATABASE " + self.__dbname)
        self.cursor.execute("USE " + self.__dbname)
        self.cursor.execute("CREATE TABLE IRIS_DATA(id INT NOT NULL, feature_sepal_length FLOAT NOT NULL, feature_sepal_width FLOAT NOT NULL, feature_petal_length FLOAT NOT NULL, feature_petal_width FLOAT NOT NULL, target_species VARCHAR(255) NOT NULL, target_species_id INT NOT NULL)")
        print("Database and IRIS table created in DB " + self.__dbname)


    # Close connection
    def close(self):

        self.__conn.close()

        print('Disconnected')

    # Loop the Iris data and INSERT into the IRIS_DATA table
    def load(self,truncate=False):
        if truncate:

            self.__truncate_iris()
            self.load(truncate=False)

            print('Iris table truncated')

        else:
            iris_data = ds.load_iris()
            target_names = list(iris_data.target_names)
            df = pd.DataFrame(np.c_[iris_data['data'], iris_data['target']], columns= np.append(iris_data['feature_names'], ['target']))
            for index, row in df.iterrows():
                insert = ("INSERT INTO IRIS_DATA "
                        "(id, feature_sepal_length, feature_sepal_width, feature_petal_length, feature_petal_width, target_species, target_species_id) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                row_data = (index, row['sepal length (cm)'], row['sepal width (cm)'], row['petal length (cm)'], row['petal width (cm)'], target_names[int(row['target'])], int(row['target']))
                self.cursor.execute(insert, row_data)
            self.__conn.commit()

        print('Iris dataset loaded')

    # Display all rows that have ID greater than integer n
    def display_gt(self,n): 

        select = "SELECT * FROM IRIS_DATA WHERE id > %s"
        self.cursor.execute(select, (n,))
        results = self.cursor.fetchall()
        for x in results:
            print(x)


    # Update observation with a specific id to a new target species and species id
    def update_observation(self,id,new_target_species,new_target_species_id):

        update = "UPDATE IRIS_DATA SET target_species = %s, target_species_id = %s WHERE id = %s"
        values = (new_target_species, new_target_species_id, id)
        self.cursor.execute(update,values)
        self.__conn.commit()


    # Delete all rows that are in the list row_ids    
    def del_observations(self,row_ids):

        delete = "DELETE FROM IRIS_DATA WHERE id = %s"
        for i in range(len(row_ids)):
            self.cursor.execute(delete,(row_ids[i],))
        self.__conn.commit()


    # Truncate the IRIS_DATA table
    def __truncate_iris(self):
        self.cursor.execute("TRUNCATE TABLE IRIS_DATA")


    # Establish a connection
    def __get_connection(self,creds):
        return mc.connect(user=creds['user'], password=creds['password'],
                              host='127.0.0.1',
                              auth_plugin='mysql_native_password')      

    # Returns the current row count of the IRIS_DATA table
    def get_row_count(self):
        self.cursor.execute("SELECT * FROM IRIS_DATA")
        count = len(self.cursor.fetchall())
        print("Row count is " + str(count))

        return count

