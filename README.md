/// INTRODUCTION ///

The file in this repo allows you to close asana tasks when committing changes to Bitbucket (or any other git-based repository).  This code will be set up as something known as a git hook (you can read more about them here: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).  Git hooks are called when a certain action occurs and this script, per the instructions below, will be setup to run automatically after every git commit.  Thus, this script is named "post-commit" because it will occur after a commit.

There is a great bash script version of this file available here: https://github.com/Spaceman-Labs/asana-post-commit if you find bash script more interesting.  It served as the general model for this code, so check it out if you have some time!

The rest of this readme will take you through the following steps:

>ASANA SETUP:  This section provides instructions for getting a Personal Access Token and some basics on the structure of the Asana API.

>INSTALLATION:  This section walks you through the process for installing and preparing the file(s) from this repository.

>USAGE:  This section gives instructions on how to use this program once it is installed.

 

/// ASANA SETUP ///

To begin with, you will need an accout with Asana.  If you do not have one, please visit: https://asana.com/ and make an account.  These programs use Asana personal access tokens instead of API keys because API keys are being deprecated.

Assuming you have an account, there are three major steps to get and configure your Asana personal access token:

1.  Get an Asana token.

    To get a token, visit: http://app.asana.com/-/account_api.  There will be an option to "Create New Personal Access Token," which you can click and follow instructions to create and copy the personal access token.  Remember to copy it because you will only see it once!  If there are any problems, you can always deauthorize a token a create a new one by following these steps.

2.  Set token via git config

    Once you have a personal access token, open up the terminal or command line and type (including the quotation marks):
            
            git config --global user.asana-token "YOUR PERSONAL ACCESS TOKEN HERE"

    This makes your personal access token accessible for any git repository so that it can be used to authenticate closing a task from a git commit.

3.  Asana API basics

    You can read more about the Asana API here: https://asana.com/developers/api-reference/attachments, but for the time being, you really only need to know the following principle.  

    In order to mark a task as completed and/or to comment on a task, you need to have the task id.  To get the task id, login to the Asana online app here: https://app.asana.com/.  Then, create a new task or click on an existing one.  After clicking on it, notice the url.  The last number in the url is the task id.  This number will change if you click on a different task.  For example, if you click on a task in Asana, you will see something like:  https://app.asana.com/0/0123456789/9876543210.  The first, long number (0123456789) represents the workspace or project in which the task is located.  The last number (9876543210) represents the id of the task that is currently selected.  As you will see later under the "USAGE" heading, you will need to copy this task id (the last number of the url) in order to close a task via a commit message.

 

/// INSTALLATION ///

Using post-commit.py (the python script):

1.  Download or clone this repository.

2.  Open the post-commit.py program.  Even before you place it in a repository of your own, you should change the git_config_file_directory variable that is located near the top of the post-commit.py script.  This variable is the path to the git config file which will contain your Asana personal access token as described in step five.  This directory will be the same for every copy of this script, so once you have set the git_config_file_directory, you can copy the script to any repo of your choice.  In order to find the path to your git config file, type the following in terminal:

        git config --global --edit
        # This will open the file for editing and should show you the path to the file at the bottom of the terminal.  
        # For more information, please visit https://answers.atlassian.com/questions/235494/storage-location-for-global-gitconfig.

3.  Copy the post-commit.py file from this downloaded/cloned repository to the .git/hooks folder within your own repository where you want to use this script.  The file also needs to be renamed to 'post-commit' (without the quotation marks).  Using terminal, you can do this in one, fell swoop:

        cp PATH/TO/THIS/CLONED/REPO/post-commit.py PATH/TO/YOUR/REPO/.git/hooks/post-commit

4.  Navigate to the repo from which you want to run this script and make the post-commit file executable.  Using terminal:

        cd PATH/TO/YOUR/REPO
        chmod +x .git/hooks/post-commit

5.  Make sure that you have added your Asana personal access token to the global git config.  Instructions for doing this can be found in step 2 of the "ASANA SETUP" section.  Using terminal:

        git config --global user.asana-token "YOUR_ASANA_PERSONAL_ACCESS_TOKEN" 

6.  EVERY TIME YOU PUT THE POST-COMMIT SCRIPT in a new file, you will have to specify the directory of that repo.  To do this, open the post-commit file you have copied into a repository and change the bitbucket_repo_directory variable near the top of the script to hold the path to the current repo.  Using terminal, it will look something like:
        
        cd PATH/TO/REPO
        nano /.git/hooks/post-commit
        # At this point, type in the path to the top folder of the current repo.


At this point, you're good to go!  Check out the guide to usage below and if you have any problems please check out the "NOTES & GOTCHAs" section below or post a comment and let me know.


/// USAGE ///

This file closes asana tasks just like you would close issues in Bitbucket except this program uses task id numbers instead of issue numbers.  When closing issue (for example issue #4) in Bitbucket, you would add something like this to the end of the commit message:

        fixes #4

For this script, you can do very much the same thing only you need to copy the task id number (refer to step 3 in "ASANA SETUP" for more information on how to find this) and use that number in a fixes statement as follows:

        fixes #0123456789

        or 

        updated the UI which fixes #0123456789

There are a couple more features of this script, however.  First, you can close multiple tasks by typing multiple task ids and you can even use the word 'and' when closing multiple tasks.  Second, to close a task in Asana with this script, you can type any word that starts with: 'close', 'fix', or 'closing'.  For some examples, all of the lines below would close the same three tasks in Asana:

        updated usage which closes #0987654321 and fixes #4444444444 and #0123456789

        updated union dues fixed #0987654321, #4444444444, and #0123456789

        closing #0987654321 and #4444444444 because the thingy was updated and is now working!  And also closing #0123456789


/// NOTES & GOTCHA's ///

When the scripts are running to close a task, the script itself can take a couple of seconds to run depending on the speed of your internet connection.  Even once the script has run and made a successful request to Asana, it can still take up to ten seconds for the task to appear as closed in Asana.  Don't worry... it will close.  Quien espera desespera (or the English equivalent: "The watched pot never boils").

If the script is not running properly, you might want to look into changing the #!/usr/bin/env python at the top of the script or make sure that you have python in your system path.  For more information on this, refer to: https://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script