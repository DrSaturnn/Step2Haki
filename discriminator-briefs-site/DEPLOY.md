# Deploying AxBx with cross-device sync

Upload the **`discriminator-briefs-site` folder**, not the single file. Vercel
serves `index.html` at the root and turns `api/progress.js` into a function at
`/api/progress`.

```
discriminator-briefs-site/
  index.html          the study page
  api/progress.js     read/write one person's schedule — no dependencies
  DEPLOY.md           this file (ignored by Vercel)
```

**The folder name matters.** The project's *Root Directory* was set to
`discriminator-briefs-site`, with *"Skip deployments when no changes to root
directory"* enabled — so a folder with a different name can be **silently
skipped**: no error, page unchanged, and it looks like it worked. The folder is
named to match. If you ever clear the Root Directory setting instead, the name
stops mattering.

## Check it worked — five seconds, every deploy

Open **`/api/progress`** on the live site:

| What you see | What it means |
|---|---|
| `{"names":[...]}` | Function is live and storage is connected. Done. |
| `{"error":"Storage is not connected yet…"}` | Function deployed; add the Upstash integration. |
| A 404 | The `api/` folder did not make it — you uploaded the file, not the folder. |

## Updating later

1. Keep this folder on your machine as the canonical copy.
2. Drop each new `index.html` into it, replacing the old one.
3. Re-upload the **whole folder**.

`api/progress.js` never changes when content changes, and **progress lives in
Upstash, not in either file** — so no deploy, however botched, can overwrite
anyone's schedule. The worst case is that `api/` goes missing and sync stops
until you re-upload; the data waits in Redis.

## One-time: connect storage

1. Vercel dashboard → your project → **Storage** → **Browse Marketplace**
2. Add **Upstash** → create a Redis database (free tier is ample — the whole
   thing is a few KB per person) → connect it to the project
3. Redeploy once so the function picks up the injected credentials

The function reads `KV_REST_API_URL` / `KV_REST_API_TOKEN`, and falls back to
`UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN`. The integration injects
one of those pairs; you do not set anything by hand.

## Until you do that

Nothing breaks. The page falls back to per-browser storage and says so in the
review panel: *"Saved on this device only."* **The same `index.html` works with
or without the backend** — uploading the file alone is still a valid deploy.

## What is stored

Which briefs a person has reviewed, the Leitner box each sits in, and when each
is next due. Per name. No scores, no answers, no email.

## The PIN

Optional, and not security — it is labelled that way in the UI. It stops someone
typing a name that already exists and overwriting that person's schedule. Reads
stay open. A wrong PIN refuses the write and the device keeps its local copy;
nothing is destroyed.

## How two devices reconcile

Per brief, whichever device reviewed it more recently wins — recovered from the
stored due date minus that box's interval, so it is evidence rather than a guess.
Dates are day-granular, so a same-day tie goes to the **lower box**: when the
evidence is equally recent, trust the weaker result.

**The merge runs on write, not only on read.** Without that the store would be
last-write-wins over the whole schedule, and a phone that had not refreshed
would erase a laptop's work on its next push. The server merges, stores, and
returns the merged view so the pusher stops being stale. Push order does not
matter, and merging twice changes nothing.

## Limits built in

- **50 profiles** per link. The endpoint is public and a public page can hold no
  secret, so a roster cap is the only real brake on junk names.
- **64 KB / 2,000 entries** per schedule (the library is 152 briefs).
- A PIN, once set, guards writes **and** removal. A wrong PIN refuses and
  destroys nothing.

## Removing a profile

The panel offers *Remove here* (this browser) and *Remove everywhere* (also drops
it from the shared list). It shows your export code first — removal is the one
action with no undo.

## If the database is down

Reviews still run, marks still save locally, and the panel reports the outage.
The next successful push carries the backlog up. The sync layer is wrapped so
that it cannot break the page even if `fetch` itself is unavailable.

## Adding content later

Progress is keyed on each brief's **id**, and the review pool is enumerated from
the page at load time. So when you add briefs and re-upload:

- every existing schedule survives untouched;
- new briefs appear in the pool immediately, counted as unseen, and enter the
  rotation with no migration step;
- a brief you remove leaves a harmless orphan record that is never offered,
  because the pool decides what can be reviewed.

Verified by test: adding two briefs took the pool from 152 to 154, left all
existing boxes intact, and both new briefs showed up as due.

**The one thing that would break it is renaming an id.** A renamed brief orphans
its own progress and comes back as unseen. Ids were already permanent because
they are the deep-link and cross-reference surface; they now also carry everyone's
review history. Move a brief between systems freely — never rename it.

## Sync is optional

The same `index.html` works with or without the backend. Skip the Upstash step and
the page simply runs on per-browser storage, says *"Saved on this device only"*, and
the `AXBX2.…` code is how progress moves between devices. Add Upstash whenever you
want it and nothing else changes — profiles already on a device push up on the next
review. Deploying the folder either way is harmless: an unconnected `api/progress`
returns a plain message, not an error page.

## If the sync store is lost

Nothing on your devices is lost with it. Each browser keeps its own working copy,
and the panel detects that the store no longer knows the profile and offers
**Restore it to sync** — one click puts your schedule back. The backup code is
the fallback for the case where no device has a copy either.
