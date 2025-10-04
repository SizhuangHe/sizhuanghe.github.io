# Academic Personal Website

**Built on the [Minimal Light Theme](https://github.com/yaoyao-liu/minimal-light) by [Yaoyao Liu](https://www.yaoyaoliu.com/)**

A modern, feature-rich academic homepage with enhanced publication management and automatic Google Scholar integration.

**Live Site:** [sizhuang.org](https://sizhuang.org/)  
**Original Theme:** [Minimal Light by Yaoyao Liu](https://github.com/yaoyao-liu/minimal-light)

[![LICENSE](https://img.shields.io/github/license/yaoyao-liu/minimal-light?style=flat-square&logo=creative-commons&color=EF9421)](https://github.com/yaoyao-liu/minimal-light/blob/main/LICENSE)

## ✨ Key Features

This site extends the [Minimal Light Theme](https://github.com/yaoyao-liu/minimal-light) with powerful new capabilities:

### Enhancements Over Original Theme

- **📊 Automatic Google Scholar Integration** - Daily automated updates of citations, h-index, and publication metrics
- **📄 Automatic CV Compilation** - LaTeX CV automatically compiled to PDF and HTML on every update
- **🏷️ Smart Publication Filtering** - Tag-based filtering system with dynamic search
- **📑 Enhanced Publication Display** - Expandable abstracts, BibTeX, and author lists with smooth animations
- **🎯 Interactive Tagging** - Click tags to filter publications by research area

### Inherited from Minimal Light Theme

- **🌓 Dark Mode Support** - Automatic theme switching based on system preferences
- **📱 Fully Responsive** - Optimized for all devices from mobile to desktop
- **⚡ Fast & Lightweight** - Static site generation with Jekyll
- **🎨 Clean & Professional** - Minimalist academic design

## 📊 Google Scholar Integration

This website automatically fetches and displays your Google Scholar statistics without any manual intervention.

### How It Works

```
Daily (2 AM UTC) or on git push
    ↓
GitHub Actions triggered
    ↓
Python crawler fetches Google Scholar data
    ↓
Data pushed to google-scholar-stats branch
    ↓
Website JavaScript loads data in real-time
    ↓
Visitors see updated stats instantly
```

### What's Displayed

- **Homepage Statistics**: Total citations, H-index, and last update time
- **Per-Publication Citations**: Citation count displayed next to each paper
- **Automatic Timestamps**: Shows when data was last refreshed

### Technical Implementation

Built with [`scholarly`](https://github.com/scholarly-python-package/scholarly) - a Python package that provides clean access to Google Scholar data.

**Key Features:**
- ✅ Proxy support to avoid rate limiting
- ✅ Unbuffered output for real-time GitHub Actions logs  
- ✅ Graceful fallback if Scholar is unavailable
- ✅ 5-minute timeout protection
- ✅ No manual deployment needed

**Files:**
- Crawler: `google_scholar_crawler/simple_crawler.py`
- Workflow: `.github/workflows/update-scholar.yml`
- Data Branch: `google-scholar-stats`

### Setup Instructions

1. Set your Google Scholar ID in `_config.yml`:
   ```yaml
   google_scholar: https://scholar.google.com/citations?user=YOUR_ID_HERE
   ```

2. The workflow automatically extracts your ID and runs daily

3. That's it! Your stats will update automatically every day.

## 📄 Automatic CV Generation

Your CV is **automatically generated and maintained** from your website data using a sophisticated two-stage workflow - ensuring perfect synchronization between your website and CV!

### How It Works

```
Push changes to _data/*.yml or index.md
    ↓
GitHub Actions triggered automatically
    ↓
Stage 1: Data Integration
├─ Scrapes education from _data/education.yml
├─ Scrapes publications from _data/publications.yml  
├─ Scrapes honors from _data/honors.yml
├─ Scrapes services from _data/service.yml
├─ Scrapes research interests from index.md
└─ Creates integrated _data/cv_integrated.yml
    ↓
Stage 2: Multi-Format Generation
├─ Generates LaTeX source (assets/files/cv.tex)
├─ Compiles to PDF (assets/files/cv.pdf)
└─ Jekyll generates HTML webpage (/cv/)
    ↓
Auto-commit back to repository
    ↓
Live website updates automatically
```

### Three CV Formats

1. **📄 PDF Download** - Professional LaTeX-compiled PDF at `/assets/files/cv.pdf`
2. **🌐 HTML Webpage** - Interactive web version at `/cv/` with consistent styling
3. **📝 LaTeX Source** - Editable source code at `/assets/files/cv.tex`

### Data Sources

The CV automatically pulls from:
- **`_data/education.yml`**: Academic background and degrees
- **`_data/publications.yml`**: All publications with proper LaTeX formatting
- **`_data/honors.yml`**: Awards and honors with institutions and years
- **`_data/service.yml`**: Professional service and reviewing activities
- **`index.md`**: Research interests and bio information

### Key Features

- ✅ **Single Source of Truth**: Update once, propagates to all formats
- ✅ **Automatic LaTeX Formatting**: Proper escaping and bibliography formatting
- ✅ **Professional Typography**: LaTeX produces publication-quality PDFs
- ✅ **Consistent Styling**: HTML version matches main website theme
- ✅ **Real-time Updates**: Changes appear immediately after push
- ✅ **Version Control**: All sources and outputs tracked in git
- ✅ **No Manual Maintenance**: Set it once, works forever

### Workflow Files

- **`scripts/generate_cv.py`**: Two-stage Python generator
  - Stage 1: Data scraping and integration
  - Stage 2: LaTeX generation with proper formatting
- **`.github/workflows/compile-cv.yml`**: GitHub Actions automation
  - Triggers on changes to CV-related files
  - Compiles LaTeX to PDF using `xu-cheng/latex-action`
  - Auto-commits generated files back to repository
- **`_data/cv_integrated.yml`**: Intermediate data file (auto-generated)
- **`cv.md`**: Jekyll page template for HTML version

### Manual Testing (Optional)

To test the CV generation locally:

```bash
# Activate the Python environment
conda activate scholar-crawler

# Run Stage 1: Data integration
python scripts/generate_cv.py --stage 1

# Run Stage 2: LaTeX generation  
python scripts/generate_cv.py --stage 2

# Check outputs
ls -la assets/files/cv.*
```

### Customization

**LaTeX Template**: Modify the preamble and commands in `scripts/generate_cv.py`
**HTML Styling**: Edit `_includes/cv.md` for webpage appearance
**Data Structure**: Add new YAML files and update the scraping logic

**Example: Adding a new section**
1. Create `_data/your_section.yml`
2. Add scraping logic to Stage 1 in `generate_cv.py`
3. Add LaTeX formatting to Stage 2
4. Update HTML template in `_includes/cv.md`

## 🎨 Custom Features

### Enhanced Publication System

- **Tag-Based Filtering**: Filter publications by research area with animated transitions
- **Rich Content Display**: 
  - Expandable abstracts with smooth animations
  - One-click BibTeX copying
  - Author list with show more/less functionality
- **Interactive Elements**:
  - Clickable filter tags
  - Year sections that hide when empty
  - Hover effects and visual feedback
  - Filter state persistence via localStorage

### UI/UX Improvements

- **Responsive Layout**: Optimized spacing and containers for all screen sizes
- **Consistent Design**: Unified styling across light and dark modes
- **Smooth Animations**: Slide-down effects for filters and expandable content
- **Theme Colors**: Enhanced link and tag colors matching the overall theme
- **Typography**: Choice between Serif and Sans Serif fonts

## 🚀 Getting Started

### Option 1: Using with GitHub Pages (Recommended)

1. **Fork this repository** or [use it as a template](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template)

2. **Rename** to `your-username.github.io`

3. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` → `/ (root)` → Save

4. **Edit `_config.yml`** with your information:
   ```yaml
   title: Your Name
   position: Ph.D. Student
   affiliation: Your University
   email: yourname (at) university.edu
   google_scholar: https://scholar.google.com/citations?user=YOUR_ID
   ```

5. **Edit `index.md`** with your bio and content

6. **Update `_data/publications.yml`** with your publications

7. **Push to main** - Your site will be live at `https://your-username.github.io`!

### Option 2: Using as a Remote Theme

Add to your `_config.yml`:
```yaml
remote_theme: yaoyao-liu/minimal-light
```

Note: You'll need to copy files you want to customize to your own repository.

### Option 3: Running Locally

**Prerequisites**: Ruby and Jekyll ([installation guide](https://jekyllrb.com/docs/installation/))

```bash
# Clone the repository
git clone https://github.com/your-username/your-username.github.io.git
cd your-username.github.io

# Install dependencies
bundle install
bundle add webrick

# Serve locally
bundle exec jekyll server

# View at http://localhost:4000
```

## 📁 Project Structure

```
.
├── _config.yml                      # Site configuration
├── index.md                         # Homepage content
├── cv.md                           # CV webpage template
│
├── _data/
│   ├── publications.yml             # Publications database
│   ├── education.yml               # Education and degrees
│   ├── honors.yml                  # Awards and honors
│   ├── service.yml                 # Professional service
│   └── cv_integrated.yml           # Auto-generated CV data
│
├── _includes/
│   ├── publications.md              # Publications section
│   ├── selected-publications.md     # Featured publications
│   ├── scholar-stats.md             # Google Scholar stats widget
│   ├── services.md                  # Service & activities
│   └── cv.md                       # CV HTML template
│
├── _layouts/
│   └── homepage.html                # Main page template
│
├── _sass/
│   ├── minimal-light.scss           # Main stylesheet
│   └── minimal-light-no-dark-mode.scss
│
├── assets/
│   ├── css/                         # Compiled CSS
│   ├── img/                         # Images & avatars
│   ├── files/                       # CV and documents
│   │   ├── cv.pdf                   # Auto-generated CV PDF
│   │   └── cv.tex                   # Auto-generated LaTeX source
│   └── js/                          # JavaScript
│
├── scripts/
│   ├── generate_cv.py               # Two-stage CV generator
│   └── requirements.txt             # Python dependencies
│
├── google_scholar_crawler/
│   ├── simple_crawler.py            # Main crawler script
│   ├── requirements.txt             # Python dependencies
│   └── results/                     # Cached data
│
└── .github/
    └── workflows/
        ├── update-scholar.yml       # Scholar stats automation
        └── compile-cv.yml           # CV generation automation
```

## ⚙️ Configuration

### Basic Information

Edit `_config.yml`:

```yaml
# Basic Information 
title: Your Name
position: Ph.D. Student
affiliation: Your University
email: yourname (at) example.edu

# Links
google_scholar: https://scholar.google.com/citations?user=YOUR_ID
cv_link: assets/files/curriculum_vitae.pdf
github_link: https://github.com/username
linkedin: https://www.linkedin.com/in/username/
twitter: https://twitter.com/username

# Images
avatar: ./assets/img/avatar.png
favicon: ./assets/img/favicon.png
favicon_dark: ./assets/img/favicon-dark.png

# Options
enable_footnote: true
auto_dark_mode: true
font: "Serif"  # or "Sans Serif"
```

### Adding Publications

Edit `_data/publications.yml`:

```yaml
- title: "Your Paper Title"
  authors: "Author 1, <strong>Your Name</strong>, Author 3"
  conference_short: "ICML"
  conference: "International Conference on Machine Learning <strong>(ICML)</strong>, 2024"
  pdf: ./assets/papers/paper.pdf
  code: https://github.com/username/project
  page: https://project-page.com
  bibtex: ./assets/bibs/paper.txt
  image: ./assets/img/paper-preview.png
  notes: Oral Presentation
  tags:
    - Machine Learning
    - Computer Vision
```

### Styling

- **Custom CSS**: Edit `_sass/minimal-light.scss`
- **Layout Changes**: Edit `_layouts/homepage.html`
- **Color Scheme**: Modify CSS variables in the SCSS file

## 🛠️ Advanced Customization

### Google Scholar Crawler Setup

If you want to modify the crawler behavior:

1. **Local Testing**:
   ```bash
   cd google_scholar_crawler
   conda create -n scholar-crawler python=3.9
   conda activate scholar-crawler
   pip install -r requirements.txt
   GOOGLE_SCHOLAR_ID=your_id python simple_crawler.py
   ```

2. **Modify Crawler** (`simple_crawler.py`):
   - Add more metrics
   - Change update frequency
   - Customize data format

3. **Update Workflow** (`.github/workflows/update-scholar.yml`):
   - Change schedule (default: daily at 2 AM UTC)
   - Modify timeout settings
   - Add notifications

### Disabling Features

**Disable Dark Mode**:
```yaml
auto_dark_mode: false
```

**Disable Google Scholar Stats**:
Remove or comment out the `loadScholarStats()` call in `_layouts/homepage.html`

**Disable Publication Tags**:
Remove the tags section from publications in `_data/publications.yml`

## 📝 Content Management

### Writing Content

Both Markdown and HTML are supported in:
- `index.md` - Your main homepage content
- `_includes/*.md` - Section includes
- `_data/publications.yml` - Publication metadata

### Including Files

In `index.md`, you can include sections:

```markdown
{% include_relative _includes/publications.md %}
{% include_relative _includes/services.md %}
```

Remove these lines if you don't need those sections.

## 🔧 Troubleshooting

### Google Scholar Stats Not Showing

1. Check that your Google Scholar ID is correct in `_config.yml`
2. View the GitHub Actions workflow run logs
3. Check if the `google-scholar-stats` branch exists
4. Verify the data files exist in that branch

### Crawler Timeout

If the crawler times out:
- Increase timeout in `.github/workflows/update-scholar.yml`
- The workflow will retry on the next scheduled run
- Data will fallback to previous values

### Local Development

If `bundle exec jekyll server` fails:
```bash
bundle update
bundle add webrick
```

## 📄 License

This work is licensed under a [Creative Commons Zero v1.0 Universal](https://github.com/yaoyao-liu/minimal-light/blob/master/LICENSE) License.

## 🙏 Acknowledgements

**This website is built on top of the [Minimal Light Theme](https://github.com/yaoyao-liu/minimal-light) created by [Yaoyao Liu](https://www.yaoyaoliu.com/).**

### Additional Credits

- [scholarly](https://github.com/scholarly-python-package/scholarly) - Python package for Google Scholar data access
- [pages-themes/minimal](https://github.com/pages-themes/minimal) - Original minimal theme
- [orderedlist/minimal](https://github.com/orderedlist/minimal) - Minimal theme inspiration
- [al-folio](https://github.com/alshedivat/al-folio) - Academic Jekyll theme inspiration

## 📮 Contact

For questions or issues, please [open an issue](https://github.com/SizhuangHe/sizhuanghe.github.io/issues) or visit my website at [sizhuang.org](https://sizhuang.org/).

---

**Other Languages:** [简体中文](https://github.com/yaoyao-liu/minimal-light/blob/master/README_zh_Hans.md) | [繁體中文](https://github.com/yaoyao-liu/minimal-light/blob/master/README_zh_Hant.md) | [Deutsche](https://github.com/yaoyao-liu/minimal-light/blob/master/README_de.md)
