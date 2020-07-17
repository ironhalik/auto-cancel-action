#!/usr/bin/env python
from github import Github
from datetime import datetime

def main():
    inputs = ActionsContext("input")
    context = ActionsContext("github")
    repo = Github(inputs.access_token).get_repo(context.repository)

    current_run_id = int(context.run_id)
    current_created_at = repo.get_workflow_run(current_run_id).created_at

    if context.event_name == "pull_request":
        current_branch = context.head_ref
    else:
        current_branch = context.ref.replace("refs/heads/", "")

    runs_to_cancel = []
    for run in repo.get_workflow_runs():
        if (
            run.status != "completed"
            and run.id != current_run_id
            and run.head_branch == current_branch
            and run.created_at < current_created_at
        ):
            runs_to_cancel.append(run)

    if runs_to_cancel: 
        for run in runs_to_cancel:
            print(f"Cancelling run id {run.id}")
            run.cancel()
    else:
        print("No runs to cancel.")


class ActionsContext:
    def __init__(self, namespace):
        from os import environ

        if namespace == "input":
            prefix = "INPUT_"
        elif namespace == "github":
            prefix = "GITHUB_"
        else:
            print(f"Context for {namespace} not found.")
            exit(2)

        for env in environ:
            if env.startswith(prefix):
                setattr(self, env[len(prefix):].lower(), environ[env])

        del environ


if __name__ == "__main__":
    main()