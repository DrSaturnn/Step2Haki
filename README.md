# Step2Haki

Clinical board briefs for USMLE Step 2 CK and the clerkship shelves.

**Live: https://step2haki.vercel.app**

## What this is

A study reference built the other way round from a textbook. Each brief starts
from the decision a question actually turns on — the one finding that separates
two diagnoses, or the trigger that licenses the next step — and works outward
from there. Disease description that would not change an answer is left out.

Every brief carries the same spine:

- **the decision point** — the fork, and the word or finding that settles it
- **defining criteria**, when the question turns on a stated threshold
- **a mimics table or a management ladder**, whichever the question earns
- **a decision spine** — the questions to ask the stem, in collapse order
- **a scenario bank** of variants that each change the answer
- **the traps**, named by the mechanism that makes them tempting
- **a transferable rule** — what to carry to a question you have not seen

Briefs cross-link: where two topics share a complaint and diverge on one
finding, each names the other and stores the discriminator as a question.

## Using it

**Shelves.** Step 2 pools everything; each shelf narrows it to what that
clerkship tests. The choice is in the sidebar and travels in the URL —
`?shelf=peds` opens there, so a shared link lands where you meant it to. Shelves
are added as they are written.

**Study mode** masks the answer column, the transferable rules and the criteria
definitions, so a brief becomes something to answer rather than something to
read. Tables reveal as you work down them.

**Scenario banks** toggle between Review and Quiz. Review shows the whole chain;
Quiz turns each item into a question with the prompt the exam would use.

**Review** puts five briefs in front of you at a time, in study mode, chosen by
a spaced schedule — briefs you know come back at widening intervals, briefs you
miss come back tomorrow. Mark each one and it reschedules itself. There is also
a quiz mode that interleaves questions with no surrounding brief, for cold
retrieval.

**Profiles** keep schedules apart when several people use the same link, and
sync across devices, so the phone and the laptop stay on the same rotation. A
backup code is available for anything the sync cannot reach.

## Structure

```
discriminator-briefs-site/
  index.html          the whole study page — no build step, no dependencies
  api/progress.js     sync endpoint; without it the page runs on local storage
  DEPLOY.md           setup and update notes
```

## Updating

Push to `main` and Vercel redeploys. Progress lives outside the deployment, so
no upload can disturb it, and new briefs join the review rotation on their own.

One rule: **never rename a brief's id.** Ids are how deep links, cross-links and
everyone's review history find a brief. Move briefs between systems freely.

## Caveat

Assembled from question-based study sessions. Clinical content reflects standard
board material and is unverified against primary sources except where noted.
Guideline-dependent figures — screening intervals, vaccine schedules, treatment
thresholds — change. Check USPSTF, ACIP/CDC, or the relevant specialty society
before relying on anything here clinically.

A study aid, not a clinical reference.
