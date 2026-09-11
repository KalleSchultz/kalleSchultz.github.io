# Polar Health Data Sync

Automatically pulls your health data (daily activity, exercises, sleep, and
continuous heart rate) from your **Polar** account via the
[Polar AccessLink API](https://www.polar.com/accesslink-api/) and commits it
into this repo as JSON, once a day, via a scheduled GitHub Action. A small
dashboard at `health/index.html` (published at
`https://kalleschultz.github.io/health/` once GitHub Pages rebuilds)
visualizes the latest data.

This only needs to be set up **once**. After that, everything runs
automatically.

## How it works

- `.github/workflows/polar-health-sync.yml` runs daily (and can be triggered
  manually from the **Actions** tab) and executes
  `health/scripts/pull_polar_data.py`.
- The script talks to Polar's AccessLink API using a long-lived access token
  stored as a GitHub Actions secret, fetches anything new since the last run,
  and writes/updates files under `health/data/`.
- If new data was fetched, the workflow commits and pushes it automatically.
- `health/index.html` reads `health/data/summary.json` and renders charts.

Polar's AccessLink API only exposes data **going forward from when you
authorize the app** — it cannot backfill your full historical training
history.

## One-time setup

### 1. Register a Polar AccessLink application

1. Go to <https://admin.polaraccesslink.com/> and sign in with your regular
   Polar Flow account.
2. Click **New application**, give it any name (e.g. "Health Data Sync").
3. Set the **Callback URL** to `http://localhost/callback` (this repo only
   needs it for the one-time manual authorization step below; nothing
   actually needs to be listening on that URL).
4. Save, then copy the **Client ID** and **Client Secret** it gives you.

### 2. Authorize the app against your Polar account (run once, locally)

You need Python 3 with `requests` installed (`pip install requests`).

```bash
export POLAR_CLIENT_ID=your-client-id
export POLAR_CLIENT_SECRET=your-client-secret
python3 health/scripts/setup_polar_auth.py
```

The script will:

1. Print an authorization URL — open it in your browser and log in to Polar
   Flow, then approve access.
2. Polar redirects your browser to
   `http://localhost/callback?code=...` (the page itself won't load, that's
   fine — just copy the full URL, or just the `code` value, from your
   browser's address bar).
3. Paste that URL (or code) back into the terminal when prompted.
4. The script exchanges the code for an access token and registers you as a
   user of the app, then prints:
   - `POLAR_ACCESS_TOKEN`
   - `POLAR_USER_ID`

Polar AccessLink tokens don't expire on a schedule — they stay valid until
you revoke access in Polar Flow (**Settings → Data sharing**) or re-run this
authorization step.

### 3. Add the values as GitHub repository secrets

In this repo on GitHub: **Settings → Secrets and variables → Actions → New
repository secret**, and add:

| Secret name          | Value                              |
| --------------------- | ----------------------------------- |
| `POLAR_ACCESS_TOKEN`  | printed by the script above         |
| `POLAR_USER_ID`       | printed by the script above         |

### 4. Run the sync

Go to the **Actions** tab → **Sync Polar Health Data** → **Run workflow** to
trigger the first sync manually. After that it runs automatically every day.
Once data exists, visit `https://kalleschultz.github.io/health/` to see the
dashboard.

## Notes / troubleshooting

- The AccessLink API is transaction-based for activity, exercise, and
  physical-information data: each sync "checks out" whatever is new since
  the last check, then marks it as read. If a sync run fails **after**
  fetching but **before** committing the transaction, Polar may re-serve the
  same data next time — the script dedupes by date/id so this is harmless.
- If a specific endpoint starts returning errors, check Polar's current
  AccessLink API reference at
  <https://www.polar.com/accesslink-api/#polar-accesslink-api> — Polar
  occasionally adjusts response field names, and the script may need small
  updates to match.
- To stop syncing, either disable/delete the
  `.github/workflows/polar-health-sync.yml` workflow, or revoke access from
  Polar Flow's **Settings → Data sharing** page.
