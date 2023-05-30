version = 0.1
[default.deploy.parameters]
stack_name = "todo-app"
resolve_s3 = true
s3_prefix = "todo-app"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
disable_rollback = true
image_repositories = []
