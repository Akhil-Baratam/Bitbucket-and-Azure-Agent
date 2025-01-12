# Sample Repository for BBAgent

## Overview

This repository is designed to automate Bitbucket repository management tasks. It provides functionalities for cloning repositories, managing branches, modifying files, and creating pull requests. The project utilizes various tools and libraries to streamline these operations, making it easier for developers to manage their Bitbucket repositories efficiently.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- Git
- Access to a Bitbucket account
- An active internet connection

## Getting Started

### Cloning the Repository

To clone this repository, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command:

   ```bash
   git clone https://github.com/Akhil-Baratam/Bitbucket-and-Azure-Agent.git
   ```

4. Change into the cloned directory:

   ```bash
   cd Bitbucket-and-Azure-Agent
   ```

### Setting Up the Environment

1. **Install Dependencies**: This project requires several Python packages. You can install them using pip. Run the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**: Create a `.env` file in the root of the project directory and add your Bitbucket access token and OpenAI API key:

   ```plaintext
   ACCESS_TOKEN=your_bitbucket_access_token
   OPENAI_API_KEY=your_openai_api_key
   ```

### Project Structure

The project consists of the following key files and directories:

- `prompts.py`: Contains the prompts used for interacting with the AI agent.
- `tools.py`: Defines the tools for managing the repository and handling file operations.
- `bitbucket.py`: Contains methods for interacting with the Bitbucket API.
- `agent.py`: The main script that runs the AI agent.
- `models.py`: Defines the models used for AI interactions.
- `sample.yml`: A sample configuration file that can be modified as needed.
- `sample_text.txt`: A sample text file for testing file operations.
- `README.md`: This file, which provides an overview and instructions for the project.

### Using the AI Agent

1. **Run the Agent**: To start the AI agent, execute the following command in your terminal:

   ```bash
   python agent.py
   ```

2. **Interacting with the Agent**: The agent will prompt you to provide specific requirements for managing your Bitbucket repository. Follow the instructions provided in the terminal.

### Key Features

- **Repository Management**: Clone repositories, navigate through the structure, and manage local copies.
- **File Operations**: Read and modify file contents in the repository.
- **Branch Management**: Create and switch between branches as needed.
- **Version Control Operations**: Stage changes, commit with meaningful messages, and push changes to the remote repository.
- **Pull Requests**: Create pull requests for code review directly from the command line.

### Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Support

If you encounter any issues or have questions, feel free to open an issue in the repository or contact the project maintainers.

---

Thank you for using the Sample Repository for BBAgent! Happy coding!
