#!/bin/bash
psql -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"
psql -U postgres -c 'CREATE TABLE "public"."tbl_web_page" ("id" serial NOT NULL,"title" varchar NOT NULL,"ptime" varchar(32) ,"images" varchar NOT NULL,"likes" int4 DEFAULT 0,"visits" int4 DEFAULT 0,"link" varchar,CONSTRAINT "tbl_web_page_pk" PRIMARY KEY ("id")) WITH (IDS=FALSE); ALTER TABLE "public"."tbl_web_page" OWNER TO "slj_web";'
