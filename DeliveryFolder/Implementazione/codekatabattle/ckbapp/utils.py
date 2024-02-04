# yourapp/utils.py
def get_pushed_code(payload):
    # Extract the repository name and branch from the payload
    repo_name = payload['repository']['name']
    branch = payload['ref'].split('/')[-1]  # Extract branch name from the ref

    # Assuming the pushed code is in the 'head_commit' key
    head_commit = payload['head_commit']
    files_changed = head_commit.get('modified', []) + head_commit.get('added', [])

    # Read and concatenate the content of changed/added files
    pushed_code = ""
    for file_path in files_changed:
        # Fetch file content using GitHub API or clone the repository and read the file
        # Replace this with your actual code to retrieve file content
        # Example using PyGithub:
        # content = repo.get_contents(file_path, ref=branch).decoded_content.decode('utf-8')
        # pushed_code += content

        # For demonstration purposes, we'll assume you have a 'get_file_content' function
        # that fetches file content from a local repository. Implement this function accordingly.
        content = get_file_content(repo_name, branch, file_path)
        pushed_code += content

    return pushed_code


# yourapp/utils.py
def get_file_content(repo_name, branch, file_path):
    # Replace this with your actual implementation
    # Example: read file content from a local repository
    file_full_path = f'/path/to/your/local/repository/{repo_name}/{branch}/{file_path}'
    with open(file_full_path, 'r') as file:
        content = file.read()
    return content
