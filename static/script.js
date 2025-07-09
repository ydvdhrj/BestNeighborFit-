// DOM Elements
const form = document.getElementById('preferences-form');
const loadingSection = document.getElementById('loading-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const resultsContainer = document.getElementById('results-container');
const errorMessage = document.getElementById('error-message');

// Slider value displays
const populationDensitySlider = document.getElementById('population-density');
const populationDensityValue = document.getElementById('population-density-value');
const parksDensitySlider = document.getElementById('parks-density');
const parksDensityValue = document.getElementById('parks-density-value');
const restaurantsDensitySlider = document.getElementById('restaurants-density');
const restaurantsDensityValue = document.getElementById('restaurants-density-value');

// Update slider values in real-time
populationDensitySlider.addEventListener('input', (e) => {
    populationDensityValue.textContent = parseInt(e.target.value).toLocaleString();
});

parksDensitySlider.addEventListener('input', (e) => {
    parksDensityValue.textContent = parseFloat(e.target.value).toFixed(1);
});

restaurantsDensitySlider.addEventListener('input', (e) => {
    restaurantsDensityValue.textContent = parseInt(e.target.value);
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results and errors
    hideAllSections();
    
    // Show loading
    loadingSection.classList.remove('hidden');
    
    // Get form data
    const formData = new FormData(form);
    const preferences = {
        population_density: parseInt(formData.get('population_density')),
        parks_per_sqkm: parseFloat(formData.get('parks_per_sqkm')),
        restaurants_per_sqkm: parseInt(formData.get('restaurants_per_sqkm')),
        k: parseInt(formData.get('k'))
    };
    
    try {
        // Make API request
        const response = await fetch('/api/neighborhoods/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(preferences)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            await displayResults(data);
        } else {
            throw new Error(data.message || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        loadingSection.classList.add('hidden');
    }
});

// Display results
async function displayResults(data) {
    const { recommendations, user_preferences } = data;
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    // Fetch detailed information for each recommendation
    const detailedResults = await Promise.all(
        recommendations.map(async (rec, index) => {
            try {
                const response = await fetch(`/api/neighborhoods/${rec.geoid}`);
                const details = await response.json();
                return {
                    ...rec,
                    rank: index + 1,
                    details: details.status === 'success' ? details.neighborhood : null
                };
            } catch (error) {
                console.error(`Error fetching details for ${rec.geoid}:`, error);
                return {
                    ...rec,
                    rank: index + 1,
                    details: null
                };
            }
        })
    );
    
    // Create result cards
    detailedResults.forEach(result => {
        const card = createResultCard(result, user_preferences);
        resultsContainer.appendChild(card);
    });
    
    // Show results section
    resultsSection.classList.remove('hidden');
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Create a result card
function createResultCard(result, userPreferences) {
    const card = document.createElement('div');
    card.className = 'result-card';
    
    const features = result.details ? result.details.features : {};
    
    card.innerHTML = `
        <div class="result-header">
            <div class="result-rank">${result.rank}</div>
            <div class="result-geoid">ID: ${result.geoid}</div>
        </div>
        
        <div class="result-features">
            <div class="feature-item">
                <i class="fas fa-users"></i>
                <div>
                    <div class="feature-value">
                        ${features.population_density ? 
                            Math.round(features.population_density.value).toLocaleString() : 
                            'N/A'
                        }
                    </div>
                    <div class="feature-label">people/km²</div>
                </div>
            </div>
            
            <div class="feature-item">
                <i class="fas fa-tree"></i>
                <div>
                    <div class="feature-value">
                        ${features.parks_per_sqkm ? 
                            features.parks_per_sqkm.value.toFixed(1) : 
                            'N/A'
                        }
                    </div>
                    <div class="feature-label">parks/km²</div>
                </div>
            </div>
            
            <div class="feature-item">
                <i class="fas fa-utensils"></i>
                <div>
                    <div class="feature-value">
                        ${features.restaurants_per_sqkm ? 
                            Math.round(features.restaurants_per_sqkm.value) : 
                            'N/A'
                        }
                    </div>
                    <div class="feature-label">restaurants/km²</div>
                </div>
            </div>
        </div>
        
        <div class="result-distance">
            <strong>Match Score:</strong> ${(100 - Math.min(result.distance / 100, 100)).toFixed(1)}%
            <br>
            <small>Distance: ${result.distance.toFixed(2)}</small>
        </div>
    `;
    
    // Add click handler for more details
    card.addEventListener('click', () => {
        showNeighborhoodDetails(result);
    });
    
    return card;
}

// Show neighborhood details (placeholder for future enhancement)
function showNeighborhoodDetails(result) {
    alert(`Neighborhood Details\n\nGEOID: ${result.geoid}\nMatch Distance: ${result.distance.toFixed(2)}\n\nClick OK to continue.`);
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

// Hide error
function hideError() {
    errorSection.classList.add('hidden');
}

// Hide all sections
function hideAllSections() {
    loadingSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

// Initialize slider values on page load
document.addEventListener('DOMContentLoaded', () => {
    populationDensityValue.textContent = parseInt(populationDensitySlider.value).toLocaleString();
    parksDensityValue.textContent = parseFloat(parksDensitySlider.value).toFixed(1);
    restaurantsDensityValue.textContent = parseInt(restaurantsDensitySlider.value);
});

// Add some interactive animations
document.addEventListener('DOMContentLoaded', () => {
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe result cards when they're created
    const originalCreateResultCard = createResultCard;
    window.createResultCard = function(...args) {
        const card = originalCreateResultCard.apply(this, args);
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
        return card;
    };
});


