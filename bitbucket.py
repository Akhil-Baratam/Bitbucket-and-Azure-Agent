import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
import requests
import json
from urllib.parse import quote_plus


access_token = os.getenv("ACCESS_TOKEN")

class bitbucketmethods:

  def __init__(self) -> None:
    pass

  def get_repo(self,workspace, repo_slug, access_token):
      
      url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}"

      headers = {
          "Accept": "application/json",
          "Authorization": f"Bearer {access_token}"
      }

      response = requests.request(
          "GET",
          url,
          headers=headers
      )


      repo_details = json.loads(response.text)
      print(json.dumps(repo_details, sort_keys=True, indent=4, separators=(",", ": ") ))
      return repo_details
  

  def clone_repo(self,workspace, repo_slug, access_token):

      encoded_token = quote_plus(access_token)
      clone_url = f"https://x-token-auth:{encoded_token}@bitbucket.org/{workspace}/{repo_slug}.git"
        
      # Set Git configurations to prevent prompts
      env = os.environ.copy()
      env['GIT_TERMINAL_PROMPT'] = '0'
      env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
      
      try:
          # Remove directory if it exists
          if os.path.exists(repo_slug):
              import shutil
              shutil.rmtree(repo_slug)
              
          # Clone with credential helper disabled and other automated settings
          clone_command = [
              'git',
              '-c', 'credential.helper=',
              '-c', 'core.askPass=',
              'clone',
              clone_url
          ]
          
          result = subprocess.run(
              clone_command,
              env=env,
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,
              text=True,
              check=True
          )
          
          print("Repository cloned successfully!")
          return True
            
      except subprocess.CalledProcessError as e:
          print(f"Error cloning repository: {e.stderr}")
          return False

  def get_filecontent(self, file_path, repo_path):
      """
      Reads the content of a file using subprocess.

      Args:
          file_path (str): The path to the file.

      Returns:
          str: The content of the file if successful, None otherwise.
      """
      try:
        # Open the file in read mode
        relative_path = repo_path + file_path
        with open(relative_path, 'r') as f:
          content = f.read()
        #   print(content)
          return content
      except (FileNotFoundError, PermissionError) as e:
        print(f"Error reading file: {e}")
        return None
  
  def create_branch(self, branch_name, repo_path, workspace, repo_slug):
    try:
        # Change to the specified repository path
        os.chdir(repo_path)  # Ensure this path is a valid Git repository
        print("Current directory before creating branch:", os.getcwd())
        
        # Check if the branch already exists
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            branches = response.json().get('values', [])
            existing_branches = [branch['name'] for branch in branches]
            
            if branch_name in existing_branches:
                print(f"Branch '{branch_name}' already exists. Skipping creation.")
                return True  # Exit the method if the branch exists
        else:
            print(f"Failed to fetch branches: {response.text}")
            return False

        # Pull the latest changes from the main branch
        pull_command = ['git', 'pull', 'origin', 'main']
        result = subprocess.run(
            pull_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Create a new branch using subprocess
        create_branch_command = ['git', 'checkout', '-b', branch_name]
        print(f"Creating a new branch with name: {branch_name}")
        
        result = subprocess.run(
            create_branch_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print(f"Branch '{branch_name}' created successfully!")
        return True
      
    except subprocess.CalledProcessError as e:
        self.checkout_main()
        print(f"Error creating branch: {e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

  def change_content(self, file_path, changed_content):
      
      try:
        print("current directory while changing content" , os.getcwd())
        # Open the file in read mode
        file_path = '.' + file_path
        changed_content = changed_content.replace('```','')
        with open(file_path, 'w') as f:
          f.write(changed_content)
          return "success"
      except (FileNotFoundError, PermissionError) as e:
        print("current working directory", os.getcwd())
        self.checkout_main()
        print(f"Error writing file: {e}")
        return f"failure: {e} "
     
  def commit_changes(self, commit_message):
      try:
          print("current directory while committing changes" , os.getcwd())
          # Stage all changes
          add_command = ['git', 'add', '.']
          print("Adding all the changes made...")
          subprocess.run(add_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
          
          # Commit the changes
          commit_command = ['git', 'commit', '-m', commit_message]
          print("Commiting the changes...")
          subprocess.run(commit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)          
          print(f"Changes committed successfully with message: '{commit_message}'")
          return True
          
      except subprocess.CalledProcessError as e:
          self.checkout_main()
          print(f"Error during commit: {e}")
          return False

  def checkout_main(self):
      checkout_to_main = ['git', 'checkout', 'main']
      print(f"checking out to main branch...")
      subprocess.run(checkout_to_main, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

  def raise_pr(self, branch_name, workspace, repo_slug):
      try:
          print("current directory while raising pr" , os.getcwd())
          # Push the code to the specified branch
          push_command = ['git', 'push', 'origin', branch_name]
          print(f"Pushing changes to branch '{branch_name}'...")
          subprocess.run(push_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
          print(f"Changes pushed successfully to branch '{branch_name}'.")

          # Prepare to create a pull request
          url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests"
          
          headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              "Authorization": f"Bearer {access_token}"
          }
          
          # Create the payload for the pull request
          payload = {
              "title": f"Pull request for {branch_name}",
              "source": {
                  "branch": {
                      "name": branch_name
                  }
              }
          }
          
          # Send the request to create the pull request
          response = requests.post(url, json=payload, headers=headers)
          
          if response.status_code == 201:
              print(f"Pull request created successfully for branch '{branch_name}'.")
          else:
              print(f"Failed to create pull request: {response.text}")

                  # Remove the cloned repository directory
          if os.path.exists(repo_slug):
              import shutil
              shutil.rmtree(repo_slug)  # Remove the directory and all its contents
              print(f"Removed the cloned repository directory: {repo_slug}")
          self.checkout_main()

      
      except subprocess.CalledProcessError as e:
          print(f"Error during push: {e.stderr}")
          self.checkout_main()
      except Exception as e:
          print(f"An error occurred: {e}")
          self.checkout_main()

trail = bitbucketmethods()
# trail.get_repo("sampleforbbagent", "sample_repo_for_bbagent", access_token)
# trail.clone_repo("sampleforbbagent", "sample_repo_for_bbagent", access_token)
# trail.get_filecontent("./sample_repo_for_bbagent/sample_json_file")
# trail.create_branch(branch_name, repo_path)