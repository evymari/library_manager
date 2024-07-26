from config.DBConnection import DBConnection

myConnection=DBConnection()
print(myConnection.execute_query("SELECT * FROM books"))

