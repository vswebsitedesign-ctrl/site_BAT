# AI_READ_THIS_FIRST stale deploy status vs rest of report

Found 2026-07-21 during a deploy request.

AI_READ_THIS_FIRST says:
- live_server: "NOT YET CONFIGURED"
- deploy_command: "SERVER NOT YET CONFIGURED — do not deploy"
- send_php_deploy: "SERVER NOT YET CONFIGURED"

But server / deployment_workflow / build_pipeline sections say:
- server.ip: 217.154.33.12, with working ssh_command
- deployment_workflow.deploy_status: "LIVE — manual rsync via ~/.ssh/github_actions_bat"
- build_pipeline.deploy_command: full rsync command to that same IP
- build_pipeline.deploy_note (dated 2026-07-03) describes a real production
  incident (the --exclude=index.html bug) in this exact deploy command —
  only possible if deploys were already happening in production by then.

Conclusion: AI_READ_THIS_FIRST was written before the server was configured
and never updated when server/deployment_workflow/build_pipeline were filled
in. It is stale, not the other sections.

NOT YET RESOLVED — needs human confirmation that 217.154.33.12 is still the
correct live server before AI_READ_THIS_FIRST is corrected and any deploy
proceeds.
