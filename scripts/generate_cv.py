#!/usr/bin/env python3
"""
Generate CV from website data - Three-stage workflow
Stage 1: Scrape data from website YAML files to one integrated YAML file
Stage 2: Generate LaTeX CV from the integrated YAML file
Stage 3: Generate HTML CV using template system (similar to publications.md)
"""

import os
import yaml
import re
import html
from datetime import datetime
import argparse

def load_yaml(filepath):
    """Load YAML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_yaml_optional(filepath, default=None):
    """Load YAML file if it exists, else return default"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data is None:
                return default if default is not None else {}
            return data
    return default if default is not None else {}

def _strip_html(s: str) -> str:
    s = re.sub(r'<[^>]+>', '', s or '')
    return html.unescape(s).strip()

def ensure_yaml(path: str, data):
    """Create YAML file with given data if missing."""
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def escape_latex(text):
    """Escape special LaTeX characters"""
    if not text:
        return ""

    # First decode HTML entities (&#58; -> :, &amp; -> &, etc.)
    text = html.unescape(text)
    
    # Replace special characters
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def abbreviate_name(full_name):
    """Convert full name to first-initial last name format"""
    if not full_name:
        return ""

    parts = full_name.split()
    if not parts:
        return full_name

    particles = {
        'de', 'del', 'der', 'van', 'von', 'da', 'di', 'la', 'le', 'du',
        'den', 'ter', 'ten', 'dos', 'das', 'bin', 'al', 'ibn'
    }

    last_parts = [parts[-1]]
    idx = len(parts) - 2
    while idx >= 0 and parts[idx].lower() in particles:
        last_parts.insert(0, parts[idx])
        idx -= 1

    first_parts = parts[:idx + 1]

    def token_initial(token):
        if not token:
            return ""
        segments = token.split('-')
        return '-'.join(seg[0].upper() + '.' for seg in segments if seg)

    if not first_parts:
        return ' '.join(last_parts)

    initials = [token_initial(token) for token in first_parts if token]
    last_name = ' '.join(last_parts)
    return ' '.join(initials + [last_name])

def format_authors(authors_str, my_name="Sizhuang He", mode="latex"):
    """Format authors list with abbreviation and highlighting"""
    authors_str = html.unescape(authors_str or "")
    authors_str = authors_str.replace('<strong>', '').replace('</strong>', '')
    authors_str = authors_str.replace('<b>', '').replace('</b>', '')
    authors_str = authors_str.replace('<u>', '').replace('</u>', '')
    authors_str = re.sub(r'<[^>]+>', '', authors_str)

    authors_str = re.sub(r'<sup>\*</sup>', '*', authors_str, flags=re.IGNORECASE)
    authors_str = re.sub(r'\s*,\s*and\s+', ', ', authors_str)
    authors_str = re.sub(r'\s+and\s+', ', ', authors_str)

    parts = [part.strip() for part in authors_str.split(',') if part.strip()]

    structured_authors = []
    for part in parts:
        star = ''
        while part.endswith('*'):
            star += '*'
            part = part[:-1].strip()

        if not part:
            continue

        structured_authors.append({'name': part, 'star': star})

    name_sequence = [entry['name'] for entry in structured_authors]
    include_up_to = len(structured_authors) - 1

    if my_name in name_sequence:
        my_index = name_sequence.index(my_name)
        star_indices = [idx for idx, entry in enumerate(structured_authors) if entry.get('star')]
        max_star_index = max(star_indices) if star_indices else my_index
        include_up_to = max(my_index, max_star_index)
        include_up_to = min(include_up_to, len(structured_authors) - 1)

    rendered_authors = structured_authors[:include_up_to + 1]

    if include_up_to < len(structured_authors) - 1:
        rendered_authors.append({'text': 'et al.'})

    formatted_entries = []
    for entry in rendered_authors:
        if 'text' in entry:
            text = entry['text']
            if mode == "latex":
                formatted_entries.append(escape_latex(text))
            else:
                formatted_entries.append(html.escape(text))
            continue

        name = entry['name']
        star = entry.get('star', '')
        abbreviated = abbreviate_name(name)

        if mode == "latex":
            abbreviated_escaped = escape_latex(abbreviated)
            star_escaped = escape_latex(star) if star else ''
            if name == my_name:
                formatted_entries.append(f'\\underline{{\\textbf{{{abbreviated_escaped}}}}}{star_escaped}')
            else:
                formatted_entries.append(abbreviated_escaped + star_escaped)
        elif mode == "html":
            abbreviated_escaped = html.escape(abbreviated)
            star_escaped = html.escape(star) if star else ''
            if name == my_name:
                formatted_entries.append(f'<span class="cv-me">{abbreviated_escaped}</span>{star_escaped}')
            else:
                formatted_entries.append(abbreviated_escaped + star_escaped)
        else:
            formatted_entries.append(abbreviated + star)

    return ', '.join(formatted_entries)

