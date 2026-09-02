# Day 4 Hands-On Lab: Reusable Workflows, Composite Actions & OIDC

A small, real project — push this to your own GitHub repo and watch it run in the
Actions tab. Nothing here is simulated; every workflow actually executes.

## What's in here

- `app.py` / `test_app.py` — a trivial app with tests, just so the pipeline has
  something real to build/test.
- `.github/actions/setup-python-env/action.yml` — a **composite action**: wraps
  "set up Python" + "install deps" into one reusable step.
- `.github/workflows/reusable-build.yml` — a **reusable workflow**: triggers on
  `workflow_call` only, never runs on its own. Uses the composite action above.
- `.github/workflows/ci.yml` — the normal, push/PR-triggered workflow that
  **calls** the reusable workflow, plus a couple of jobs designed to make the
  parallel-vs-sequential behavior visible, plus a job that inspects a real OIDC
  token.

## Step 1 — Get it into a real GitHub repo

1. Go to github.com, create a new **empty** repository (no README/gitignore),
   e.g. `day4-github-actions-lab`. Keep it public or private, either works.
2. In Terminal, from this folder:
   ```bash
   cd day-04-github-actions
   git init
   git add .
   git commit -m "Day 4 hands-on lab"
   git branch -M main
   git remote add origin https://github.com/<your-username>/day4-github-actions-lab.git
   git push -u origin main
   ```
3. Open the repo on GitHub and click the **Actions** tab. You should see the
   `CI` workflow already running from that push.

## Step 2 — Watch what actually happens

Click into the running workflow. You should see four jobs: `build`,
`lint-placeholder`, `notify`, `inspect-oidc-token`.

- Notice `build` has no visible "steps" of its own in the job list the way
  `lint-placeholder` does — instead it shows the reusable workflow's *own*
  jobs nested underneath it. That's Day 4's point made visible: the call
  itself IS the job.
- Notice `lint-placeholder` starts immediately, at the same time as `build` —
  they're not sequenced.
- Notice `notify` doesn't start until `build` (the whole reusable workflow)
  finishes — that's `needs:` in action.
- Open `inspect-oidc-token`'s log and find "Decoded OIDC token claims" — you'll
  see real JSON with fields like `repository`, `ref`, `workflow`, `sub`, and
  `aud`. That `sub` claim is exactly what an AWS IAM trust policy or Azure
  federated credential checks before handing out temporary credentials. You're
  looking at the actual mechanism from Day 4, not a diagram of it.

## Step 3 — Exercises (do these in order, one commit each)

1. **Change a variable and watch the diff propagate.** In `ci.yml`, change
   `python-version: "3.12"` to `"3.11"`. Commit, push, and watch the reusable
   workflow's log show it actually set up 3.11 — proving inputs really flow
   from caller to reusable workflow.

2. **Break the composite action on purpose.** In
   `.github/actions/setup-python-env/action.yml`, temporarily change
   `pip install -r requirements.txt` to `pip install -r requirements-typo.txt`.
   Push, watch it fail, read the error, then fix it. This is what a broken
   shared action looks like from the calling workflow's point of view — useful
   to have seen once before an interview asks you to debug it verbally.

3. **See a red pipeline, and see `needs:` block on failure.** In
   `test_app.py`, uncomment the `test_this_will_fail` function. Push. Confirm:
   `build` turns red, and `notify` never runs at all (not even a failed run —
   it's skipped). This is `needs:` enforcing "don't proceed past a failure,"
   the same principle from Day 1's manual-gate discussion. Re-comment it after.

4. **SHA-pin an action (Day 4's hardening practice).** Go to
   github.com/actions/checkout, find the commit SHA for the tag you're using
   (`v4`), and replace `uses: actions/checkout@v4` with
   `uses: actions/checkout@<full-sha>` in both workflow files. Push, confirm it
   still runs identically. In an interview, be ready to explain *why* this is
   more secure than the tag (a tag can be moved to point at different code
   later; a SHA can't).

5. **Least-privilege permissions.** Right now `inspect-oidc-token` requests
   `id-token: write` and `contents: read`. Try removing `id-token: write`
   entirely, push, and watch the curl step fail because there's no token to
   request. This is the concrete version of "you must declare `id-token:
   write` or OIDC has nothing to hand you."

6. **Stretch goal, once you have an AWS account:** replace the
   `inspect-oidc-token` job's curl step with a real
   `aws-actions/configure-aws-credentials@v4` step pointing at an IAM role
   whose trust policy's `sub` condition matches this exact repo. This is the
   full Day 4 OIDC flow, now actually assuming a role instead of just reading
   its own token. Good candidate for revisiting after your Terraform/AWS
   certification study — you'll have somewhere to create that IAM role from.

## Why this is worth doing beyond just reading Day 4 again

Every one of Day 4's flashcard answers has a concrete, visible artifact here:
the reusable workflow's separate `workflow_call` trigger, the composite
action's wrapped steps, the real decoded OIDC claims, the `needs:` gate
blocking on failure, and a SHA-pinned action. If an interviewer asks you to
sketch any of this on a whiteboard, you'll be describing something you've
actually watched run, not something you memorized.
