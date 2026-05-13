Promotion Process (detailed)

When an agent branch contains changes that modify behaviour, skills, or shared documentation, follow this process:

1. The agent branch PR will cause CI to create a promotion PR to main.
2. The promotion PR should be reviewed by owners of shared components (CODEOWNERS will help route reviewers).
3. If accepted, merge the promotion PR into main.
4. CI will automatically attempt to push/sync the main changes back into the agent branches.

If automatic sync fails, maintainers should manually apply the changes to agent branches and merge.
