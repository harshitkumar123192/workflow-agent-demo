# Workflow Agent Demo Project — Personal Expense Tracker

A small, realistic Flask Personal Expense Tracker API for demonstrating the Dev Workflow Agent.
Use the same files to seed your Azure DevOps repository and GitHub repository. The app uses
clean in-memory data, and the demo deployment jobs intentionally wait for manual human approval.

## What the starter API does

- `POST /expenses` adds an expense (`description`, `amount`, `category`).
- `GET /expenses` lists all expenses.
- `GET /summary` totals spending across categories.
- `GET /` health check.

## Suggested First Jira Story

**Summary:** Filter expenses by category via query parameter

**Description / Acceptance Criteria:**

- Add `GET /expenses?category=<name>`.
- When `?category=` is passed, return only expenses whose category matches.
- When `?category=` is omitted or empty, return all expenses as before.
- When no expenses match the specified category, return `{"expenses": []}` with HTTP 200.
- Add tests in `app/tests/test_app.py` for matching and non-matching category filters.

## Review-Change Exercise (Demonstrating Human-in-the-Loop Rework)

When the agent creates the PR and reaches the `wait_for_review` step, vote **Changes Requested**
in Azure DevOps or GitHub with this comment:

> *"Please make the category filter case-insensitive so that `?category=food` matches an expense saved as `'Food'`. Also add a unit test covering mixed-case filtering."*

The agent detects the rejection, pulls the comment, applies the case-insensitive fix, updates the tests, and pushes a second commit to the same PR.

## Local check

From this directory, run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
PYTHONPATH=. python -m pytest app/tests -q
```

## Create both source repositories

Create an empty repository named `workflow-agent-demo` in Azure DevOps and another named
`workflow-agent-demo` in GitHub. In both, use `main` as the default branch. Seed both with
this directory's contents (including `app/`, `azure-pipelines.yml`, and `.github/`). Do not
put credentials in the repo.

To push this directory to both repositories from one local checkout:

```sh
cd demo-project
git init -b main
git add .
git commit -m "Add workflow agent demo app"
git remote add github https://github.com/YOUR-USER/workflow-agent-demo.git
git push -u github main
git remote add ado https://dev.azure.com/YOUR-ORG/YOUR-PROJECT/_git/workflow-agent-demo
git push -u ado main
```

Replace the uppercase placeholders with your own values. If `git init` says this is already
a repository, do not reinitialize it; check `git status` and `git remote -v` first.

## Jira Cloud

1. Create a Jira Cloud account at [Jira Free](https://www.atlassian.com/software/jira/free).
2. Create a Jira Software project named `Workflow Agent Demo`, preferably with key `DEMO`.
3. Create a Story with the sample summary and acceptance criteria above. Note its actual key
   (for example `DEMO-1`).
4. Create an API token at [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
5. In this app's Settings, configure the Jira URL (`https://YOUR-SITE.atlassian.net`), your
   Atlassian account email, and the API token. Use **Save and test**.

## Azure DevOps

Before setting up ADO on macOS, make sure Azure CLI is installed and on your PATH:

```sh
brew install azure-cli
az --version
```

If `brew` or `az` says `command not found`, finish Homebrew's PATH setup or open a new
Terminal window, then retry the version check. The app's Azure sign-in uses this CLI.

1. Create an organization at [Azure DevOps](https://dev.azure.com/), then create a project
   named `Workflow Agent Demo` and a Git repository named `workflow-agent-demo`.
2. Push the starter files to `main` using the commands above.
3. In Azure DevOps, open **Pipelines > Create Pipeline**, choose the repo, select **Existing
   Azure Pipelines YAML file**, and choose `/azure-pipelines.yml`. Name it `Workflow Agent Demo`
   if prompted, then save and run once. If ADO gives it another name, use that exact displayed
   name in the app's Settings.
4. To validate PRs, open **Repos > Branches**, open the menu for `main`, and add a **Build
   validation** branch policy using this pipeline. Azure Repos uses this branch policy for
   PR validation; the YAML `trigger` handles pushes to `main`.
5. In this app's Settings choose **Azure DevOps**. Set the organization URL, project name,
   repo name, default branch `main`, app folder `app`, and pipeline name `Workflow Agent Demo`.
   Then sign in to Azure in Settings and use **Save and test**.

The pipeline runs tests, then pauses at its `DEV` stage for a manual validation. Approve or
reject it in Azure DevOps to demonstrate the deployment gate; no Azure subscription or real
deployment is used.

## GitHub

1. Create a repo named `workflow-agent-demo` and push the same starter files to its `main`
   branch. For a no-cost approval-gate demo, make it **public**: GitHub Free only allows
   required-reviewer environment protection on public repositories.
2. In **Settings > Environments**, create an environment named `demo-dev`. Add a required
   reviewer. If you only have one account, leave **Prevent self-review** off; otherwise use
   a second account to approve deployments. Save the protection rules.
3. For the app's API access, create a fine-grained personal access token restricted to this
   repository. Grant **Contents: Read and write**, **Pull requests: Read and write**, and
   **Actions: Read** (plus the default Metadata read access). Store it only in this app's
   Settings, never in the demo repo.
4. In this app's Settings choose **GitHub**. Set repo to `YOUR-USER/workflow-agent-demo`,
   default branch `main`, app folder `app`, workflow `demo-ci.yml`, and deploy job `Deploy
   DEV`. Enter the token and use **Save and test**.

The workflow runs tests on PRs. After a merge to `main`, its `Deploy DEV` job waits for the
`demo-dev` environment approval, then completes without deploying anything. GitHub does not
allow an account to approve its own PR, so use a different GitHub account for the PR review
step if you want to complete the full agent workflow.

## App settings checklist

- Language model: keep the working Gemini configuration and use **Save and test**.
- Jira: site URL, Atlassian email, API token.
- Source control and pipeline: choose exactly one provider per run and fill in its values
  above. The sample code is the same in both repos, but the app runs against one provider
  at a time.
- Use **Save and test** for each configured section. Then run the Jira story key from the
  Run tab. Review and approve the agent-created PR in the hosting service; approve the
  separate DEV gate in the pipeline when it pauses.