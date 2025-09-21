<h2 id="publications" style="margin: 2px 0px -15px;">Complete Publication List</h2>
<p style="font-size: 0.9em; margin-top: 15px; margin-bottom: -10px;"><i>(*: Equal Contribution; Last Updated: Sep 2025)</i></p>

<div class="publications">

{% comment %} Get unique years and sort them {% endcomment %}
{% assign years = '' | split: ',' %}
{% for pub in site.data.publications.main %}
  {% assign year = pub.date | split: ' ' | last %}
  {% unless years contains year %}
    {% assign years = years | push: year %}
  {% endunless %}
{% endfor %}
{% assign years = years | sort | reverse %}

{% for year in years %}
  <div class="year-section">
    <h3 class="year-header" style="font-size: 1.1em; margin: 25px 0 15px 0; font-weight: normal; border-bottom: 1px solid #eee; padding-bottom: 5px;">{{ year }}</h3>
    <ol class="bibliography">
    {% for link in site.data.publications.main %}
      {% assign pub_year = link.date | split: ' ' | last %}
      {% if pub_year == year %}

<li style="margin-bottom: 1em;">
<div class="pub-row">
  <div class="col-sm-12" style="position: relative;padding-right: 15px;padding-left: 15px;">
      <div class="title"><a href="{{ link.pdf }}">{{ link.title }}</a></div>
      <div class="author" style="font-size: 0.9em; margin-top: 2px;">
        {% assign author_parts = link.authors | split: ', ' %}
        {% assign truncated_authors = '' %}
        {% assign author_count = 0 %}
        {% assign found_sizhuang = false %}
        {% assign should_truncate = false %}
        
        {% for author in author_parts %}
          {% assign author_count = author_count | plus: 1 %}
          
          {% if truncated_authors == '' %}
            {% assign truncated_authors = author %}
          {% else %}
            {% assign truncated_authors = truncated_authors | append: ', ' | append: author %}
          {% endif %}
          
          {% if author contains 'Sizhuang He' %}
            {% assign found_sizhuang = true %}
          {% endif %}
          
          {% comment %} Only truncate after finding Sizhuang He and having at least 5 authors {% endcomment %}
          {% if found_sizhuang == true and author_count >= 5 and author_parts.size > author_count %}
            {% assign should_truncate = true %}
            {% break %}
          {% endif %}
        {% endfor %}
        
        {% if should_truncate and author_parts.size > author_count %}
          <span class="author-truncated">{{ truncated_authors }}</span>
          <span class="author-toggle" onclick="toggleAuthors(this)" style="color: #888888; cursor: pointer; text-decoration: underline dashed; margin-left: 5px;">and {{ author_parts.size | minus: author_count }} more authors</span>
          <span class="author-full" style="display: none;">{{ link.authors }}</span>
        {% else %}
          {{ link.authors }}
        {% endif %}
      </div>
      <div class="periodical" style="margin-top: 2px;"><em>{{ link.conference }}</em></div>
    <div class="links" style="margin-top: 5px;">
      {% if link.full_abstract %} 
      <a href="javascript:void(0)" onclick="toggleAbstract('abstract-{{ forloop.index }}')" class="btn btn-sm z-depth-0" role="button" style="font-size:11px;">Abstract</a>
      {% endif %}
      {% if link.bibtex %} 
      <a href="javascript:void(0)" onclick="toggleBibtex('bibtex-{{ forloop.index }}', '{{ link.bibtex }}')" class="btn btn-sm z-depth-0" role="button" style="font-size:11px;">BibTex</a>
      {% endif %}
      {% if link.pdf %} 
      <a href="{{ link.pdf }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">PDF</a>
      {% endif %}
      {% if link.blog %} 
      <a href="{{ link.blog }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">Blog</a>
      {% endif %}
      {% if link.code %} 
      <a href="{{ link.code }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">Code</a>
      {% endif %}
      {% if link.page %} 
      <a href="{{ link.page }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">Project Page</a>
      {% endif %}
      {% if link.poster %} 
      <a href="{{ link.poster }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">Poster</a>
      {% endif %}
      {% if link.others %} 
      {{ link.others }}
      {% endif %}
    </div>
    <!-- BibTeX formatted display -->
    {% if link.bibtex %}
    <div id="bibtex-{{ forloop.index }}" class="bibtex-container" style="display: none; margin-top: 10px; padding: 15px; background-color: #f8f9fa; border-left: 3px solid #003d82; border-radius: 4px; position: relative; width: 700px; max-width: 80%;">
      <button onclick="copyBibtexContent('bibtex-content-{{ forloop.index }}')" style="position: absolute; top: 8px; right: 8px; padding: 6px; border: 1px solid #ced4da; background: #fff; border-radius: 4px; cursor: pointer; color: #495057; display: flex; align-items: center; justify-content: center; z-index: 10;" title="Copy BibTeX">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      </button>
      <pre id="bibtex-content-{{ forloop.index }}" class="bibtex-code" style="margin: 0; font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace; font-size: 11px; line-height: 1.5; white-space: pre; word-wrap: normal; background-color: transparent; border: none; padding: 0; overflow-x: auto; color: #24292e;"></pre>
    </div>
    {% endif %}
    <!-- Abstract display -->
    {% if link.full_abstract %}
    <div id="abstract-{{ forloop.index }}" class="abstract-container" style="display: none; margin-top: 10px; padding: 15px; background-color: #f8f9fa; border-left: 3px solid #724e52; border-radius: 4px; width: 700px; max-width: 80%;">
      <div id="abstract-content-{{ forloop.index }}" style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; line-height: 1.6; color: #495057; text-align: justify;">{{ link.full_abstract }}</div>
    </div>
    {% endif %}
  </div>
</div>
</li>

      {% endif %}
    {% endfor %}
    </ol>
  </div>
{% endfor %}

</div>
