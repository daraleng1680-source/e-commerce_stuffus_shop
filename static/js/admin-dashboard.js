// ============ SALES CHART ============
function initSalesChart() {
    const salesCtx = document.getElementById('salesChart');
    if (!salesCtx) return;
    
    const salesChart = new Chart(salesCtx.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Sales',
                    data: [3200, 4100, 3800, 5200, 4900, 6100, 5800],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#28a745',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#2c3e50',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#6c757d'
                    }
                }
            }
        }
    });
}

// ============ CATEGORY CHART ============
function initCategoryChart() {
    const categoryCtx = document.getElementById('categoryChart');
    if (!categoryCtx) return;
    
    const categoryChart = new Chart(categoryCtx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Indoor Plants', 'Outdoor Plants', 'Accessories', 'Pots'],
            datasets: [
                {
                    data: [35, 25, 20, 20],
                    backgroundColor: [
                        '#28a745',
                        '#20c997',
                        '#17a2b8',
                        '#ffc107'
                    ],
                    borderColor: '#fff',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#2c3e50',
                        font: {
                            size: 12,
                            weight: '600'
                        },
                        padding: 15
                    }
                }
            }
        }
    });
}

// ============ SEARCH FUNCTIONALITY ============
function initSearchFunctionality() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function(e) {
        const query = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('table tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
    });
}

// ============ SIDEBAR TOGGLE (Mobile) ============
function initSidebarToggle() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    
    const isMobile = window.innerWidth <= 576;
    if (isMobile) {
        sidebar.classList.remove('active');
    }
}

// ============ INITIALIZE ALL ============
document.addEventListener('DOMContentLoaded', function() {
    initSalesChart();
    initCategoryChart();
    initSearchFunctionality();
    initSidebarToggle();
});
