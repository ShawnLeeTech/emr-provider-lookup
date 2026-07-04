# GitHub Workflow

This document records the GitHub workflow for the EMRTS Provider Lookup project.

## Repository

- GitHub repository: git@github.com:ShawnLeeTech/emr-provider-lookup.git
- Default branch: main
- Local project path on Vesta: /home/chao/projects/emr-provider-lookup

## Authentication

The Vesta server is configured to connect to GitHub using SSH authentication.

- SSH config file: ~/.ssh/config
- GitHub SSH key name on server: id_ed25519_github
- GitHub account: ShawnLeeTech

Do not share private keys, passwords, personal access tokens, or other credentials in the repository.

## Daily Update Workflow

After completing work for the day, use this workflow:

1. Check the current status with git status.
2. Add changed files with git add.
3. Commit the changes with a clear commit message.
4. Push the committed changes to GitHub with git push.

## Useful Commands

- Check repository status: git status
- Check remote repository: git remote -v
- Push committed work to GitHub: git push
- Test GitHub SSH authentication: ssh -T git@github.com

A successful SSH authentication message should confirm the GitHub account and state that GitHub does not provide shell access.
