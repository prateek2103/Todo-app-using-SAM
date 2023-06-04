#!/bin/bash
aws s3 rb s3://todo-list-archive-bucket --force
aws cloudformation delete-stack --stack-name todo-app