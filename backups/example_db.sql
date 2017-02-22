--- Manually create mock database for SQLite3 
-- You can use .dump command to export complete database in a text file using SQLite command at command prompt as follows:
-- $sqlite3 testDB.db .dump > testDB.sql
-- The opposite: 
-- $sqlite3 testDB.db < testDB.sql



PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	description VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO "role" VALUES(1,'user','The typical user ');
INSERT INTO "role" VALUES(2,'superuser','e.g. Administrator');
INSERT INTO "role" VALUES(3,'ultrauser','mega admin');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	first_name VARCHAR(255), 
	last_name VARCHAR(255), 
	email VARCHAR(255), 
	password VARCHAR(255), 
	share_favourites INTEGER DEFAULT '1', 
	active BOOLEAN, 
	confirmed_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	CHECK (active IN (0, 1))
);
INSERT INTO "user" VALUES(1,'Adminius Ivan Asen','Kirov','admin','$pbkdf2-sha512$25000$7J0z5jwHIARAiBECAMCYkw$VUQ9EO.vXJJJEA5Nlgdz/gKTLGOqc3kDzupxU00EiZjKHkxtD1.KmMc.Pk9kUYBkqZxLGKGf.ui0QNYo7MtlhA',0,1,NULL);
INSERT INTO "user" VALUES(2,'Harry','Brown','harry.brown@batko.com','$pbkdf2-sha512$25000$NeYco9Q6p7T2fk/JeU9pTQ$iFDk6cPEg9zcD1LLCF6TR1GkgAanz4kTywFpdA.Tm4.JwAB4JYHXfCw0XQmq31fuI0Kiwn5irZIKLZq6F2f89Q',1,1,NULL);
INSERT INTO "user" VALUES(3,'Amelia','Smith','amelia.smith@batko.com','$pbkdf2-sha512$25000$c04pZcy5F4JwrtU6hzDmnA$JEMd21EdF.V/UHSLHRXxsQmhrXKFSWRO8EyF1dCM1yPqUpnMRsjC.SyKVUGnh9z4v8KMPM78u1cZX1ABt546pA',1,1,NULL);
INSERT INTO "user" VALUES(4,'Oliver','Patel','oliver.patel@batko.com','$pbkdf2-sha512$25000$MybkfC8FYGwtRej9P6d0rg$Jh3JEHIbFc1iCkyVHgfo/lC0Te6i3hyYr3KNmdCMC9Cl4YsIZ9rwmrK2ZplynIR1ckSzxEbDjhyzhzXTmZ4I9Q',1,1,NULL);
INSERT INTO "user" VALUES(5,'Jack','Jones','jack.jones@batko.com','$pbkdf2-sha512$25000$UcqZ814rZUwppdT63xuDsA$Pg.lvro8DHCPWwbBRjdBiFo/rGUMH9fbvcgj4icBT/GTeSNvpksLb6OpUv8wk0OVlyK1iiEziy5nsuGrv6UCLw',1,1,NULL);
INSERT INTO "user" VALUES(6,'Isabella','Williams','isabella.williams@batko.com','$pbkdf2-sha512$25000$p9TaG2Ms5bzX.n.vtfZ.zw$MPHPDC/kRVNFxikVwc9GSO9.ka5fhyenzrmkZPkQKjQOGe5tuyfQfAJLtfdLI95DS7dLzS8OZyWECZ2AksAhdw',1,1,NULL);
INSERT INTO "user" VALUES(7,'Charlie','Johnson','charlie.johnson@batko.com','$pbkdf2-sha512$25000$oBQCIMR4753TOoewlnIupQ$BfV/.lmnmqKZx2Q5n29WYjfogG5aBDtyHzb2CUVjynw6g3yyAZc7ljKwbO/GI/bfzh30NrF/cLbxP1ZkO.eGOQ',1,1,NULL);
INSERT INTO "user" VALUES(8,'Sophie','Taylor','sophie.taylor@batko.com','$pbkdf2-sha512$25000$0HrvXYuxllKqVSoFwLiXEg$NhVF3zTWLEp7KPAOKcwz5JM0BdWGjtjrUHcics.WV62M6Hriu7oakSM4ZqtxSAmVUjiqyeCw23nmw8A.bDKJTA',1,1,NULL);
INSERT INTO "user" VALUES(9,'Mia','Thomas','mia.thomas@batko.com','$pbkdf2-sha512$25000$z7nXuvf.fy9lDKEU4pyzVg$bOwaUHjjfgJTKPH3pj/nJ9kbAxIgMgU8xCjEFniESbv4BOQoxxC2Fe4wFuK4JuafAlkkgzjlViV8cNHV2Khb3A',1,1,NULL);
INSERT INTO "user" VALUES(10,NULL,NULL,'ads@abv.bg','$pbkdf2-sha512$25000$uHeuNUZozVlrbW2tFQIgJA$DNRFF9Q58s49Wtc73nCvYkeJtcpUcfQetu28cKqobj5EHquRxMYzb2hkHhElC2FVM8GrFpZcJODU470gD0Hf7g',1,1,NULL);
INSERT INTO "user" VALUES(11,NULL,NULL,'ro@abv.bg','$pbkdf2-sha512$25000$wtgbA8AYgzBmjBFCCEFoLQ$EUm1hZhTsED5SVFi.hcSYl/fHOSZdda8E2ntIbQNipfjkdpH3/I7SZ9bBdfk55EL7ULAnBhy8JIYZXEFkUtM0A',1,1,NULL);
INSERT INTO "user" VALUES(12,'BB','BB','borislav@abv.bg','$pbkdf2-sha512$25000$C0GIMcYYI.Q8p9T6P.d8jw$BahAUeoAvs4dk8Gtl/oUYhA0hm.w8RmFuVn21h3WcypRzw8EOczpRYP.a50LYhdLQix/f85WaC0fi50w/weqbw',1,1,NULL);
INSERT INTO "user" VALUES(13,'bor','bor','bor','123',1,1,NULL);
INSERT INTO "user" VALUES(14,NULL,NULL,'borbanchev@abv.bg','$pbkdf2-sha512$25000$FuKcs7Y2JiSkVArBOIcQ4g$E.NUzrRYOKrgQMURmB6V6vKdCOuDqYjo.JnbwBuDGeWLhXgElvpOhT721.7.S5lte0/zgHXfiD6clPHoKzj6aQ',1,1,NULL);
CREATE TABLE favourites (
	id INTEGER NOT NULL, 
	author VARCHAR(100), 
	song_name VARCHAR(100), 
	pub_date DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO "favourites" VALUES(4,'aaa','aaa','2016-09-22 15:40:58.359567',13);
INSERT INTO "favourites" VALUES(7,NULL,'5','2016-09-23 12:10:17.117952',13);
INSERT INTO "favourites" VALUES(8,NULL,'5','2016-09-23 12:29:49.715696',13);
INSERT INTO "favourites" VALUES(9,NULL,'5','2016-09-23 12:29:53.414619',13);
INSERT INTO "favourites" VALUES(10,NULL,'test test','2016-09-26 12:39:09.993765',1);
INSERT INTO "favourites" VALUES(11,NULL,'aaa','2016-09-26 14:56:36.899492',12);
INSERT INTO "favourites" VALUES(12,NULL,'AAAA ','2016-09-28 08:53:15.299741',1);
CREATE TABLE roles_users (
	user_id INTEGER, 
	role_id INTEGER, 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(role_id) REFERENCES role (id)
);
INSERT INTO "roles_users" VALUES(1,1);
INSERT INTO "roles_users" VALUES(1,2);
INSERT INTO "roles_users" VALUES(2,1);
INSERT INTO "roles_users" VALUES(3,1);
INSERT INTO "roles_users" VALUES(4,1);
INSERT INTO "roles_users" VALUES(5,1);
INSERT INTO "roles_users" VALUES(6,1);
INSERT INTO "roles_users" VALUES(7,1);
INSERT INTO "roles_users" VALUES(8,1);
INSERT INTO "roles_users" VALUES(9,1);
INSERT INTO "roles_users" VALUES(13,1);
INSERT INTO "roles_users" VALUES(2,3);
COMMIT;
