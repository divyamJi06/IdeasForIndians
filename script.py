import base64
import requests
import json

def edit_and_commit_file(username, repository, file_path, branch, token, new_content, commit_message, typeOfData, idea_id=1):
    try:
        # Fetch the current content of the file
        current_content = get_github_file_contents(username, repository, file_path, branch, token)

        # Load the current content as JSON
        current_data = json.loads(current_content)

        # Assuming current_data is a list of maps (dictionaries)
        if not isinstance(current_data, list):
            raise ValueError("Error: The current content is not a list of maps.")

        if typeOfData == "newidea":
            print("Creating new idea")
            modified_content = addIdea(current_data, new_content)
        else:
            print("Creating new suggestion")
            modified_content = add_suggestion(current_data, idea_id, new_content)
        modified_content = json.dumps(modified_content, indent=2)

        # Create a new commit
        commit_sha = create_commit(username, repository, file_path, branch, token, modified_content, commit_message)

        print(f"File edited and committed successfully. Commit SHA: {commit_sha}")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def addIdea(ideas, new_idea):
    try:
        new_idea_id = max(idea['id'] for idea in ideas) + 1 if ideas else 1

        # Add the new idea with the calculated ID
        new_idea['id'] = new_idea_id
        ideas.append(new_idea)
        return ideas

    except Exception as e:
        print(f"Error in adding new idea: {e}")
        raise

def add_suggestion(ideas, idea_id, new_suggestion):
    try:
        # Find the idea with the specified ID
        idea = next((i for i in ideas if i['id'] == idea_id), None)

        if idea:
            # Calculate the next available suggestion ID for the idea
            new_suggestion_id = max(suggestion['id'] for suggestion in idea['suggestions']) + 1 if idea['suggestions'] else 1

            # Add the new suggestion with the calculated ID
            new_suggestion['id'] = new_suggestion_id
            idea['suggestions'].append(new_suggestion)

            print(f'Suggestion added successfully to Idea {idea_id} with ID: {new_suggestion_id}')
            return ideas
        else:
            raise ValueError(f'Idea with ID {idea_id} not found.')

    except Exception as e:
        print(f'Error in adding new suggestion: {e}')
        raise

def get_github_file_contents(username, repository, file_path, branch, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/contents/{file_path}?ref={branch}'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for errors

        # Decode content from base64 and load JSON
        decoded_content = base64.b64decode(response.json()['content']).decode('utf-8')
        print(f"Fetched the data from branch {branch}")

        return decoded_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching file from GitHub: {e}")
        raise

def create_commit(username, repository, file_path, branch, token, new_content, commit_message):
    try:
        # Get the latest commit SHA from the specified branch
        latest_commit_sha = get_latest_commit_sha(username, repository, branch, token)

        # Get the tree SHA associated with the latest commit
        tree_sha = get_tree_sha(username, repository, latest_commit_sha, token)

        # Create a new tree with the modified file content
        new_tree_sha = create_new_tree(username, repository, tree_sha, file_path, new_content, token)

        # Create a new commit with the updated tree
        new_commit_sha = create_new_commit(username, repository, latest_commit_sha, new_tree_sha, commit_message, token, branch)

        return new_commit_sha

    except Exception as e:
        print(f"Error creating commit: {e}")
        raise

def get_latest_commit_sha(username, repository, branch, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/commits/{branch}'

        headers = {
            'Authorization': f'token {token}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for errors
        print("Fetched the latest commit")
        print(response.json()['sha'])

        return response.json()['sha']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest commit SHA from GitHub: {e}")
        raise

def get_tree_sha(username, repository, commit_sha, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/commits/{commit_sha}'

        headers = {
            'Authorization': f'token {token}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for errors
        print("Got the tree SHA")
        print(response.json()['commit']['tree']['sha'])
        return response.json()['commit']['tree']['sha']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching tree SHA from GitHub: {e}")
        raise

def create_new_tree(username, repository, base_tree_sha, file_path, new_content, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/git/trees'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = {
            'base_tree': base_tree_sha,
            'tree': [
                {
                    'path': file_path,
                    'mode': '100644',  # Blob mode
                    'content': new_content
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check for errors
        print("Created Tree")
        print(response.json()['sha'])
        return response.json()['sha']

    except requests.exceptions.RequestException as e:
        print(f"Error creating new tree on GitHub: {e}")
        raise

def create_new_commit(username, repository, parent_commit_sha, new_tree_sha, commit_message, token, branch):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/git/commits'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = {
            'message': commit_message,
            'parents': [parent_commit_sha],
            'tree': new_tree_sha
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check for errors
        print("Created new Commit")
        print(response.json()['sha'])

        # Update the reference (branch) to point to the new commit
        update_branch_reference(username, repository, branch, response.json()['sha'], token)

        return response.json()['sha']

    except requests.exceptions.RequestException as e:
        print(f"Error creating new commit on GitHub: {e}")
        raise

def update_branch_reference(username, repository, branch, new_commit_sha, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/git/refs/heads/{branch}'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = {
            'sha': new_commit_sha
        }

        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()  # Check for errors
        print(f"Updated {branch} branch reference to new commit")
        create_pull_request(username,repository,"master", branch, "Merge the new idea" , "New Idea/suggestion added", token)

    except requests.exceptions.RequestException as e:
        print(f"Error updating branch reference on GitHub: {e}")
        raise

def create_pull_request(username, repository, base_branch, compare_branch, title, body, token):
    try:
        url = f'https://api.github.com/repos/{username}/{repository}/pulls'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = {
            'title': title,
            'body': body,
            'head': compare_branch,
            'base': base_branch
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check for errors
        print("Pull request created successfully!")
        print(response.status_code)
        print(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error creating pull request on GitHub: {e}")
        # raise
