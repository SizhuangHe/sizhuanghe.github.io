# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic personal homepage built on Jekyll: a single-page design ("Denoise") with Google Scholar numbers that update automatically.

**Live Site:** https://sizhuang.org
**GitHub Pages:** Deploys from `main` branch at root

## Homepage: "Denoise" design

The site is a single page, `index.html` (layout `_layouts/denoise.html`, sections in
`_includes/denoise/`, styles `assets/css/denoise.css`, behaviour `assets/js/denoise.js`).
`cv.md`, `publications.md` and `beyond.md` are kept in git but excluded from the build
(`exclude:` in `_config.yml`). `/cv/` and `/publications/` are redirect stubs in
`redirects/`. Content still comes from data, so routine edits never touch the design:

- About: research prose first, then the education timeline `_data/about_timeline.yml` (newest first, drawn like News). Research prose:
  `_includes/about.md` (Markdown). Hero thesis, position line, advisor: `_config.yml`.
  Hero method blurbs (under the "sampled via …" readout, one per generation style): `_data/hero_methods.yml`.
- News: `_data/news.yml` (newest first; the first 4 show, the rest fold under "N earlier").
- Papers: `_data/publications.yml`. Homepage-only fields: `topics` (keys from `_data/topics.yml`,
  drive the filter chips), `thumb` (animated thumbnail key from `_data/thumbnails.yml`; omit it and
  the paper shows `image`), `image_size` (`WxH` of `image`), `tagline` (one-line summary shown in
  § Selected), `venue` (optional display label; otherwise `conference`, or "Preprint YEAR").
  `selected: true` puts a paper in § Selected. Full-list order: year of `date` (newest first),
  accepted before preprints, then file order.
- Open Source: `_data/projects.yml` (name, description, github; shown in file order).
- Service: `_data/service.yml`. Scholar numbers load live from the `google-scholar-stats` branch;
  `_data/scholar.yml` is only the build-time fallback.
- CV link: `/assets/files/cv.pdf` (`cv_pdf` in `_config.yml`). The HTML CV data
  (`_data/cv_integrated.yml`) is hand-maintained; do not run `scripts/generate_cv.py`.

## Key Commands

### Local Development
```bash
# Install dependencies (first time only)
bundle install
bundle add webrick

# Serve the site locally at http://localhost:4000
bundle exec jekyll server
```

### Google Scholar Crawler (Local Testing)
```bash
cd google_scholar_crawler
conda create -n scholar-crawler python=3.9
conda activate scholar-crawler
pip install -r requirements.txt
GOOGLE_SCHOLAR_ID=5biMMmIAAAAJ python simple_crawler.py
```

## Architecture Overview

### Google Scholar Integration

**Data Flow:**
1. GitHub Actions runs weekly (Sundays 2 AM UTC) or on push to `main`
2. `google_scholar_crawler/simple_crawler.py` fetches data using the `scholarly` library
3. Results saved to `google-scholar-stats` branch as JSON
4. Website JavaScript loads data in real-time from that branch

**Files:**
- Crawler: `google_scholar_crawler/simple_crawler.py`
- Workflow: `.github/workflows/update-scholar.yml`
- Data Branch: `google-scholar-stats` (separate branch)
- Display: `_includes/scholar-stats.md` (homepage widget)

**Configuration:** Google Scholar ID is set in workflow at line 51: `GOOGLE_SCHOLAR_ID: "5biMMmIAAAAJ"`

### Publication System

**Data Source:** `_data/publications.yml`

Each publication has:
```yaml
title: "Paper Title"
authors: "Author 1<sup>*</sup>, <b><u>Your Name</u></b>, Author 3"
conference_short: "NeurIPS"
conference: "NeurIPS 2025 (Poster)"
pdf: https://arxiv.org/pdf/...
code: https://github.com/...
bibtex: ./assets/bibs/paper.txt
image: ./assets/img/paper.png
tags: ["Tag1", "Tag2"]
selected: true  # For featured publications
summary: "One-line summary"
full_abstract: "Full abstract text"
```

**Publication Classification:** The CV generator automatically categorizes publications (in `stage1_scrape_data()`):
- **Conference:** Default category
- **Workshop:** If "workshop" in conference name/short name
- **Preprint:** If "arxiv", "biorxiv" in conference, or "preprint" in notes

**Display Components:**
- `_includes/publications.md`: Full publication list with filtering
- `_includes/selected-publications.md`: Featured publications only
- `assets/css/publications.css`: Styling for tags, filters, and animations

**Interactive Features:**
- Tag-based filtering with localStorage persistence
- Expandable abstracts and BibTeX
- Author list show more/less functionality
- Year sections that hide when filtered out

## Common Development Workflows

### Adding a New Publication

1. Edit `_data/publications.yml` - add entry to `main:` list
2. Add BibTeX file to `assets/bibs/`
3. Add thumbnail image to `assets/img/`
4. Push to `main` branch

### Troubleshooting GitHub Actions

**Scholar Workflow:** Check `.github/workflows/update-scholar.yml`
- Timeout after 5 minutes is normal if Google Scholar is blocking
- Falls back to existing data from `google-scholar-stats` branch
- Data updates appear on website immediately (no rebuild needed)
