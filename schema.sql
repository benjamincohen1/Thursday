drop table if exists events;
CREATE TABLE "events" (
	"id" INTEGER PRIMARY KEY  NOT NULL ,
	 "event" VARCHAR NOT NULL ,
	 "day" INTEGER NOT NULL ,
	 "month" INTEGER NOT NULL ,
	 "year" INTEGER NOT NULL );
drop table if exists karma;
CREATE TABLE "users" (
	"id" INTEGER PRIMARY KEY  NOT NULL , 
	"username" VARCHAR NOT NULL  UNIQUE , 
	"password" VARCHAR NOT NULL , 
	"admin" BOOL NOT NULL  DEFAULT False);
