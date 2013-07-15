import sqlite3
import thursday


# singleton -- 1-1 correspondence to ShoppingList table
class ShoppingList:
   
   def __init__( self ):
	  self.inStock = []
	  self.toBuy = []
	  self.requested = []


	  self.cursor = thursday.connect_db()

	  rst = self.cursor.execute( "SELECT * FROM  ShoppingList")
	  
	  for row in rst:
		 print row

   
   
   def add( self,values ):
	  conn = thursday.connect_db()
	  cursor = conn.cursor()
	  query = "INSERT INTO ShoppingList(item_name, quantity, status) VALUES( :item_name, :quantity, :status)"
	  cursor.execute( query , values )
	  conn.commit()
	  conn.close()

	   
	     
	       
   
	  

	  
    
