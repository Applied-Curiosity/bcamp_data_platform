# bcamp_data_platform_azure

BCAMP and Applied Curiosity's Data Platform Infrastructure

## Azure Walking Skeleton

### Step 1: Create a Git Repository to Hold Our Infrastructure as Code

**Objective:** Set up a central repository to store and manage your Infrastructure as Code (IaC) using Git.

**Instructions:**

1. **Set up Git (if not already installed):**
    - On your local machine, check if Git is installed by running `git --version` in your terminal. If it's not installed, download and install Git from [git-scm.com](https://git-scm.com/).
2. **Create a new repository on GitHub:**
    - Log in to your GitHub account.
    - Navigate to the Repositories tab and click on 'New' to create a new repository.
    - Name your repository `bcamp_data_platform_azure`.
    - Choose whether to make the repository public or private.
    - Initialize the repository with a README file to provide an overview of the project.
    - Initialize with a Python `.gitignore` file to protect environment variables and avoid checking in libraries
    - Click on 'Create repository'.
3. **Clone the repository to your local machine:**
    - Once the repository is created, click the 'Code' button and copy the URL provided.
    - Open your terminal, navigate to the directory where you want to store the project, and run:
        
        ```
        git clone [URL]
        
        ```
        
    - Replace `[URL]` with the URL you copied from GitHub.
4. **Create a directory structure:**
    - Inside your local repository, create a directory named `infra` to store your Pulumi projects:
        
        ```
        mkdir infra
        cd infra
        
        ```
        
5. **Initial Commit:**
    - Add the newly created directory to Git:
        
        ```
        git add infra
        git commit -m "Initial commit: Setup infra directory for Pulumi projects"
        
        ```
        
    - Push the changes to GitHub:
        
        ```
        git push origin main
        
        ```
        

### Step 2: Install the Pulumi Library

**Objective:** Install Pulumi on your local machine to manage and deploy your infrastructure as code.

**Instructions:**

1. **Download Pulumi:**
    - Visit the [Pulumi Downloads page](https://www.pulumi.com/docs/get-started/install/) and select the installer appropriate for your operating system (Windows, macOS, or Linux).
2. **Install Pulumi:**
    - For macOS and Linux:
        - Open a terminal and run the script provided on the Pulumi website. For example:
            
            ```
            curl -fsSL <https://get.pulumi.com> | sh
            
            ```
            
    - For Windows:
        - Download the installer and execute it to install Pulumi.
3. **Verify Installation:**
    - After installation, reopen your terminal or command prompt and run:
        
        ```
        pulumi version
        
        ```
        
    - This command should display the version of Pulumi installed, confirming that the installation was successful.
4. **Set up the Pulumi configuration:**
    - Pulumi requires you to log in to a backend where it can store state and perform operations. For initial setup and testing, you can use the Pulumi-managed service by running:
        
        ```
        pulumi login
        
        ```
        
    - This command will prompt you to log in via a web browser.
    - ***Special note*** - if you’re using codespaces or container development, you will need to use your personal access token from Pulumi to authenticate. You can retrieve this token from the Pulumi website by clicking your profile icon in the top right corner. In the dropdown menu select personal access token.
5. **Configure Pulumi for Python:**
    - Ensure Python is installed on your system by running:
        
        ```
        python --version
        
        ```
        
    - If Python is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).
    - Install the Python package manager, pip, if it's not included in your Python installation:
        
        ```
        python -m ensurepip --upgrade
        
        ```
        
    - Set up a virtual environment in your project directory (`infra`) to manage Python dependencies:
        
        ```
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
        
        ```
        
    - Install the Pulumi Python SDK in the virtual environment:
        
        ```
        pip install pulumi
        
        ```
        

### Step 3: Install the Library for the Cloud Environment (Azure)

**Objective:** Install the necessary Pulumi library for Azure to manage resources in the Azure cloud.

**Instructions:**

1. **Activate your Python environment:**
    - Make sure you are in your project's root directory (where the `infra` directory is located).
    - Activate the Python virtual environment by running:
        
        ```
        source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
        
        ```
        
2. **Install the Pulumi Azure Provider:**
    - Use pip to install the Pulumi Azure provider. Run:
        
        ```
        pip install pulumi_azure
        
        ```
        
    - This command installs the Pulumi Azure SDK which allows you to write infrastructure code that provisions and manages Azure resources.
3. **Verify the installation:**
    - To ensure that the Azure provider was installed correctly, you can check the installed packages in your virtual environment:
        
        ```
        pip list
        
        ```
        
    - Look for `pulumi` and `pulumi_azure` in the list of installed packages to confirm their installation.
4. **Configure Azure settings:**
    - Set up the Azure provider configuration by running:
        
        ```
        pulumi config set azure:location <preferred-location>
        
        ```
        
    - Replace `<preferred-location>` with the Azure region you prefer, such as `eastus`, `westeurope`, etc.
