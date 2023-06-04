# Todo-App

This project contains source code and supporting files for a todo list serverless application that is managed with AWS Serverless Application Model (SAM) and can use the SAM CLI to deploy the application. 

It includes the following files and folders.

- `src/` - source  ode for the application's Lambda functions.
- `template.yaml` - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Project Summary

This todo list application is a rest API for a todo list application. It is built using serverless technologies in complete native AWS services. 

The todo list API allows you to:

- create new todos
- get existing todo
- update existing todos
- list all todos (incl. archived ones)
- delete existing todos
- archived todos
- mark todos as done

## Architecture

![todolist](https://github.com/prateek2103/Todo-app-using-SAM/assets/30109806/a749536c-e86a-46e2-90fb-1f51af83fcd3)

## API Guide

This section provides in-depth guide on the APIs.
### Create new Todos

To create new todos, make a post request to:

e.g.
```bash
curl -X POST -d '{"title": "todo title", "content": "the content"}' http://{todo-list-api}/todo-list/create
```

### Get Todo

```bash
curl http://{todo-list-api}/todo-list/{item_id}
```

### Update existing Todo

To update existing todos, make the following request:

e.g.

```bash
curl -X PUT -d '{"item_id": "e99b8e6d-40a0-11eb-8288-3be6f58d0c20", "title": "updated title", "content": "updated content"}' http://{todo-list-api}/todo-list/update
```

### List all Todos

To fetch all the todos;

```bash
curl http://{todo-list-api}/todo-list/list-todos
```

### Delete existing Todos

Todos are not permanently deleted. They are marked as 'deleted' with the `is_deleted` flag set to `true`. 

To delete a todo you need to 'mark' it as "deleted" first by hitting the delete endpoint:

```bash
curl -X DELETE http://{todo-list-api}/todo-list/delete/{item_id}
# where item_id = the id of the todo item you want to delete
```

This request doesn't delete the todo but instead request for the todo to be deleted by sending a request to a backend queue (SQS) for delete processing. The delete queue triggers a mark deletion when the queue messages hit a certain threshold thereby trigger a CloudWatch Alarm which in term sends a notification to the topic (SNS Topic). A lambda subscription then triggers the actual delete lambda function to do the actual "mark deletion".

Overall, the todo stays within the DynamoDB table without ever being permanently removed.

### Archive Todos

When archiving the todo, it marks the todo item as "archived" with the `is_archived` flag set to `true` for the todo item and send a csv file equivalent of the todo to a S3 bucket that stores the archives.

```bash
curl -X POST http://{todo-list-api}/todo-list/archive/{item_id}

# where item_id is the id of the todo item
```

### Mark Todos as Done

When marking a todo as "Done", make a request like the following:

```bash
curl -X POST http://{todo-list-api}/todo-list/complete/{item_id}

# where item_id is the id of the todo item
```

When 'completing' the todo we just mark it as "Complete" by setting the `is_done` flag of the todo item to `true`.

## Tech Stack

- SAM
- Lambda
- API Gateway
- DynamoDB
- S3
- SQS
- SNS
- Systems Manager
  - Parameter Store (SSM)
- CloudWatch
  - CloudWatch Alarms

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Cleanup
A shell script (destroy.sh) is provided to delete all the resources so that you don't incur any costs unnecessarily.
