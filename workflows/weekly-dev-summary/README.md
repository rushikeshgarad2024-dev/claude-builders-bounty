# n8n + Claude Code: Weekly Dev Summary Workflow

Automated workflow that aggregates GitHub commits, closed issues, and merged PRs every week, synthesizes them into an executive narrative using the Claude API (`claude-sonnet-4-20250514`), and broadcasts the summary to Discord, Slack, or Email.

## Quick Setup (5 Steps)

1. **Import Workflow**: Open your n8n dashboard -> Click **Import from File** -> Select `workflows/weekly-dev-summary/weekly-summary.json`.
2. **Configure Variables**: In the **Set Config Variables** node, set:
   - `owner`: GitHub repo owner
   - `repo`: GitHub repo name
   - `language`: `EN` or `FR`
   - `webhookUrl`: Discord/Slack Webhook URL
3. **Set Credentials**: Add your **GitHub Personal Access Token** and **Anthropic Claude API Key** to n8n credentials.
4. **Test Run**: Click **Test Step** on the trigger to verify live GitHub fetching and summary generation.
5. **Activate**: Toggle workflow to **Active**. It will automatically trigger every Friday at 5:00 PM!
