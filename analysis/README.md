What this folder contains

- `50_videos.csv` — compiled dataset of Nate B. Jones' 50 most-recent video titles (Substack + YouTube search links) for analysis.

Notes
- Source material pulled from Nate's Substack feed, his YouTube channel and public search results.
- Some entries are mapped to Substack posts (where Nate publishes the long-form article + video); others use a YouTube search URL when the direct watch ID wasn't available in the scrape.

Next steps
1. Expand rows with exact YouTube watch IDs + transcripts.
2. Produce 250 categorized insights using this dataset.
3. Build runnable agent prompts, SOPs, and Policy Forge templates and integrate into `policy/` and `agents/`.

To regenerate the dataset automatically, run the fetch script (coming soon).
