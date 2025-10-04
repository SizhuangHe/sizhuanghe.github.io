#!/usr/bin/env python3
"""
Generate CV from website data
Single source of truth: website YAML and config files
"""

import os
import yaml
import re
import html
from datetime import datetime

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

def build_cv_data():
    """Collect structured CV data from site content"""
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
                'title_html': html.escape(title),
                'authors_latex': authors_latex,
                'authors_html': authors_html,
                'venue_latex': escape_latex(venue),
                'venue_html': html.escape(venue),
            })

    honors = honors_yaml.get('items') or []

    service = service_yaml.get('groups') or []

    return {
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


def generate_latex_content(cv):
    """Render LaTeX CV from structured data"""
    # (content inserted below)
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

% \newcommand{\resumeHonor}[2]{
%   \vspace{-2pt}\item
%     \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
%       \textbf{#1} & #2 \\
%     \end{tabular*}\vspace{-7pt}
% }
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
    contact = cv['contact']
    name = escape_latex(cv['name'])
    
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
    lines.append('\\resumeText{' + cv['research']['latex'] + '}\n')

    # Education section
    lines.append('%-----------EDUCATION-----------\n\\section{Education}\n  \\resumeSubHeadingListStart')
    for edu in cv['education']:
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
    for pub in cv['publications']:
        lines.append(
            f"    \\resumePublication{{{pub['title_latex']}}}{{{pub['authors_latex']} ({pub['venue_latex']})}}"
        )
    lines.append('\\resumeSubHeadingListEnd\n')
    lines.append('\\vspace{-6pt}\\small{\\textit{* denotes equal contribution}}\n')

    # Honors & Awards section
    lines.append('%%-----------Honors \\& Awards-----------\n\\section{Honors \\& Awards}\n    \\resumeSubHeadingListStart')
    for honor in cv['honors']:
        lines.append(
            f"        \\resumeHonor{{\\textbf{{{escape_latex(honor['name'])}}}, {escape_latex(honor['institution'])}}}{{{escape_latex(honor['year'])}}}"
        )
    lines.append('    \\resumeSubHeadingListEnd\n')

    # Academic Service section
    lines.append('%%-----------Services-----------\n\\section{Services}\n  \\resumeSubHeadingListStart')
    for svc in cv['service']:
        lines.append(
            f"        \\resumePosition{{\\textbf{{{escape_latex(svc['heading'])}}}}}\n            \\resumeItemListStart"
        )
        for item in svc['items']:
            lines.append(f"                \\resumeDataItem{{{escape_latex(item)}}}{{}}")
        lines.append('            \\resumeItemListEnd')
    lines.append('  \\resumeSubHeadingListEnd\n')

    lines.append('\\vfill')
    lines.append('\\center{\\small Last updated: \\today}\n')
    lines.append('\\end{document}\n')

    return '\n'.join(lines)


def generate_html_content(cv):
    pdf_link = "{{ '/assets/files/cv.pdf' | relative_url }}"
    tex_link = "{{ '/assets/files/cv.tex' | relative_url }}"

    parts = [
        '---',
        'layout: default',
        'title: Curriculum Vitae',
        'permalink: /cv/',
        '---',
        '<style>',
        '.cv-page { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }',
        '.cv-header h1 { color: var(--global-theme-color, #00356B); margin-bottom: 0.2rem; }',
        '.cv-contact { font-size: 0.95rem; color: var(--text-color, #222); }',
        '.cv-contact a { color: inherit; text-decoration: none; border-bottom: 1px solid var(--global-theme-color, #00356B); }',
        '.cv-contact a:hover { color: var(--global-theme-color, #00356B); }',
        '.cv-download { margin: 1.5rem 0 2rem; font-size: 0.95rem; }',
        '.cv-download a { color: var(--global-theme-color, #00356B); font-weight: 600; text-decoration: none; }',
        '.cv-download a:hover { text-decoration: underline; }',
        '.cv-section { margin-bottom: 2rem; }',
        '.cv-section-title { color: var(--global-theme-color, #00356B); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; font-weight: 700; }',
        '.cv-research li { margin-bottom: 0.4rem; }',
        '.cv-education-item { margin-bottom: 1.2rem; }',
        '.cv-education-heading { display: flex; justify-content: space-between; font-weight: 600; }',
        '.cv-education-sub { font-style: italic; display: flex; justify-content: space-between; font-size: 0.95rem; margin-top: 0.15rem; }',
        '.cv-education-details { margin: 0.4rem 0 0.2rem 1rem; font-size: 0.95rem; }',
        '.cv-education-details li { margin-bottom: 0.2rem; }',
        '.cv-publication-list { list-style: none; padding-left: 0; }',
        '.cv-publication-list li { margin-bottom: 1rem; }',
        '.cv-pub-title { font-weight: 600; }',
        '.cv-pub-authors { display: block; margin-top: 0.2rem; }',
        '.cv-pub-venue { display: block; font-style: italic; margin-top: 0.15rem; }',
        '.cv-me { font-weight: 700; text-decoration: underline; }',
        '.cv-honor-list { list-style: none; padding-left: 0; }',
        '.cv-honor-list li { display: flex; justify-content: space-between; margin-bottom: 0.35rem; font-size: 0.95rem; }',
        '.cv-service-heading { font-weight: 600; margin-bottom: 0.3rem; }',
        '.cv-service-list { list-style: disc; padding-left: 1.2rem; margin-top: 0.2rem; }',
        '.cv-last-updated { margin-top: 3rem; font-size: 0.9rem; color: var(--text-color, #555); }',
        '@media (max-width: 640px) { .cv-education-heading, .cv-education-sub { flex-direction: column; gap: 0.1rem; } .cv-honor-list li { flex-direction: column; align-items: flex-start; gap: 0.15rem; } }',
        '</style>',
        '<div class="cv-page">',
        '  <div class="cv-header">',
        f"    <h1>{html.escape(cv['name'])}</h1>",
        '    <div class="cv-contact">',
        f"      <a href=\"mailto:{cv['contact']['email_link']}\">{html.escape(cv['contact']['email_display'])}</a> · ",
        f"      <a href=\"{cv['contact']['homepage']}\">{html.escape(cv['contact']['homepage'])}</a>",
    ]

    if cv['contact'].get('github'):
        parts[-1] += f" · <a href=\"{cv['contact']['github']}\">{html.escape(cv['contact']['github'])}</a>"

    parts.extend([
        '    </div>',
        '  </div>',
        f'  <p class="cv-download"><a href="{pdf_link}">Download PDF</a> · <a href="{tex_link}">LaTeX Source</a></p>',
    ])

    parts.append('  <section class="cv-section">')
    parts.append('    <h2 class="cv-section-title">Research Interest</h2>')
    parts.append('    <ul class="cv-research">')
    for item in cv['research']['items']:
        parts.append(
            f"      <li><strong>{html.escape(item['title'])}:</strong> {html.escape(item['description'])}</li>"
        )
    parts.append('    </ul>')
    parts.append('  </section>')

    parts.append('  <section class="cv-section">')
    parts.append('    <h2 class="cv-section-title">Education</h2>')
    for edu in cv['education']:
        parts.append('    <div class="cv-education-item">')
        parts.append(
            f"      <div class=\"cv-education-heading\"><span>{html.escape(edu['institution'])}</span><span>{html.escape(edu['location'])}</span></div>"
        )
        parts.append(
            f"      <div class=\"cv-education-sub\"><span>{html.escape(edu['degree'])}</span><span>{html.escape(edu['dates'])}</span></div>"
        )
        if edu['details']:
            parts.append('      <ul class="cv-education-details">')
            for label, value in edu['details']:
                parts.append(
                    f"        <li><strong>{html.escape(label)}:</strong> {html.escape(value)}</li>"
                )
            parts.append('      </ul>')
        parts.append('    </div>')
    parts.append('  </section>')

    parts.append('  <section class="cv-section">')
    parts.append('    <h2 class="cv-section-title">Publications</h2>')
    parts.append('    <ol class="cv-publication-list">')
    for pub in cv['publications']:
        parts.append('      <li>')
        parts.append(f"        <span class=\"cv-pub-title\">{pub['title_html']}</span>")
        parts.append(f"        <span class=\"cv-pub-authors\">{pub['authors_html']}</span>")
        parts.append(f"        <span class=\"cv-pub-venue\">{pub['venue_html']}</span>")
        parts.append('      </li>')
    parts.append('    </ol>')
    parts.append('    <p class="cv-footnote"><em>* denotes equal contribution.</em></p>')
    parts.append('  </section>')

    parts.append('  <section class="cv-section">')
    parts.append('    <h2 class="cv-section-title">Honors &amp; Awards</h2>')
    parts.append('    <ul class="cv-honor-list">')
    for honor in cv['honors']:
        parts.append(
            f"      <li><span><strong>{html.escape(honor['name'])}</strong>, {html.escape(honor['institution'])}</span><span>{html.escape(honor['year'])}</span></li>"
        )
    parts.append('    </ul>')
    parts.append('  </section>')

    parts.append('  <section class="cv-section">')
    parts.append('    <h2 class="cv-section-title">Academic Service</h2>')
    for svc in cv['service']:
        parts.append('    <div class="cv-service">')
        parts.append(f"      <div class=\"cv-service-heading\">{html.escape(svc['heading'])}</div>")
        parts.append('      <ul class="cv-service-list">')
        for item in svc['items']:
            parts.append(f"        <li>{html.escape(item)}</li>")
        parts.append('      </ul>')
        parts.append('    </div>')
    parts.append('  </section>')

    parts.append(f'  <p class="cv-last-updated">Last updated: {html.escape(cv["last_updated"])}.</p>')
    parts.append('</div>')

    return '\n'.join(parts)


def main():
    print("🔧 Generating CV from website data...")
    cv_data = build_cv_data()
    latex_content = generate_latex_content(cv_data)
    html_content = generate_html_content(cv_data)

    os.makedirs('assets/files', exist_ok=True)
    with open('assets/files/cv.tex', 'w', encoding='utf-8') as f:
        f.write(latex_content)

    os.makedirs('cv', exist_ok=True)
    with open('cv/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ CV generated: assets/files/cv.tex")
    print("✅ CV webpage generated: cv/index.html")
    print("📄 Source: _config.yml, _data/publications.yml, index.md")


if __name__ == "__main__":
    main()