5. **Authentication:**
    - Since you are using federated credentials in Azure, ensure your local environment is configured to authenticate with Azure. This might involve setting up the Azure CLI and logging in:
        
        ```
        az login
        
        ```
        
    - This step is crucial for Pulumi to perform operations on your Azure account.
6. **Test the setup:**
    - Create a simple Pulumi script to test the setup. In the `infra` directory, create a Python file, say `test_azure.py`, and write a basic script to list resource groups as a test:
        
        ```python
        import pulumi_azure as azure
        
        # List all resource groups
        resource_groups = azure.core.get_resource_groups()
        for rg in resource_groups:
            pulumi.export(rg.name, rg.location)
        
        ```
        
    - Run this script using:
        
        ```
        pulumi up
        
        ```
        
    - This command will execute the script and should output the resource groups in your Azure subscription if everything is configured correctly.

### Step 3: Install the Library for the Cloud Environment (Azure)

**Objective:** Install and configure the Azure CLI, which is essential for managing Azure resources directly from the command line.

**Instructions:**

1. **Install Azure CLI:**
    - Visit the [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) page and follow the instructions for your operating system.
    - For most systems, you can install Azure CLI via a single command. For instance, on macOS, you can use Homebrew:
        
        ```
        brew update && brew install azure-cli
        
        ```
        
    - On Windows, you can install it using the MSI installer available from Microsoft.
2. **Verify Installation:**
    - Open a new terminal or command prompt and run:
        
        ```
        az --version
        
        ```
        
    - This command will display the Azure CLI version along with other relevant information. Ensure that the Azure CLI is properly installed.
3. **Login to Azure:**
    - To configure the Azure CLI to use your Azure subscription, run:
        
        ```
        az login
        
        ```
        
    - This command will open a web browser asking you to log in to your Azure account. Once logged in, the CLI will be connected to your Azure subscription.
4. **Set the Default Subscription:**
    - If you have multiple Azure subscriptions, set the default one for your operations:
        
        ```
        az account set --subscription "Name or ID of Your Subscription"
        
        ```
        
    - Replace "Name or ID of Your Subscription" with the actual name or ID of the subscription you intend to use for deploying resources.
5. **Check Connectivity and Permissions:**
    - Run a simple command to list Azure resource groups to confirm proper setup and connectivity:
        
        ```
        az group list --output table
        
        ```
        
    - This command shows a table of all resource groups in your subscription, confirming that your CLI is configured correctly and has the necessary permissions.

### Step 4: Create the Project from the Git Repository Using Pulumi

**Objective:** Set up a new Pulumi project within your existing `infra` directory in your repository, tailored for Azure using Python.

**Instructions:**

1. **Navigate to Your `infra` Directory:**
    - Open your terminal, and make sure you are in the root directory of your cloned repository (`bcamp_data_platform_azure`). Then navigate to the `infra` directory:
        
        ```
        cd infra
        
        ```
        
2. **Create a New Pulumi Project:**
    - Initiate the creation of a new Pulumi project by running:
        
        ```
        pulumi new bcamp_data_platform_azure
        
        ```
        
    - This command will scaffold a new Pulumi project set up for Python development with Azure. It includes sample code and dependencies in a Python virtual environment.
3. **Configure the Project:**
    - During the setup, you will be prompted to enter several details:
        - **Project Name:** You can accept the default name suggested by Pulumi or provide a new one. For consistency, let's name it based on our repository structure, e.g., `bcamp_data_platform_azure`.
        - **Project Description:** Provide a brief description, e.g., "A minimal Azure Native Pulumi program."
4. **Set Up a Stack:**
    - You will be asked to provide a stack name. A stack in Pulumi represents an isolated environment within your project. You can use the default name, `dev`, or specify another name that reflects your deployment stage, such as `production` or `test`.
5. **Choose Azure Location:**
    - Specify the Azure location where your resources will be deployed. You can accept the default or choose another location. To list all available locations, use:
        
        ```
        az account list-locations --output table
        
        ```
        
    - Set the location for your stack with:
        
        ```
        pulumi config set azure-native:location [location-name]
        
        ```
        
    - Replace `[location-name]` with your chosen location, such as `centralus`.
6. **Finalize and Review Project Files:**
    - Once the project setup is complete, review the created files within the `infra` directory. You should have a `Pulumi.yaml` for project settings, `__main__.py` for your Python code, and a virtual environment folder for Python packages.
7. **Commit the New Project to Git:**
    - Add the new Pulumi project files to your Git repository:
        
        ```
        git add .
        git commit -m "Setup new Pulumi project for Azure in Python"
        
        ```
        
    - Push the changes to your GitHub repository:
        
        ```
        git push origin main
        
        ```
        

### **Step 5: Create an Authentication and Authorization Principal Cloud Service Account**

**Objective:** Set up an Azure service principal with Federated Identity Credential to allow GitHub Actions to deploy resources securely.

**Instructions:**

1. **Create a Service Principal:**
    - Open the Azure CLI and run the following command to create a new application and service principal:
        
        ```css
        cssCopy code
        az ad sp create-for-rbac --name <YourAppName> --role contributor --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}
        
        ```
        
    - Replace **`<YourAppName>`**, **`{subscription-id}`**, and **`{resource-group}`** with your application name, Azure subscription ID, and resource group name respectively.
