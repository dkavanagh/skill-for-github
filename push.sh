#!/bin/bash
flake8 github-skill.py --max-line-length=120
if [ $? -ne 0 ]; then
    echo "fix the error first"
    exit -1
fi
rm ../github-skill.zip
zip ../github-skill.zip github-skill.py github/*
aws lambda update-function-code --function-name arn:aws:lambda:us-east-1:721404732763:function:github-skill --zip-file fileb://../github-skill.zip
