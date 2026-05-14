## Services

{% for group in site.data.service.groups %}
<h4 style="margin:0 10px 0;">{{ group.heading }}</h4>

<ul style="margin:0 0 5px;">
{% for item in group.items %}{% assign parts = item | split: ", " %}{% assign year = parts | last %}{% if parts.size > 1 and year.size == 4 %}{% assign namecount = parts.size | minus: 1 %}{% assign nameparts = parts | slice: 0, namecount %}  <li><span style="display:flex; justify-content:space-between; gap:1em;"><span>{{ nameparts | join: ", " }}</span><span style="white-space:nowrap;">{{ year }}</span></span></li>
{% else %}  <li>{{ item }}</li>
{% endif %}{% endfor %}</ul>
{% endfor %}