2. **Assign Role to Service Principal:**
    - Assign a role to the service principal to define the permissions it has on Azure resources. The 'Contributor' role is commonly used for deployment tasks.
3. **Configure Federated Identity Credential:**
    - Navigate to the Azure portal, go to 'App registrations', select your app, and then go to 'Certificates & secrets'.
    - Add a new federated credential tailored for GitHub Actions, specifying details like the GitHub organization and repository.
4. **Create GitHub Secrets:**
    - In your GitHub repository, navigate to 'Settings' > 'Security' > 'Secrets and variables' > 'Actions'.
    - Add secrets for **`AZURE_CLIENT_ID`**, **`AZURE_TENANT_ID`**, and **`AZURE_SUBSCRIPTION_ID`** with values obtained from your Azure service principal.
5. **Update GitHub Actions Workflow:**
    - Modify your GitHub Actions workflow file to include steps for Azure authentication using the secrets you stored. Use the **`azure/login@v1`** action with parameters like **`client-id`**, **`tenant-id`**, and **`subscription-id`** obtained from your Azure service principal.

### Step 6: Build a Minimal GitHub Action to Test Deployment

**Objective:** Create a GitHub Action to automate the deployment of your Azure resources using Pulumi.

**Instructions:**

1. **Create a GitHub Workflow File:**
    - In your repository (`bcamp_data_platform_azure`), navigate to the `.github/workflows` directory. If this directory doesn't exist, create it:
        
        ```
        mkdir -p .github/workflows
        
        ```
        
    - Create a new file named `azure_deploy.yml` in this directory.
2. **Define the Workflow:**
    - Edit `azure_deploy.yml` to define the workflow. Start by specifying the name and trigger conditions. For example:
        
        ```yaml
        name: Deploy Azure Infrastructure
        on:
          push:
            branches:
              - main
          workflow_dispatch:
        
        ```
        
    - This configuration triggers the workflow on pushes to the `main` branch and allows manual triggering from the GitHub interface.
3. **Set Up Jobs and Steps:**
    - Define a job to run the deployment. Configure it to run on an Ubuntu runner and include steps to check out the code, set up Python, install dependencies, and execute Pulumi commands. For instance:
        
        ```yaml
        jobs:
          deploy:
            runs-on: ubuntu-latest
            steps:
              - name: Checkout Code
                uses: actions/checkout@v2
        
              - name: Set up Python
                uses: actions/setup-python@v2
                with:
                  python-version: '3.x'
        
              - name: Install Dependencies
                run: |
                  pip install -r requirements.txt
        
              - name: Deploy with Pulumi
                run: |
                  pulumi up --yes
        
        ```
        
    - Include authentication steps using Azure credentials before running Pulumi commands:
        
        ```yaml
              - name: Login to Azure
                uses: azure/login@v1
                with:
                  client-id: ${{ secrets.AZURE_CLIENT_ID }}
                  tenant-id: ${{ secrets.AZURE_TENANT_ID }}
                  subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        
        ```
        
4. **Push Changes to GitHub:**
    - Commit and push your changes to the repository:
        
        ```
        git add .github/workflows/azure_deploy.yml
        git commit -m "Add GitHub Actions workflow for Azure deployment"
        git push origin main
        
        ```
        

### Step 7: Check in a Minimal Resource for Deployment and Allow the Action to Deploy the Resource

**Objective:** Add a minimal Azure resource definition in your Pulumi project and use the GitHub Action to deploy it.

**Instructions:**

1. **Define a Minimal Azure Resource:**
    - In your Pulumi project within the `infra` directory, edit the `__main__.py` file to define a minimal resource, such as an Azure Resource Group. For example:
        
        ```python
        import pulumi
        from pulumi_azure_native import resources
        
        # Create an Azure Resource Group
        # Naming convention is 
        # rg = resource group
        # ac = Applied Curiosity
        # cus = Central US
        # adb = Azure Databricks
        # acclrtor = Accelerator
        resource_group = resources.ResourceGroup('rg-ac-cus-adb-acclrtor')
        
        ```
        
    - This code snippet creates a new resource group in Azure.
2. **Commit and Push the Changes:**
    - Add the changes to your Git repository:
        
        ```
        git add infra/__main__.py
        git commit -m "Add minimal Azure resource group definition"
        git push origin main
        
        ```
        
3. **Monitor GitHub Actions Workflow:**
    - After pushing the changes, navigate to the 'Actions' tab in your GitHub repository to monitor the workflow execution.
    - The GitHub Action you set up in the previous step will trigger, building and deploying the new resource using Pulumi.
4. **Verify Deployment:**
    - Check the output of the GitHub Action to confirm that the deployment was successful.
    - Optionally, use the Azure CLI to verify the resource was created:
        
        ```
        az group show --name rg-ac-cus-adb-acclrtor
        
        ```
