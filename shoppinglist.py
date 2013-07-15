import sqlite3
import thursday


# singleton -- 1-1 correspondence to ShoppingList table
class ShoppingList:
   
   def __init__( self ):
	  self.inStock = []
	  self.toBuy = []
	  self.requested = []


	  self.cursor = thursday.connect_db()

	  rst = self.cursor.execute( "SELECT status, item_name, quantity  FROM  ShoppingList")
	  
	  # go through all the rows in ShoppingList and bucket the results
	  # based on the status column
   	  for row in rst:
		 bucket = row[0] 
		 item = {
			"item_name": row[1],
			"quantity": row[2]
		 }

		 if str(bucket) == "inStock":
			self.inStock.append( item )
		 elif str(bucket) == "toBuy":
			self.toBuy.append( item )
		 elif str(bucket) == "requested":
			self.requested.append( item )
		 

		 print item



   
   
   # add a given item to the SHoppingList in the datbase
   # values -- a dictionary with at least the following keys
   #  item_name
   #  quantity
   #  status
   def add( self,values ):
	  conn = thursday.connect_db()
	  cursor = conn.cursor()
	  query = "INSERT INTO ShoppingList(item_name, quantity, status) VALUES( :item_name, :quantity, :status)"
	  cursor.execute( query , values )
	  conn.commit()
	  conn.close()

	  # TODO this should alter the actual object as well as the database

	   
	     
	       
   
	  

	  
    
