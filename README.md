# Step2Haki

Discriminator Briefs — Family Medicine Shelf / USMLE Step 2 CK.

Live: https://step2haki.vercel.app

## What this is

A single self-contained HTML study reference: 88 briefs across 12 systems.
Each system carries Part I diagnosis-fork briefs, then a board-style
sub-band of NBME next-step briefs.

## Structure

- `discriminator-briefs-site/index.html` — the whole document. No build step,
  no dependencies, no external assets. Vercel serves it as-is.

  ## Updating

  Push a change to `index.html` on `main`. Vercel redeploys automatically and
  the live URL always reflects the newest commit.

  ## Caveat

  Assembled from question-based study sessions. Clinical content reflects
  standard board material and is unverified against primary sources except
  where noted. Guideline-dependent figures — screening intervals, vaccine
  schedules, treatment thresholds — change. Check USPSTF, ACIP/CDC, or the
  relevant specialty society before relying on anything here clinically.
  Study aid, not a clinical reference.
  
