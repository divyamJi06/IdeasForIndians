from script import edit_and_commit_file
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

github_username = os.getenv("GITHUB_USERNAME")
repository_name = os.getenv("REPO_NAME")
github_token = os.getenv("GITHUB_TOKEN")
file_path = os.getenv("FILE_PATH")
branch = os.getenv("BRANCH")

new_content = 'This is the new content.'
commit_message = 'Updated file with new '


def createCommit( typeOfData, new_idea_data= None,new_suggestion_data = None,idea_id = None):


    if typeOfData == "newidea":
        edit_and_commit_file(github_username, repository_name, file_path, "ideas", github_token, new_idea_data, commit_message + "idea" , typeOfData )
    else:
        edit_and_commit_file(github_username, repository_name, file_path, "ideas", github_token, new_suggestion_data, commit_message + "suggestion." ,typeOfData, idea_id)




new_idea_data = {
    "id": 125,
    "title": "Innovative Sustainable Agriculture App",
    "description": "Proposing an app that empowers farmers with sustainable practices and connects them with modern agricultural resources.",
    "tags": ["Agriculture", "Technology", "Sustainability"],
    "likes": 0,
    "user": {
        "name": "New User",
        "email": "newuser@example.com",
        "phone": "9876543210"
    },
    "suggestions": []
}

new_suggestion_data = {
            "likes": 0,
            "isAnonymous": False,
            "description": "Fantastic IDea. Would love to work with you.",
            "user": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "phone": None
            }}

# For Ideas
createCommit("newidea",new_idea_data = new_idea_data)


idea_id = 1
# For suggestions
# createCommit(typeOfData= "newsuggestion", new_suggestion_data = new_suggestion_data, idea_id=idea_id)
