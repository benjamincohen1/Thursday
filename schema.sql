drop table if exists events;
CREATE TABLE `events` (
	`id` INTEGER PRIMARY KEY  NOT NULL ,
	 `event` VARCHAR NOT NULL ,
	 `day` INTEGER NOT NULL ,
	 `month` INTEGER NOT NULL ,
	 `year` INTEGER NOT NULL,
	 `big` BOOLEAN);


drop table if exists users;
CREATE TABLE `users` (
	`id` INTEGER PRIMARY KEY  NOT NULL , 
	`username` VARCHAR NOT NULL  UNIQUE , 
	`password` VARCHAR NOT NULL , 
	`admin` BOOL NOT NULL  DEFAULT False);


INSERT INTO Users( username, password, admin ) VALUES
   ("Ben", "5f4dcc3b5aa765d61d8327deb882cf99", "true" ),
   ("Lee", "5f4dcc3b5aa765d61d8327deb882cf99", "true" );


DROP TABLE IF EXISTS ShoppingList;
CREATE TABLE ShoppingList (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   item_name STRING NOT NULL,
   quantity INTEGER NOT NULL,
   status string NOT NULL
);
DROP TABLE IF EXISTS bar;
CREATE TABLE bar(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	item_name STRING NOT NULL,
	size STRING NOT NULL,
	quantity INTEGER NOT NULL DEFAULT 0,
	owner VARCHAR NOT NULL,
	FOREIGN KEY(owner) REFERENCES users(username)

);
