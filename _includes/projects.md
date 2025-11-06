## Open Source Projects

<div class="projects-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
{% for project in site.data.projects.projects %}
  <div class="project-card" style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.3s ease; display: flex; flex-direction: column;">
    {% if project.image %}
    <div style="margin-bottom: 1rem;">
      <img src="{{ project.image }}" alt="{{ project.name }}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 6px;">
    </div>
    {% endif %}

    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2em; color: var(--global-theme-color);">
      <a href="{{ project.github }}" target="_blank" style="color: inherit; text-decoration: none;">
        {{ project.name }}
      </a>
    </h3>

    <p style="margin: 0 0 1rem 0; color: #666; line-height: 1.6; flex-grow: 1; font-size: 0.95em;">
      {{ project.description }}
    </p>

    {% if project.tags %}
    <div class="project-tags" style="margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 0.4rem;">
      {% for tag in project.tags %}
      <span style="background-color: #f0f0f0; color: #555; padding: 3px 10px; border-radius: 12px; font-size: 0.8em;">{{ tag }}</span>
      {% endfor %}
    </div>
    {% endif %}

    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 0.5rem; border-top: 1px solid #f0f0f0;">
      <a href="{{ project.github }}" target="_blank" style="color: var(--global-theme-color); text-decoration: none; font-size: 0.9em; font-weight: 500;">
        View on GitHub →
      </a>
      {% if project.stars %}
      <span style="color: #888; font-size: 0.85em;">⭐ {{ project.stars }}</span>
      {% endif %}
    </div>
  </div>
{% endfor %}
</div>

<style>
.project-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

@media (prefers-color-scheme: dark) {
  .project-card {
    background-color: #1a1a1a !important;
    border-color: #333 !important;
  }
  .project-card .project-tags span {
    background-color: #2a2a2a !important;
    color: #ccc !important;
  }
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
