#!/bin/bash


mysql -u$1 -p$2 -e "create database $3 character set utf8 collate utf8_general_ci;"
mysql -u$1 -p$2 -e "grant all on $3.* to '$4'@'localhost' identified by '$5';"