# STAGE 1: Data Scraping
def stage1_scrape_data():
    """Stage 1: Collect structured CV data from site content and save to integrated YAML"""
    print("🔍 Stage 1: Scraping data from website files...")
    
    config = load_yaml('_config.yml')
    publications_data = load_yaml('_data/publications.yml')

    # Ensure data files exist; create starter templates if missing
    ensure_yaml('_data/education.yml', {
        'items': [
            {
                'institution': 'Yale University',
                'location': 'New Haven, CT',
                'degree': 'Ph.D. in Computer Science',
                'dates': 'Aug. 2024 -- Present',
                'details': [
                    {'label': 'Advisor', 'value': 'Dr. David van Dijk'},
                    {'label': 'Research Focus', 'value': 'Machine Learning for Computational Biology'},
                ],
            },
            {
                'institution': 'University of Michigan, Ann Arbor',
                'location': 'Ann Arbor, MI',
                'degree': 'Bachelor of Science in Honors Mathematics (Minor in Computer Science)',
                'dates': 'Sep. 2019 -- May 2023',
                'details': []
            }
        ]
    })
    ensure_yaml('_data/honors.yml', {
        'items': [
            {'name': 'Fan Family Fellowship', 'institution': 'Yale University', 'year': '2025'},
            {'name': 'James B. Angell Scholar', 'institution': 'University of Michigan', 'year': '2023'}
        ]
    })
    ensure_yaml('_data/service.yml', {
        'groups': [
            {
                'heading': 'Conference Reviewer',
                'items': [
                    'International Conference on Learning Representations (ICLR)',
                    'AI4MATH Workshop at ICML 2025'
                ]
            }
        ]
    })

    education_yaml = load_yaml('_data/education.yml')
    honors_yaml = load_yaml('_data/honors.yml')
    service_yaml = load_yaml('_data/service.yml')

    email_link = config['email'].replace(' (at) ', '@')
    homepage = config.get('url', 'https://sizhuang.org')
    github_link = config.get('github_link', '')

    research_items = []
    research_latex_parts = []
    with open('index.md', 'r', encoding='utf-8') as f:
        content = f.read()
        research_match = re.search(r'I work on the intersection.*?(?=##)', content, re.DOTALL)
        if research_match:
            section = research_match.group(0)
            bullet_pattern = re.compile(r'- \*\*<span.*?>(.*?)</span>\*\* (.*)')
            for title, desc in bullet_pattern.findall(section):
                title_clean = html.unescape(title.strip().rstrip(':'))
                desc_clean = html.unescape(desc.strip())
                research_items.append({'title': title_clean, 'description': desc_clean})
                research_latex_parts.append(
                    f"\\textbf{{{escape_latex(title_clean)}}}: {escape_latex(desc_clean)}"
                )

    if not research_items:
        default_focus = 'Machine Learning and Computational Biology'
        research_items = [{'title': 'Focus', 'description': default_focus}]
        research_latex_parts = [escape_latex(default_focus)]

    # Normalize education from YAML (preferred), else empty list
    def normalize_details_list(details):
        result = []
        for d in (details or []):
            if isinstance(d, dict):
                label = str(d.get('label', '')).strip()
                value = str(d.get('value', '')).strip()
                result.append((label, value))
            else:
                # treat as single text item under label ""
                result.append((str(d), ''))
        return result

    education = []
    for edu in (education_yaml.get('items') or []):
        education.append({
            'institution': edu.get('institution', ''),
            'location': edu.get('location', ''),
            'degree': edu.get('degree', ''),
            'dates': edu.get('dates', ''),
            'details': normalize_details_list(edu.get('details')),
        })

    pubs_by_type = {'conference': [], 'workshop': [], 'preprint': []}
    for pub in publications_data.get('main', []):
        conference_short = (pub.get('conference_short') or '').lower()
        conference_full = (pub.get('conference') or '').lower()
        notes = (pub.get('notes') or '').lower()

        if 'workshop' in conference_full or 'workshop' in conference_short:
            pubs_by_type['workshop'].append(pub)
        elif 'arxiv' in conference_full or 'biorxiv' in conference_full or 'preprint' in notes:
            pubs_by_type['preprint'].append(pub)
        else:
            pubs_by_type['conference'].append(pub)

    publications = []
    for category in ['conference', 'workshop', 'preprint']:
        for pub in pubs_by_type[category]:
            title = pub.get('title', 'Untitled')
            venue = pub.get('conference', '')
            authors_latex = format_authors(pub.get('authors', ''), mode='latex')
            authors_html = format_authors(pub.get('authors', ''), mode='html')

            publications.append({
                'title': title,
                'title_latex': escape_latex(title),
                'title_html': title,  # Don't escape HTML for display
                'authors_latex': authors_latex,
                'authors_html': authors_html,
                'venue_latex': escape_latex(venue),
                'venue_html': venue,  # Don't escape HTML for display
            })

    honors = honors_yaml.get('items') or []
    service = service_yaml.get('groups') or []

    integrated_data = {
        'name': config['title'],
        'contact': {
            'email_display': email_link,
            'email_link': email_link,
            'homepage': homepage,
            'github': github_link,
        },
        'research': {
            'items': research_items,
            'latex': ', '.join(research_latex_parts),
        },
        'education': education,
        'publications': publications,
        'honors': honors,
        'service': service,
        'last_updated': datetime.today().strftime('%B %d, %Y'),
    }

    # Save integrated data
    os.makedirs('_data', exist_ok=True)
    with open('_data/cv_integrated.yml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(integrated_data, f, sort_keys=False, allow_unicode=True)
    
    print("✅ Stage 1 complete: Integrated CV data saved to _data/cv_integrated.yml")
    return integrated_data

# STAGE 2: LaTeX Generation
def stage2_generate_latex():
    """Stage 2: Generate LaTeX CV from integrated data"""
    print("📝 Stage 2: Generating LaTeX CV from integrated data...")
    
    # Load integrated data
    cv_data = load_yaml('_data/cv_integrated.yml')
    
    preamble = r"""%-------------------------
% Resume in Latex (auto-generated)
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
% Source: https://github.com/SizhuangHe/sizhuanghe.github.io
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks,colorlinks=true,urlcolor=black]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}  % Optional
\usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% \definecolor{mycolor}{RGB}{0, 128, 0} % Define a custom color (RGB model)
\definecolor{mycolor}{RGB}{49, 89, 152} % GPT
\definecolor{urlcolor}{RGB}{44, 79, 152} % GPT
% \definecolor{mycolor}{RGB}{57, 114, 180}    % Zuobai and Runzhe
% \definecolor{mycolor}{RGB}{37, 150, 190} % Define a custom color (RGB model)
% \definecolor{itemcolor}{RGB}{37, 150, 190}
\definecolor{itemcolor}{RGB}{0, 0, 0}
% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\color{mycolor}\scshape\raggedright\large
}{}{0em}{}[\color{mycolor}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      #1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}


\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[label={\color{itemcolor}•}]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

% For Experience
\newcommand{\resumeExpListStart}{\begin{itemize}[leftmargin=0.15in, label={\color{itemcolor}$\circ$}, itemsep=1\itemsep]}
\newcommand{\resumeExpListEnd}{\end{itemize}}
\newcommand{\resumeSubExpListStart}{\begin{itemize}[leftmargin=\leftmargin, label={\color{itemcolor}•}, itemsep=2\itemsep]}
\newcommand{\resumeSubExpListEnd}{\end{itemize}}

\newcommand{\resumeExpItem}[1]{
  \item{
    {\textbf{#1} \vspace{-1pt}}
  }
}

\newcommand{\resumeExpBriefItem}[1]{
  \item{
    {{\small#1} \vspace{-1pt}}
  }
}


\newcommand{\resumeSubExpItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeText}{\vspace{3pt}}
\newcommand{\resumePosition}[1]{
    \item
    \begin{tabular*}{0.97\textwidth}{l}
      \small#1 \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeDataItem}[2]{
  \item\small{
    #1 \hfill #2 \vspace{-2pt}
  }
}
\newcommand{\resumePublication}[2]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{p{0.9\textwidth}@{\extracolsep{\fill}}r}
      \textbf{#1} & \\
      \textit{\small#2} & \\
    \end{tabular*}\vspace{-2pt}
}

\newcommand{\resumeHonor}[2]{
  \vspace{-2pt}\item
    {\small#1} \hfill {\small#2}
  \vspace{-7pt}
}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}
"""

    lines = [preamble]
    contact = cv_data['contact']
    name = escape_latex(cv_data['name'])
    
    # Header section
    lines.append("%----------HEADING----------")
    lines.append("\\begin{center}")
    lines.append(f"    \\textbf{{\\Huge \\scshape \\color{{mycolor}}{name}}} \\\\ \\vspace{{10pt}}")
    contact_parts = [
        f"\\href{{mailto:{contact['email_link']}}}{{Email: \\underline{{{escape_latex(contact['email_display'])}}}}}",
        f"\\href{{{contact['homepage']}}}{{Homepage: \\underline{{{escape_latex(contact['homepage'])}}}}}",
    ]
    if contact.get('github'):
        contact_parts.append(
            f"\\href{{{contact['github']}}}{{Github: \\underline{{{escape_latex(contact['github'])}}}}}"
        )
    lines.append("    " + " $|$ ".join(contact_parts) + "\\\\ \\vspace{3pt}")
    lines.append("\\end{center}\n")
    lines.append('\\hypersetup{urlcolor=urlcolor}\n')

    # Research Interest section
    lines.append('%-----------Interest-----------\n\\section{Research Interest}')
    lines.append('\\resumeText{' + cv_data['research']['latex'] + '}\n')

    # Education section
    lines.append('%-----------EDUCATION-----------\n\\section{Education}\n  \\resumeSubHeadingListStart')
    for edu in cv_data['education']:
        lines.append('    \\resumeSubheading')
        lines.append(f"      {{{escape_latex(edu['institution'])}}}{{{escape_latex(edu['location'])}}}")
        lines.append(f"      {{{escape_latex(edu['degree'])}}}{{{escape_latex(edu['dates'])}}}")
        if edu['details']:
            lines.append('      \\resumeItemListStart')
            for label, value in edu['details']:
                detail_text = f"{label}: {value}" if value else label
                lines.append(f"        \\resumeItem{{{escape_latex(detail_text)}}}")
            lines.append('      \\resumeItemListEnd')
    lines.append('  \\resumeSubHeadingListEnd\n')

    # Publications section
    lines.append('%%-----------Publications-----------\n\\section{Publications}\n\\resumeSubHeadingListStart')
    for pub in cv_data['publications']:
        lines.append(
            f"    \\resumePublication{{{pub['title_latex']}}}{{{pub['authors_latex']} ({pub['venue_latex']})}}"
        )
    lines.append('\\resumeSubHeadingListEnd\n')
    lines.append('\\vspace{-6pt}\\small{\\textit{* denotes equal contribution}}\n')

    # Honors & Awards section - Match Research Interest formatting but separate lines
    lines.append('%%-----------Honors \\& Awards-----------\n\\section{Honors \\& Awards}')
    
    # Format each honor on a separate line with same spacing as research interest
    for honor in cv_data['honors']:
        honor_text = f"\\textbf{{{escape_latex(honor['name'])}}}, {escape_latex(honor['institution'])} ({escape_latex(honor['year'])})"
        lines.append('\\resumeText{' + honor_text + '}')
    
    lines.append('')  # Add empty line after section

    # Services section - Match template exactly
    lines.append('%%-----------Services-----------\n\\section{Services}\n  \\resumeSubHeadingListStart')
    for svc in cv_data['service']:
        lines.append(
            f"        \\resumePosition{{\\textbf{{{escape_latex(svc['heading'])}}}}}\n            \\resumeItemListStart"
        )
        for item in svc['items']:
            # For services, we don't have years, so just use the item text with empty year
            lines.append(f"                \\resumeDataItem{{{escape_latex(item)}}}{{}}")
        lines.append('            \\resumeItemListEnd')
    lines.append('  \\resumeSubHeadingListEnd\n')

    lines.append('\\vfill')
    lines.append('\\center{\\small Last updated: \\today}\n')
    lines.append('\\end{document}\n')

    latex_content = '\n'.join(lines)
    
    # Save LaTeX file
    os.makedirs('assets/files', exist_ok=True)
    with open('assets/files/cv.tex', 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print("✅ Stage 2 complete: LaTeX CV generated: assets/files/cv.tex")
    return latex_content

# STAGE 3: No longer needed - CV HTML is now generated by Jekyll from cv.md template

def main():
    parser = argparse.ArgumentParser(description='Generate CV from website data - Two-stage workflow')
    parser.add_argument('--stage', type=int, choices=[1, 2], help='Run specific stage only (1=data, 2=latex)')
    args = parser.parse_args()

    print("🔧 Generating CV from website data - Two-stage workflow...")
    
    if args.stage is None or args.stage == 1:
        # Stage 1: Scrape data from website files
        stage1_scrape_data()
    
    if args.stage is None or args.stage == 2:
        # Stage 2: Generate LaTeX from integrated data
        stage2_generate_latex()
    
    if args.stage is None:
        print("📄 Two-stage workflow complete!")
        print("📄 Source: _config.yml, _data/publications.yml, index.md")
        print("📄 Integrated data: _data/cv_integrated.yml")
        print("📄 Generated files: assets/files/cv.tex")
        print("📄 HTML CV: Automatically generated by Jekyll from cv.md template")


if __name__ == "__main__":
    main()