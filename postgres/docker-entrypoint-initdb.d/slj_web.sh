#!/bin/env bash
psql -U postgres -c "CREATE USER  PASSWORD ''"
psql -U postgres -c "CREATE DATABASE  OWNER "
