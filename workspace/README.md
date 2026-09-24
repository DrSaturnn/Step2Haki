# workspace

The working folder behind the Step2Haki site: the study page source (`index.html`), the tools that edit, check and ship it, and the notes that carry the project between sessions. Start with `CURRENT_STATE.md`.

- Edit the page only through edits files (`tools/EDITS.md`), never by hand or by DOM re-serialization.
- Ship a batch with `tools/ship.sh sNN "<message>"`: it builds `repair/sNN/*.json`, runs the gate, the jsdom render and the vendor-text scan, copies the page to `../discriminator-briefs-site/index.html` (the folder Vercel deploys), commits with a generated summary (also in `CHANGELOG.md`) and pushes when a token is configured.
- Setup after cloning: `npm i` here (jsdom 24).

Question sources are private and stay local. `repair/sources/` and the other paths in `tools/local_only.txt` hold vendor text (UWorld, NBME, Aquifer); they are gitignored, were removed from all history, and travel only as `axbx-local-only.tar.gz`. The page carries paraphrase only.
