# Final — q-github-pages

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-github-pages](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-github-pages)

## How to solve (for a teammate)

> The grader only checks that **your exam email** appears in the page's HTML on a `github.io` URL.
> Use the email shown in the question (your IITM login), not a personal Gmail.

Needs a GitHub account. Everything happens in the GitHub web UI, so nothing needs installing.

1. Go to https://github.com/new. Name the repo `tds-portfolio`, set it to **Public**, tick **Add a README file**, click **Create repository**.
   (A private repo can't host Pages on a free account.)
2. In the new repo click **Add file → Create new file**. Name it `index.html` and paste the code below.
   Replace `YOUR-EXAM-EMAIL` with your exam email and `YOUR-GITHUB-USER` with your username. Click **Commit changes**.
   <details><summary>index.html (click to expand)</summary>

   ```html
   <!doctype html>
   <html lang="en">
   <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title>Portfolio</title>
     <style>
       body { max-width: 40rem; margin: 3rem auto; padding: 0 1rem; font-family: Georgia, serif; line-height: 1.6; }
     </style>
   </head>
   <body>
     <h1>Portfolio</h1>
     <p>Coursework and projects for Tools in Data Science (IITM BS).</p>
     <ul>
       <li><a href="https://github.com/YOUR-GITHUB-USER">My GitHub</a></li>
     </ul>
     <!-- The grader looks for this exact address in the page HTML. Keep the email_off comments around it. -->
     <p>Contact: <!--email_off-->YOUR-EXAM-EMAIL<!--/email_off--></p>
   </body>
   </html>
   ```

   </details>

3. Go to **Settings → Pages**. Under **Build and deployment**, set **Source: Deploy from a branch**, **Branch: `main`**, folder **`/ (root)`**, and click **Save**.
4. Wait 1–2 minutes. The **Actions** tab shows a green "pages build and deployment" run, and Settings → Pages shows
   "Your site is live at `https://YOUR-GITHUB-USER.github.io/tds-portfolio/`".
5. Check that the email is in the HTML: open the URL, press Ctrl+U (Mac: Cmd+Opt+U) and search for your email.
   Or run `curl -s https://YOUR-GITHUB-USER.github.io/tds-portfolio/ | grep YOUR-EXAM-EMAIL`, which prints the line with your email.
6. Paste `https://YOUR-GITHUB-USER.github.io/tds-portfolio/` into the answer box, then Check and Save.
   If you just edited the page and Check still fails, add `?v=1` (then `?v=2`, …) to the URL to bypass the cache.

## Final prompt

```text
Write a minimal single-file index.html portfolio page for GitHub Pages. It must contain my email
<EXAM EMAIL> in the HTML, wrapped exactly as <!--email_off--><EXAM EMAIL><!--/email_off-->
(so no CDN obfuscates it). No build step, no external assets. Then give the GitHub web-UI steps to publish
it from a public repo: Settings → Pages → Deploy from a branch → main → / (root).
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

1. Template page: [`src/index.html`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-github-pages/src/index.html). Fill in the two placeholders.
2. Publish it with any of the steps above.
3. Verify with the exam's own fetch path: `curl -s "https://exam.sanand.workers.dev/proxy/<your-pages-url>" | grep -c '<exam email>'` should print ≥ 1.

## Expected output

```
<p>Contact: <!--email_off-->YOUR-EXAM-EMAIL<!--/email_off--></p>
```

## Answer submitted (✅ passed, attempt 1)

```
https://christiano-developer.github.io/t326tdsiitmbs/
```
