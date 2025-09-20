<h2 id="publications" style="margin: 2px 0px -15px;">Publications and Preprints</h2>
<p style="font-size: 0.9em; margin-top: 15px; margin-bottom: -10px;"><i>(*: Equal Contribution; Organized by Year; Last Updated: Apr 2025)</i></p>

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
      <div class="periodical" style="margin-top: 2px;"><em>{{ link.conference }}</em>{% if link.date %} • {{ link.date }}{% endif %}{% if link.notes %} • <strong><i style="color:#e74d3c">{{ link.notes }}</i></strong>{% endif %}</div>
    <div class="links" style="margin-top: 5px;">
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
      {% if link.bibtex %} 
      <a href="{{ link.bibtex }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">BibTex</a>
      {% endif %}
      {% if link.poster %} 
      <a href="{{ link.poster }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:11px;">Poster</a>
      {% endif %}
      {% if link.others %} 
      {{ link.others }}
      {% endif %}
    </div>
  </div>
</div>
</li>

      {% endif %}
    {% endfor %}
    </ol>
  </div>
{% endfor %}

</div>
