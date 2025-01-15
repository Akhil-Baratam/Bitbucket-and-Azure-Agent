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
    self.cwd = ''
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
      
      if self.cwd:
        print("Clone operation skipped: self.cwd is already set.")
        return False

      encoded_token = quote_plus(access_token)
      clone_url = f"https://x-token-auth:{encoded_token}@bitbucket.org/{workspace}/{repo_slug}.git"
        
      # Set Git configurations to prevent prompts
      env = os.environ.copy()
      env['GIT_TERMINAL_PROMPT'] = '0'
      env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
      
      try:

              
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
          # Store the current working directory after successful clone
          self.cwd = os.getcwd()
          print("Repository cloned successfully!")
          return True
            
      except subprocess.CalledProcessError as e:
          print(f"Error cloning repository: {e.stderr}")
          return False

  def get_filecontent(self, file_name, repo_path):
      """
      Reads the content of a file using subprocess.

      Args:
          file_name (str): The name to the file.
          repo_path (str): The repository root path

      Returns:
          str: The content of the file if successful, None otherwise.
      """
      
      try:
          file_path = ''
          for root, dirs, files in os.walk(repo_path):
              if file_name in files:
                  file_path = os.path.relpath(os.path.join(root, file_name), repo_path)
                  break

          if not file_path:
              print(f"File {file_name} not found in repository")
              return None

          relative_path = os.path.join(repo_path, file_path)
          with open(relative_path, 'r') as f:
              content = f.read()
              return content

      except (FileNotFoundError, PermissionError) as e:
          print(f"Error reading file: {e}")
          return None
  
  def create_branch(self, branch_name, repo_path, workspace, repo_slug):
    try:
        print("current directory while before creating branch" , os.getcwd())
        #input("Press Enter to continue with commit...")
        # Change to the specified repository path
        if not os.path.exists(repo_path):
            print(f"Repository path '{repo_path}' does not exist. Please clone the repository first.")
            return False
        
        os.chdir(repo_path)  # Ensure this path is a valid Git repository
        
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
        print("current directory while after creating branch" , os.getcwd())
        #input("Press Enter to continue with commit...")
        return True
      
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

  def change_content(self, file_path, changed_content):
      
      try:
        print("current directory before changing content" , os.getcwd())
        # Open the file in read mode
        file_path = '.' + file_path
        changed_content = changed_content.replace('```','')
        with open(file_path, 'w') as f:
          f.write(changed_content)
          print("current directory while after changing content" , os.getcwd())
          #input("Press Enter to continue with commit...")
          return "success"
      except (FileNotFoundError, PermissionError) as e:
        print("current working directory", os.getcwd())
        self.checkout_main()
        print(f"Error writing file: {e}")
        return f"failure: {e} "
      
     
  def commit_changes(self, commit_message, repo_slug):
      try:
          #input("press enter to continue")
          print("current directory while committing changes 1" , os.path.basename(os.getcwd()))
          #input("press enter to continue")
          print("repo path directory while committing changes 2" , repo_slug)
          #input("press enter to continue")
          
        
          # Check if the current working directory is the same as repo_path
          if os.path.basename(os.getcwd()) != repo_slug:
              print(f"Error: Current working directory '{os.getcwd()}' does not match the repository path '{repo_slug}'.")
              return False
          print("Current working directory matches the repo_path")
          # Stage all changes
          add_command = ['git', 'add', '.']
          print("Adding all the changes made...")
          #input("Press Enter to continue with commit...")
          subprocess.run(add_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
          
          # Commit the changes
          commit_command = ['git', 'commit', '-m', commit_message]
          print("Commiting the changes...")
          #input("Press Enter to continue with commit...")
          subprocess.run(commit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)          
          print(f"Changes committed successfully with message: '{commit_message}'")
          print("current directory while committing changes" , os.getcwd())
          #input("Press Enter to continue with commit...")
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
      """
      Creates and pushes a pull request to Bitbucket with improved error handling and cleanup.
      
      Args:
          branch_name (str): Name of the branch to create PR from
          workspace (str): Bitbucket workspace name
          repo_slug (str): Repository name/slug
      """
      initial_dir = os.getcwd()
      
      try:
          print(f"Current directory while raising PR: {os.getcwd()}")
          
          # Push the code to the specified branch
          print(f"Pushing changes to branch '{branch_name}'...")
          push_command = ['git', 'push', 'origin', branch_name]
          result = subprocess.run(
              push_command,
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,
              text=True,
              check=True
          )
          print(f"Changes pushed successfully to branch '{branch_name}'.")
  
          # Prepare pull request creation
          url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests"
          headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              "Authorization": f"Bearer {access_token}"
          }
          
          # Enhanced PR payload with more details
          payload = {
              "title": f"Pull request for {branch_name}",
              "description": "Automated pull request created by CI/CD pipeline",
              "source": {
                  "branch": {
                      "name": branch_name
                  }
              },
              "destination": {
                  "branch": {
                      "name": "main"  # or your default branch name
                  }
              },
              "close_source_branch": True  # Optional: close source branch after merge
          }
          
          # Create pull request with better error handling
          try:
              response = requests.post(url, json=payload, headers=headers)
              response.raise_for_status()  # Raise exception for non-200 status codes
              
              if response.status_code == 201:
                  pr_data = response.json()
                  print(f"Pull request created successfully:")
                  print(f"Title: {pr_data.get('title')}")
                  print(f"URL: {pr_data.get('links', {}).get('html', {}).get('href')}")
              else:
                  print(f"Unexpected status code {response.status_code} when creating PR")
                  print(f"Response: {response.text}")
          
          except requests.exceptions.RequestException as e:
              print(f"Error creating pull request: {str(e)}")
              raise
  
      except subprocess.CalledProcessError as e:
          print(f"Error during git push: {e.stderr}")
          raise
      except Exception as e:
          print(f"Unexpected error: {str(e)}")
          raise
      finally:
          # Ensure cleanup happens whether operations succeed or fail
          try:
              # Return to initial directory before cleanup
              os.chdir(initial_dir)
              
              # Attempt to checkout main branch
              try:
                  self.checkout_main()
              except Exception as e:
                  print(f"Warning: Failed to checkout main branch: {e}")
              
              # Debugging: Print current working directory and directory to be removed
              print("Current working directory before removing cloned repo:", os.getcwd())
              print("Attempting to remove repository directory:", repo_slug)
              
              # Clean up repository directory
              try:
                  import shutil
                  os.chdir('..')
                  shutil.rmtree(repo_slug)
                  print(f"Successfully removed repository directory: {repo_slug}")
              except Exception as e:
                  print(f"Warning: Failed to remove repository directory: {e}")
              
          except Exception as cleanup_error:
              print(f"Warning: Error during cleanup: {cleanup_error}")
  
  
      
  
trail = bitbucketmethods()
  # trail.get_repo("sampleforbbagent", "sample_repo_for_bbagent", access_token)
  # trail.clone_repo("sampleforbbagent", "sample_repo_for_bbagent", access_token)
  # trail.get_filecontent("./sample_repo_for_bbagent/sample_json_file")
  # trail.create_branch(branch_name, repo_path)