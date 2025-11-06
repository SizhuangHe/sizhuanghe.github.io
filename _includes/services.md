## Services

{% for group in site.data.service.groups %}
<h4 style="margin:0 10px 0;">{{ group.heading }}</h4>

<ul style="margin:0 0 5px;">
{% for item in group.items %}  <li>{{ item }}</li>
{% endfor %}</ul>
{% endfor %}