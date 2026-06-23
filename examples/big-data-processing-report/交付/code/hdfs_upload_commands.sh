#!/bin/bash
set -e

hdfs dfs -mkdir -p /course_project/learning_data
hdfs dfs -put -f clean_learning_data.csv /course_project/learning_data/
hdfs dfs -ls /course_project/learning_data
hdfs dfs -cat /course_project/learning_data/clean_learning_data.csv | head
