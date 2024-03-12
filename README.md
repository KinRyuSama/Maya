AI Bot Sandbox
==============

- [done] Create `list_files` tool that lists files in a directory (recursively).
    update ignore
- [done] Create `read_file` tool that reads the content of a file.
- [ ] Create `update_file` tool that:
    - Takes arguments "path: str" and "changes: str".
    - Reads the content of the file behind-the-scenes.
    - Calls gpt-4 with the content and the changes (short description), and
      outputs "a list of changes that can be applied mechanically by an intern".
    - Calls gpt-3.5 with the content and this "list of changes", asking it to
      rewrite the whole file applying ONLY the listed changes.
- [ ] At this stage, you _really_ need to save your project to Git.
- [ ] Use these tools to build another tool that reads the content of a web URL.
    - That's where you see the power of automating work.


Initial Setup
-------------

### Python

Download and install [Python 3.11](https://www.python.org/downloads/).
Make sure that you have "add to path" checked when running the installer.

Open a terminal in the repository's root and create a virtual environment:

    $ python -m venv .venv

Then activate the environment with:

    $ .venv\Scripts\activate            # on Windows
    $ source .venv/scripts/activate     # on Mac or Linux

### Visual Studio Code

If you wish to use VSCode to edit this project:

1. Install the extensions "Python", "Black" and "Ruff".
   Black will format your code and Ruff will lint (auto-fixing some issues).
1. When you open a .py file, VSCode should ask you to select an interpreter.
   Select the virtual environment you created [earlier](#python).

Note: If you get the following error in the integrated terminal:

> Scripts\activate.ps1 cannot be loaded because running scripts is disabled on
> this system.  For more information, see about_Execution_Policies`

You have a few options, but the easiest is to open a PowerShell window and run

    $ Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted


Run locally
-----------

### Run with Python

Once the virtual environment has been enabled, you can run:

    $ pip install -r requirements.txt
    $ watchmedo auto-restart -p "*.py" -R python -- -m src.app

If you do not want the service to restart on file changes, or watchmedo fails,
run instead:

    $ python -m src.app

The local files visible to Sonata will be listed in your terminal.

If you open your `/settings` in Sonata, you should immediately see the tools
whose secrets you have configured.
