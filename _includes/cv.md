<h1 style="margin: 0 0 0.5rem 0;">Curriculum Vitae</h1>

<div style="display: flex; align-items: center; justify-content: space-between; margin: 0 0 1rem 0;">
  <p class="cv-last-updated" style="margin: 0;">Last updated: {{ site.data.cv_integrated.last_updated }}.</p>
  <div>
    <a href="{{ '/assets/files/cv.pdf' | relative_url }}" class="cv-download-btn">PDF</a>
    <a href="{{ '/assets/files/cv.tex' | relative_url }}" class="cv-download-btn">TeX</a>
  </div>
</div>

<style>
.cv-download-btn {
  color: var(--global-theme-color);
  font-weight: 600;
  text-decoration: none;
  padding: 0.2rem 0.8rem;
  border: 1px solid var(--global-theme-color);
  border-radius: 4px;
  margin: 0 0.3rem;
  display: inline-block;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.cv-download-btn:hover { 
  background-color: var(--global-theme-color);
  color: white;
}

.cv-education-item { 
  margin-bottom: 1.2rem; 
}

.cv-education-heading { 
  display: flex; 
  justify-content: space-between; 
  font-weight: 600; 
}

.cv-education-sub { 
  font-style: italic; 
  display: flex; 
  justify-content: space-between; 
  font-size: 0.95rem; 
  margin-top: 0.15rem; 
}

.cv-education-details { 
  margin: 0.4rem 0 0.2rem 1rem; 
  font-size: 0.95rem; 
}

.cv-education-details li { 
  margin-bottom: 0.2rem; 
}

.cv-publication-list { 
  list-style: none; 
  padding-left: 0; 
  counter-reset: publication-counter; 
}

.cv-publication-list li { 
  margin-bottom: 1rem; 
  counter-increment: publication-counter; 
  position: relative; 
  padding-left: 2rem; 
}

.cv-publication-list li::before { 
  content: counter(publication-counter) "."; 
  position: absolute; 
  left: 0; 
  font-weight: 600; 
  color: var(--global-theme-color); 
}

.cv-pub-title { 
  font-weight: 600; 
  color: #043361; 
}

.cv-pub-authors { 
  display: block; 
  margin-top: 0.2rem; 
  font-size: 0.9em; 
}

.cv-pub-venue { 
  display: block; 
  font-style: italic; 
  margin-top: 0.15rem; 
  font-size: 0.9em; 
}

.cv-me { 
  font-weight: 700; 
  text-decoration: underline; 
}

.cv-honors-awards {
  margin: 1rem 0;
}

.cv-honors-awards p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.cv-services {
  margin: 1rem 0;
}

.cv-services ul {
  list-style: none;
  padding-left: 0;
}

.cv-services li {
  margin: 0.5rem 0;
  padding-left: 1rem;
  position: relative;
}

.cv-services li::before {
  content: "•";
  color: var(--global-theme-color);
  font-weight: bold;
  position: absolute;
  left: 0;
}

@media (max-width: 640px) { 
  .cv-education-heading, .cv-education-sub { 
    flex-direction: column; 
    gap: 0.1rem; 
  } 
  .cv-publication-list li { 
    padding-left: 1.5rem; 
  }
  .cv-download-btn {
    display: block;
    margin: 0.5rem auto;
    width: fit-content;
  }
}

@media (prefers-color-scheme: dark) {
  .cv-pub-title {
    color: rgb(62, 183, 240);
  }
}
</style>

## Research Interest

{% for item in site.data.cv_integrated.research.items %}<strong><span style="color: var(--global-theme-color); font-weight: bold;">{{ item.title }}:</span></strong> {{ item.description }}{% unless forloop.last %}, {% endunless %}{% endfor %}

## Education

{% for edu in site.data.cv_integrated.education %}
<div class="cv-education-item">
  <div class="cv-education-heading">
    <span><strong>{{ edu.institution }}</strong></span>
    <span>{{ edu.location }}</span>
  </div>
  <div class="cv-education-sub">
    <span>{{ edu.degree }}</span>
    <span>{{ edu.dates }}</span>
  </div>
  {% if edu.details %}
  <ul class="cv-education-details">
    {% for detail in edu.details %}
    <li>{% if detail[1] != "" %}<strong>{{ detail[0] }}:</strong> {{ detail[1] }}{% else %}{{ detail[0] }}{% endif %}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>
{% endfor %}

## Publications

<ol class="cv-publication-list">
  {% for pub in site.data.cv_integrated.publications %}
  <li>
    <div class="cv-pub-title">{{ pub.title_html }}</div>
    <div class="cv-pub-authors">{{ pub.authors_html }}</div>
    <div class="cv-pub-venue">{{ pub.venue_html }}</div>
  </li>
  {% endfor %}
</ol>
<p style="font-size: 0.9em; margin-top: 15px; color: #666;"><em>* denotes equal contribution.</em></p>

## Honors & Awards

{% for honor in site.data.cv_integrated.honors %}
- **<span style="color: var(--global-theme-color); font-weight: bold;">{{ honor.name }}</span>**, {{ honor.institution }} ({{ honor.year }})
{% endfor %}

## Services

{% for svc in site.data.cv_integrated.service %}
- **<span style="color: var(--global-theme-color); font-weight: bold;">{{ svc.heading }}:</span>**
{% for item in svc.items %}    - {{ item }}
{% endfor %}
{% endfor %}
