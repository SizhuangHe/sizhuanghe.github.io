<h2 id="selected-publications" style="margin: 2px 0px -15px;">Selected Publications</h2>

<div class="publications">
<ol class="bibliography">

{% assign selected_count = 0 %}
{% for link in site.data.publications.main %}
{% if link.selected %}
{% assign selected_count = selected_count | plus: 1 %}

<li>
<div class="pub-row">
  {% assign is_even = selected_count | modulo: 2 %}
  {% if is_even == 1 %}
  <!-- Odd publications: Image left, text right -->
  <div class="col-sm-3 abbr" style="position: relative;padding-right: 15px;padding-left: 15px;">
    {% if link.image %} 
    <img src="{{ link.image }}" class="teaser img-fluid z-depth-1" style="width=100;height=60%">
    {% endif %}
  </div>
  <div class="col-sm-9" style="position: relative;padding-right: 15px;padding-left: 20px;">
      <div class="title" style="font-size: 1.3em; font-weight: 600;"><a href="{{ link.pdf }}">{% if link.alt_title %}{{ link.alt_title }}{% else %}{{ link.title }}{% endif %}</a></div>
      {% if link.summary %}
      <div class="abstract" style="margin-top: 10px; font-size: 1.05em; line-height: 1.5; color: #666; font-style: italic;">{{ link.summary }}{% if link.blog %} Read more about this work in our <a href="{{ link.blog }}" target="_blank" style="color: #2c5aa0; text-decoration: none;">Google Research blog post</a>.{% endif %} — <a href="{{ link.pdf }}" target="_blank" style="color: #2c5aa0; font-weight: bold; text-decoration: none;">{{ link.conference }}</a></div>
      {% endif %}
    <div class="links">
      {% if link.code %} 
      <a href="{{ link.code }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:14px;">Code</a>
      {% endif %}
      {% if link.page %} 
      <a href="{{ link.page }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:14px;">Project Page</a>
      {% endif %}
    </div>
  </div>
  {% else %}
  <!-- Even publications: Text left, image right -->
  <div class="col-sm-9" style="position: relative;padding-right: 20px;padding-left: 15px;">
      <div class="title" style="font-size: 1.3em; font-weight: 600;"><a href="{{ link.pdf }}">{% if link.alt_title %}{{ link.alt_title }}{% else %}{{ link.title }}{% endif %}</a></div>
      {% if link.summary %}
      <div class="abstract" style="margin-top: 10px; font-size: 1.05em; line-height: 1.5; color: #666; font-style: italic;">{{ link.summary }}{% if link.blog %} Read more about this work in our <a href="{{ link.blog }}" target="_blank" style="color: #2c5aa0; text-decoration: none;">Google Research blog post</a>.{% endif %} — <a href="{{ link.pdf }}" target="_blank" style="color: #2c5aa0; font-weight: bold; text-decoration: none;">{{ link.conference }}</a></div>
      {% endif %}
    <div class="links">
      {% if link.code %} 
      <a href="{{ link.code }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:14px;">Code</a>
      {% endif %}
      {% if link.page %} 
      <a href="{{ link.page }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:14px;">Project Page</a>
      {% endif %}
    </div>
  </div>
  <div class="col-sm-3 abbr" style="position: relative;padding-right: 15px;padding-left: 15px;">
    {% if link.image %} 
    <img src="{{ link.image }}" class="teaser img-fluid z-depth-1" style="width=100;height=60%">
    {% endif %}
  </div>
  {% endif %}
</div>
</li>
<br>

{% endif %}
{% endfor %}

</ol>
</div>
