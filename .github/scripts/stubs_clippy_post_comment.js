module.exports = async ({ github, context }) => {
  const fs = require('fs')
  const DIFF_LINE = { ">": true, "<": true }

  let data = fs.readFileSync('stubs_clippy_errors.txt', { encoding: 'utf8' })
  // posting comment fails if too long, so truncate
  if (data.length > 30000) {
    let truncated_data = data.substring(0, 30000)
    let lines_truncated = data.split('\n').length - truncated_data.split('\n').length
    data = truncated_data + `\n\n... (truncated ${lines_truncated} lines) ...\n`
  }

  const body = data.trim()
    ? '🚩🚩 Stubs clippy found the following red flags for this PR: \n```\n' + data + '\n```'
    : '✅ Stubs clippy found no red flags for this PR!'
  const issue_number = parseInt(fs.readFileSync("pr_number.txt", { encoding: "utf8" }))
  await github.rest.issues.createComment({
    issue_number,
    owner: context.repo.owner,
    repo: context.repo.repo,
    body
  })

  return issue_number
}
