<!-- Google Scholar Statistics -->
<div class="scholar-stats">
  <div class="stats-container" id="scholar-stats">
    <div class="stat-item">
      <div class="stat-number" id="citations">Loading...</div>
      <div class="stat-label">Citations</div>
    </div>
    <div class="stat-item">
      <div class="stat-number" id="h-index">Loading...</div>
      <div class="stat-label">H-Index</div>
    </div>
  </div>
</div>

<script>
// Fetch Google Scholar stats from the data branch
async function loadScholarStats() {
  // Check if we're on localhost (development)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Show mock data for local development
    document.getElementById('citations').textContent = '1,234';
    document.getElementById('h-index').textContent = '12';
    return;
  }
  
  try {
    const response = await fetch('https://raw.githubusercontent.com/SizhuangHe/sizhuanghe.github.io/google-scholar-stats/gs_data.json');
    if (!response.ok) {
      throw new Error('Failed to fetch stats');
    }
    
    const data = await response.json();
    
    // Update the display
    document.getElementById('citations').textContent = data.citations?.toLocaleString() || '-';
    document.getElementById('h-index').textContent = data.h_index || '-';
    
  } catch (error) {
    console.log('Could not load Google Scholar stats:', error);
    // Show fallback values
    document.getElementById('citations').textContent = 'N/A';
    document.getElementById('h-index').textContent = 'N/A';
  }
}

// Load stats when the page loads
document.addEventListener('DOMContentLoaded', loadScholarStats);
</script>

<style>
.scholar-stats {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid var(--global-theme-color);
}

.stats-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--global-theme-color);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@media (max-width: 768px) {
  .stats-container {
    gap: 1.5rem;
  }
}
</style>
