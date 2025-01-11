from langchain_core.tools import tool
import os
from bitbucket import bitbucketmethods
 

@tool
def manage_repo_and_get_file(filepath: str, repo_path):
    """
    Manages the repository and retrieves the file content based on the repository's existence.

    Args:
        filepath (str): The path to the file to be retrieved.

    Returns:
        str: The content of the file if successful, None otherwise.
    """
    # Initialize the bitbucketmethods class
    trail = bitbucketmethods()
    workspace = "sampleforbbagent"
    repo_slug = "sample_repo_for_bbagent" 
    # Extract workspace and repo_slug from the filepath or define them
    # Assuming the repo_slug is derived from the filepath, adjust as necessary
    access_token = os.getenv("ACCESS_TOKEN")

    # Check if the repository directory exists
    if os.path.exists(repo_slug):
        # If it exists, directly get the file content
        print("Repository already exists. Retrieving file content...")
        return trail.get_filecontent(filepath, repo_path)
    else:
        # If it doesn't exist, perform the sequence of operations
        print("Repository does not exist. Cloning repository...")
        repo_details = trail.get_repo(workspace, repo_slug, access_token)
        if repo_details:
            clone_success = trail.clone_repo(workspace, repo_slug, access_token)
            if clone_success:
                # After cloning, get the file content
                print("Repository clonning is successful...")
                return trail.get_filecontent(filepath, repo_path)
            else:
                print("Failed to clone the repository...")
                return None
        else:
            print("Failed to retrieve repository details...")
            return None

@tool        
def commit_changes_and_raise_pr(file_path, changed_content, branch_name, commit_message, repo_path):
    """
        Commits changes to a specified file in a Bitbucket repository and raises a pull request.

        Args:
            file_path (str): The path to the file that will be modified. format for file_path: "/file_path"
            changed_content (str): The new content to be written to the file.
            branch_name (str): The name of the branch to create for the changes.
            commit_message (str): The message to be used for the commit.
            repo_path (str): The local path to the repository where the changes will be made.
            workspace (str): The Bitbucket workspace where the repository is located.
            repo_slug (str): The slug of the repository in Bitbucket.

        Returns:
            bool: True if the changes were successfully committed and the pull request was raised, 
                  False otherwise.
    """
    # Create an instance of the bitbucketmethods class
    bitbucket_instance = bitbucketmethods()
    workspace = "sampleforbbagent"
    repo_slug = "sample_repo_for_bbagent"   
    # Step 2: Create a new branch
    print("creating a new branch")
    branch_created = bitbucket_instance.create_branch(branch_name, repo_path, workspace, repo_slug)
    if not branch_created:
        print("Failed to create branch.")
        return False
    
    # Step 1: Change the content of the file
    change_result = bitbucket_instance.change_content(file_path, changed_content)
    if change_result != "success":
        print(f"Failed to change content of the file: {change_result}")
        return False
    
    
    # Step 3: Commit the changes
    commit_success = bitbucket_instance.commit_changes(commit_message)
    if not commit_success:
        print("Failed to commit changes.")
        return False
    
    # Step 4: Raise a pull request
    bitbucket_instance.raise_pr(branch_name, workspace, repo_slug)
    return True

if __name__ == "__main__":
    # manage_repo_and_get_file.invoke(
    #     input={
    #         "filepath": "/sample_text.txt",
    #         "workspace": "sampleforbbagent",
    #         "repo_slug": "sample_repo_for_bbagent",
    #         "repo_path": "./sample_repo_for_bbagent"
    #     }
    # )
    commit_changes_and_raise_pr.invoke(
        input={
            "file_path": "/sample_text.txt",
            "changed_content": "Hey this when test",
            "branch_name": "trail8",
            "commit_message": "This is a test message",
            "repo_path": "./sample_repo_for_bbagent",
            "workspace": "sampleforbbagent",
            "repo_slug": "sample_repo_for_bbagent"
        }
    )