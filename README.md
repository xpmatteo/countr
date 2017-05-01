
Purpose: learn Python and Flask.

This is a simple REST service created with Flask.

## Instructions:

Install Python dependencies with

    pip install flask
    pip install pymysql

    # for tests only
    pip install bs4

    # for eb deployments
    pip install --upgrade awsebcli

Prepare the (local) databases with

    script/create-local-databases.sh

(Make sure you have a local mysql running first.)

See it running with

    script/run-local.sh
    open http://localhost:5000/

Run unit tests with

    pytest

Run individual test with

    python tests/(filename)

## Docker stuff

Prepare the requirements.txt file with

    pip install pipreqs
    pipreqs . --force

Build docker container: (-t is for tagging the image)

    docker build -t countr:latest .

Run with docker: (-i -t is for being able to kill it with ^C)

    docker run -i -t -p 5000:5000 countr:latest

## Deploying to Elastic Beanstalk

Assuming you created an EB app and env, you can deploy to them with

    script/deploy.sh



