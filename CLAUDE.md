# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic personal homepage built on Jekyll using the [Minimal Light Theme](https://github.com/yaoyao-liu/minimal-light). The site features automatic Google Scholar integration, automated CV generation, and an enhanced publication filtering system.

**Live Site:** https://sizhuang.org
**GitHub Pages:** Deploys from `main` branch at root

## Key Commands

### Local Development
```bash
# Install dependencies (first time only)
bundle install
bundle add webrick

# Serve the site locally at http://localhost:4000
bundle exec jekyll server
```

### CV Generation (Local Testing)
```bash
# Activate Python environment
conda activate scholar-crawler

# Run full two-stage workflow
python scripts/generate_cv.py

# Run individual stages
python scripts/generate_cv.py --stage 1  # Data integration
python scripts/generate_cv.py --stage 2  # LaTeX generation
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

### Automated CV System (Two-Stage Workflow)

The site features a sophisticated CV generation system that maintains perfect synchronization between website data and CV outputs:

**Stage 1: Data Integration** (`scripts/generate_cv.py --stage 1`)
- Scrapes data from `_data/publications.yml`, `_data/education.yml`, `_data/honors.yml`, `_data/service.yml`, and `index.md`
- Integrates into `_data/cv_integrated.yml` (auto-generated, single source of truth)

**Stage 2: LaTeX/PDF Generation** (`scripts/generate_cv.py --stage 2`)
- Reads `_data/cv_integrated.yml`
- Generates `assets/files/cv.tex` (LaTeX source)
- GitHub Actions compiles to `assets/files/cv.pdf`

**HTML CV:** Jekyll automatically generates the HTML version at `/cv/` from `cv.md` template using `_data/cv_integrated.yml`

**Trigger:** GitHub Actions workflow (`.github/workflows/compile-cv.yml`) runs automatically when any of these files change:
- `_config.yml`
- `_data/publications.yml`
- `_data/education.yml`
- `_data/honors.yml`
- `_data/service.yml`
- `index.md`
- `scripts/generate_cv.py`

**Critical Functions in `scripts/generate_cv.py`:**
- `stage1_scrape_data()`: Collects and normalizes data from website YAML files
- `stage2_generate_latex()`: Generates LaTeX with proper escaping and formatting
- `format_authors()`: Handles author list abbreviation, highlighting, and "et al." logic
- `abbreviate_name()`: Converts "First Middle Last" to "F. M. Last"
- `escape_latex()`: Escapes special LaTeX characters, decodes HTML entities

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

### Jekyll Structure

**Theme:** Uses `remote_theme: yaoyao-liu/minimal-light` (specified in `_config.yml`)

**Key Configuration:** `_config.yml` contains:
- Basic info (name, position, affiliation, email)
- Social links (Google Scholar, GitHub, LinkedIn, Twitter)
- Theme options (dark mode, font choice)

**Content Files:**
- `index.md`: Homepage content (uses `_includes/*.md` for sections)
- `cv.md`: CV page template (renders from `_data/cv_integrated.yml`)

**Data Files:**
- `_data/publications.yml`: Publications database
- `_data/education.yml`: Education entries
- `_data/honors.yml`: Awards and honors
- `_data/service.yml`: Professional service activities
- `_data/cv_integrated.yml`: Auto-generated, do not edit manually

**Layouts:**
- `_layouts/homepage.html`: Main page layout

**Styling:**
- `_sass/minimal-light.scss`: Main stylesheet (from theme)
- `assets/css/publications.css`: Custom publication styling

## Important Implementation Details

### Author Name Processing

The CV generator includes sophisticated author name handling:
- Abbreviates first/middle names to initials (e.g., "John Smith" → "J. Smith")
- Handles name particles (de, van, von, etc.) correctly
- Highlights your name with underline and bold in LaTeX: `\underline{\textbf{...}}`
- Highlights your name with custom CSS class in HTML: `<span class="cv-me">...</span>`
- Implements smart "et al." logic: includes all authors up to and including your name and any starred (*) co-first authors

### LaTeX Escaping

Critical for CV generation - `escape_latex()` function handles:
1. HTML entity decoding (&#58; → :, &amp; → &, etc.)
2. Special character escaping (&, %, $, #, _, {, }, ~, ^, \)
3. Proper handling of HTML tags in publication data

### Data Normalization

`_data/education.yml` supports flexible detail format:
```yaml
details:
  - label: "Advisor"
    value: "Dr. Name"
  - label: "Research Focus"
    value: "Machine Learning"
```

The scraper normalizes this to `[(label, value)]` tuples for consistent processing.

## Common Development Workflows

### Adding a New Publication

1. Edit `_data/publications.yml` - add entry to `main:` list
2. Add BibTeX file to `assets/bibs/`
3. Add thumbnail image to `assets/img/`
4. Push to `main` branch
5. GitHub Actions automatically updates CV (LaTeX, PDF, and HTML)

### Modifying CV Format

**LaTeX CV:** Edit `stage2_generate_latex()` in `scripts/generate_cv.py`
- Preamble: Lines 346-512 (LaTeX packages, commands, formatting)
- Sections: Lines 519-584 (header, education, publications, etc.)

**HTML CV:** Edit `cv.md` and `_includes/cv.md`

**Data sources:** Edit corresponding YAML files in `_data/`

### Testing CV Changes Locally

1. Make changes to data files or `generate_cv.py`
2. Run `python scripts/generate_cv.py`
3. Check `_data/cv_integrated.yml` (intermediate data)
4. Check `assets/files/cv.tex` (LaTeX source)
5. To compile PDF locally: `pdflatex assets/files/cv.tex` (requires LaTeX installation)

### Troubleshooting GitHub Actions

**CV Workflow:** Check `.github/workflows/compile-cv.yml`
- Stage 1 failures: Usually YAML parsing errors in data files
- Stage 2 failures: LaTeX escaping issues or malformed data
- PDF compilation failures: LaTeX syntax errors in generated `.tex` file

**Scholar Workflow:** Check `.github/workflows/update-scholar.yml`
- Timeout after 5 minutes is normal if Google Scholar is blocking
- Falls back to existing data from `google-scholar-stats` branch
- Data updates appear on website immediately (no rebuild needed)

## File Dependencies

**When you edit `_data/publications.yml`:**
- Affects: Homepage publication list, CV (all formats), publication filters
- Triggers: CV workflow → regenerates `cv_integrated.yml`, `cv.tex`, `cv.pdf`

**When you edit `_data/education.yml`, `_data/honors.yml`, `_data/service.yml`:**
- Affects: CV (all formats)
- Triggers: CV workflow

**When you edit `index.md`:**
- Affects: Homepage content, research interests in CV
- Triggers: CV workflow (scrapes research interests section)

**When you edit `_config.yml`:**
- Affects: Site-wide configuration, CV header
- Triggers: CV workflow
