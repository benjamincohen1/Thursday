drop table if exists events;
CREATE TABLE "events" (
	"id" INTEGER PRIMARY KEY  NOT NULL ,
	 "event" VARCHAR NOT NULL ,
	 "day" INTEGER NOT NULL ,
	 "month" INTEGER NOT NULL ,
	 "year" INTEGER NOT NULL )