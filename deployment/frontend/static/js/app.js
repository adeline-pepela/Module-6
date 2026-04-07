const API = '/api';

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.dataset.page;
        navigateTo(page);
    });
});

function navigateTo(page) {
    // Update nav
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // Update pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${page}`).classList.add('active');
    
    // Update title
    const titles = {
        overview: 'Executive Overview',
        customers: 'Customer Intelligence',
        risk: 'Risk Segmentation',
        predict: 'Real-Time Scoring',
        interventions: 'Retention Actions',
        model: 'Model Governance',
        evaluation: 'Model Evaluation'
    };
    document.getElementById('page-title').textContent = titles[page];
    
    // Load page data
    if (page === 'overview') loadOverview();
    if (page === 'customers') loadCustomers();
    if (page === 'risk') loadRiskSegmentation();
    if (page === 'model') loadModelGovernance();
    if (page === 'interventions') loadInterventions();
    if (page === 'evaluation') loadEvaluation();
}

// Load Overview Page
async function loadOverview() {
    try {
        // Show loading
        document.getElementById('kpi-total').textContent = 'Loading...';
        document.getElementById('kpi-churn').textContent = 'Loading...';
        document.getElementById('kpi-risk').textContent = 'Loading...';
        document.getElementById('kpi-revenue').textContent = 'Loading...';
        document.getElementById('kpi-prevention').textContent = 'Loading...';
        document.getElementById('kpi-efficiency').textContent = 'Loading...';
        
        const metrics = await axios.get(`${API}/dashboard/metrics`);
        const m = metrics.data;
        
        document.getElementById('kpi-total').textContent = m.total_customers.toLocaleString();
        document.getElementById('kpi-churn').textContent = (m.current_churn_rate * 100).toFixed(1) + '%';
        document.getElementById('kpi-risk').textContent = m.predicted_at_risk.toLocaleString();
        document.getElementById('kpi-revenue').textContent = 'KES ' + (m.revenue_at_risk / 1000000).toFixed(1) + 'M';
        document.getElementById('kpi-prevention').textContent = (m.prevention_rate * 100).toFixed(1) + '%';
        document.getElementById('kpi-efficiency').textContent = (m.campaign_efficiency * 100).toFixed(1) + '%';
        
        loadCharts();
    } catch (error) {
        console.error('Error loading overview:', error);
        document.getElementById('kpi-total').textContent = 'Error';
    }
}

async function loadCharts() {
    try {
        // Load all data in parallel for speed
        const [trend, risk, segment, perf] = await Promise.all([
            axios.get(`${API}/dashboard/churn-trend`),
            axios.get(`${API}/dashboard/risk-distribution`),
            axios.get(`${API}/dashboard/segment-analysis`),
            axios.get(`${API}/monitoring/performance-trend`)
        ]);
        
        // Trend Chart with interactive tooltips
        new Chart(document.getElementById('chart-trend'), {
            type: 'line',
            data: {
                labels: trend.data.map(d => d.month),
                datasets: [{
                    label: 'Actual Churn',
                    data: trend.data.map(d => d.actual_churn),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Predicted Churn',
                    data: trend.data.map(d => d.predicted_churn),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 2,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: (context) => `${context.dataset.label}: ${context.parsed.y} customers`
                        }
                    }
                }
            }
        });
        
        // Risk Distribution Chart with interactive tooltips
        new Chart(document.getElementById('chart-risk'), {
            type: 'doughnut',
            data: {
                labels: ['Ultra High', 'High', 'Medium', 'Low'],
                datasets: [{
                    data: [
                        risk.data['Ultra High']?.count || 0,
                        risk.data['High']?.count || 0,
                        risk.data['Medium']?.count || 0,
                        risk.data['Low']?.count || 0
                    ],
                    backgroundColor: ['#dc2626', '#ef4444', '#f59e0b', '#10b981'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 1.5,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        callbacks: {
                            label: (context) => {
                                const label = context.label;
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} customers (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
        
        // Segment Revenue Chart with interactive tooltips
        new Chart(document.getElementById('chart-segment'), {
            type: 'bar',
            data: {
                labels: segment.data.map(s => s.segment),
                datasets: [{
                    label: 'Revenue at Risk',
                    data: segment.data.map(s => s.at_risk * s.avg_revenue),
                    backgroundColor: '#2563eb',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 2,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        callbacks: {
                            label: (context) => {
                                const value = context.parsed.y;
                                return `Revenue at Risk: KES ${(value / 1000000).toFixed(2)}M`;
                            }
                        }
                    }
                }
            }
        });
        
        // Performance Trend Chart with interactive tooltips
        new Chart(document.getElementById('chart-performance'), {
            type: 'line',
            data: {
                labels: perf.data.map(p => p.month),
                datasets: [{
                    label: 'F1 Score',
                    data: perf.data.map(p => p.f1_score),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'PR-AUC',
                    data: perf.data.map(p => p.pr_auc),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 2,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        callbacks: {
                            label: (context) => `${context.dataset.label}: ${context.parsed.y.toFixed(4)}`
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// Load Customers Page
async function loadCustomers(filters = {}) {
    try {
        const params = new URLSearchParams({ limit: 100 });
        if (filters.risk_level) params.append('risk_level', filters.risk_level);
        if (filters.segment) params.append('segment', filters.segment);
        
        const res = await axios.get(`${API}/dashboard/customers/at-risk?${params}`);
        
        const tbody = document.getElementById('customer-table-body');
        tbody.innerHTML = res.data.map(c => `
            <tr>
                <td>${c.customer_id}</td>
                <td>${c.segment}</td>
                <td><span class="badge ${c.risk_level.toLowerCase()}">${c.risk_level}</span></td>
                <td>${(c.churn_probability * 100).toFixed(1)}%</td>
                <td>KES ${c.arpu.toLocaleString()}</td>
                <td>KES ${c.revenue_at_risk.toLocaleString()}</td>
                <td>${c.account_manager}</td>
                <td><button class="btn-primary" onclick="viewCustomer('${c.customer_id}')">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

function applyFilters() {
    const risk = document.getElementById('filter-risk').value;
    const segment = document.getElementById('filter-segment').value;
    const filters = {};
    if (risk) filters.risk_level = risk;
    if (segment) filters.segment = segment;
    loadCustomers(filters);
}

async function viewCustomer(id) {
    try {
        const res = await axios.get(`${API}/dashboard/customer/${id}`);
        const c = res.data;
        
        document.getElementById('modal-body').innerHTML = `
            <h2>Customer ${c.customer_id}</h2>
            <div style="margin-top: 1.5rem;">
                <p style="margin-bottom: 0.5rem;"><strong>Segment:</strong> ${c.segment}</p>
                <p style="margin-bottom: 0.5rem;"><strong>Total Revenue:</strong> KES ${c.total_revenue.toLocaleString()}</p>
                <p style="margin-bottom: 0.5rem;"><strong>ARPU:</strong> KES ${c.arpu.toLocaleString()}</p>
                <p style="margin-bottom: 0.5rem;"><strong>Churn Risk:</strong> ${(c.churn_probability * 100).toFixed(1)}%</p>
                <h3 style="margin-top: 1.5rem; margin-bottom: 1rem;">Top Churn Drivers</h3>
                <ul style="list-style: none; padding: 0;">
                    ${c.top_churn_drivers.map(d => `
                        <li style="padding: 0.75rem; background: #f8fafc; margin-bottom: 0.5rem; border-radius: 6px;">
                            ${d.feature}: ${d.value.toFixed(2)}
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
        
        document.getElementById('modal').classList.add('active');
    } catch (error) {
        console.error('Error loading customer:', error);
    }
}

function closeModal() {
    document.getElementById('modal').classList.remove('active');
}

// Load Risk Segmentation Page
async function loadRiskSegmentation() {
    try {
        const res = await axios.get(`${API}/dashboard/risk-distribution`);
        document.getElementById('risk-ultra').textContent = res.data['Ultra High']?.count || 0;
        document.getElementById('risk-high').textContent = res.data['High']?.count || 0;
        document.getElementById('risk-medium').textContent = res.data['Medium']?.count || 0;
        document.getElementById('risk-low').textContent = res.data['Low']?.count || 0;
    } catch (error) {
        console.error('Error loading risk segmentation:', error);
    }
}

// Score Customer
async function scoreCustomer() {
    const id = document.getElementById('input-customer-id').value.trim();
    if (!id) {
        alert('Please enter a Customer ID');
        return;
    }
    
    try {
        const res = await axios.get(`${API}/dashboard/customer/${id}`);
        const c = res.data;
        
        document.getElementById('result-customer-id').textContent = `Customer ID: ${c.customer_id}`;
        document.getElementById('result-probability').textContent = (c.churn_probability * 100).toFixed(1) + '%';
        
        const riskLevel = c.churn_probability > 0.8 ? 'Ultra High' : 
                         c.churn_probability >= 0.6 ? 'High' : 
                         c.churn_probability >= 0.4 ? 'Medium' : 'Low';
        
        const badge = document.getElementById('result-risk-level');
        badge.textContent = riskLevel;
        badge.className = 'badge-value';
        if (riskLevel === 'Ultra High' || riskLevel === 'High') badge.style.background = '#fee2e2';
        else if (riskLevel === 'Medium') badge.style.background = '#fef3c7';
        else badge.style.background = '#d1fae5';
        
        document.getElementById('result-drivers-list').innerHTML = c.top_churn_drivers
            .map(d => `<li>${d.feature}: ${d.value.toFixed(2)}</li>`).join('');
        
        const actions = {
            'Ultra High': 'Executive intervention required - Immediate personalized outreach with premium retention offer and dedicated account manager assignment.',
            'High': 'Personalized retention campaign - Assign dedicated account manager with custom package and priority support.',
            'Medium': 'Engagement campaign - Send targeted offers, service upgrade options, and satisfaction survey.',
            'Low': 'Loyalty nurturing - Continue regular engagement, satisfaction monitoring, and loyalty rewards.'
        };
        document.getElementById('result-action-text').textContent = actions[riskLevel];
        
        document.getElementById('scoring-result').style.display = 'block';
    } catch (error) {
        alert('Customer not found or error loading data');
        console.error('Error scoring customer:', error);
    }
}

// Load Interventions
async function loadInterventions() {
    const list = document.getElementById('interventions-list');
    list.innerHTML = '<p class="placeholder">Retention campaign tracking module - Coming soon</p>';
}

// Load Model Governance
async function loadModelGovernance() {
    try {
        const res = await axios.get(`${API}/monitoring/model-metrics`);
        document.getElementById('model-version').textContent = res.data.model_version;
        document.getElementById('model-sampling').textContent = res.data.sampling_strategy;
        document.getElementById('model-features').textContent = res.data.feature_count;
        document.getElementById('model-retrain').textContent = new Date(res.data.last_retrain_date).toLocaleDateString();
        document.getElementById('metric-f1').textContent = res.data.f1_score.toFixed(4);
        document.getElementById('metric-recall').textContent = (res.data.recall * 100).toFixed(2) + '%';
        document.getElementById('metric-precision').textContent = (res.data.precision * 100).toFixed(2) + '%';
        document.getElementById('metric-prauc').textContent = res.data.pr_auc.toFixed(4);
    } catch (error) {
        console.error('Error loading model governance:', error);
    }
}

// Initialize
loadOverview();

// Export customers to CSV
let currentCustomerData = [];

// Load Customers Page
async function loadCustomers(filters = {}) {
    try {
        const params = new URLSearchParams({ limit: 100 });
        if (filters.risk_level) params.append('risk_level', filters.risk_level);
        if (filters.segment) params.append('segment', filters.segment);
        
        const res = await axios.get(`${API}/dashboard/customers/at-risk?${params}`);
        currentCustomerData = res.data;
        
        const tbody = document.getElementById('customer-table-body');
        tbody.innerHTML = res.data.map(c => `
            <tr>
                <td>${c.customer_id}</td>
                <td>${c.segment}</td>
                <td><span class="badge ${c.risk_level.toLowerCase()}">${c.risk_level}</span></td>
                <td>${(c.churn_probability * 100).toFixed(1)}%</td>
                <td>KES ${c.arpu.toLocaleString()}</td>
                <td>KES ${c.revenue_at_risk.toLocaleString()}</td>
                <td>${c.account_manager}</td>
                <td><button class="btn-primary" onclick="viewCustomer('${c.customer_id}')">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

function exportCustomers() {
    if (currentCustomerData.length === 0) {
        alert('No data to export. Please load customers first.');
        return;
    }
    
    const csv = [
        ['Customer ID', 'Segment', 'Risk Level', 'Churn Probability', 'ARPU', 'Revenue at Risk', 'Account Manager'],
        ...currentCustomerData.map(c => [
            c.customer_id,
            c.segment,
            c.risk_level,
            (c.churn_probability * 100).toFixed(1) + '%',
            c.arpu,
            c.revenue_at_risk,
            c.account_manager
        ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `churn_predictions_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Bulk prediction
let bulkResults = [];

function handleBulkUpload() {
    const file = document.getElementById('bulk-upload').files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async (e) => {
        const text = e.target.result;
        const lines = text.split('\n').filter(l => l.trim());
        const customerIds = lines.slice(1).map(l => l.split(',')[0].trim());
        
        document.getElementById('bulk-status').textContent = `Processing ${customerIds.length} customers...`;
        document.getElementById('bulk-result').style.display = 'block';
        
        bulkResults = [];
        for (const id of customerIds) {
            try {
                const res = await axios.get(`${API}/dashboard/customer/${id}`);
                bulkResults.push({
                    customer_id: id,
                    churn_probability: res.data.churn_probability,
                    risk_level: res.data.churn_probability > 0.8 ? 'Ultra High' : 
                               res.data.churn_probability >= 0.6 ? 'High' : 
                               res.data.churn_probability >= 0.4 ? 'Medium' : 'Low',
                    segment: res.data.segment
                });
            } catch (error) {
                bulkResults.push({ customer_id: id, error: 'Not found' });
            }
        }
        
        document.getElementById('bulk-status').textContent = `✓ Processed ${bulkResults.length} customers`;
    };
    reader.readAsText(file);
}

function downloadBulkResults() {
    const csv = [
        ['Customer ID', 'Churn Probability', 'Risk Level', 'Segment', 'Status'],
        ...bulkResults.map(r => [
            r.customer_id,
            r.error ? 'N/A' : (r.churn_probability * 100).toFixed(1) + '%',
            r.error ? 'N/A' : r.risk_level,
            r.error ? 'N/A' : r.segment,
            r.error || 'Success'
        ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bulk_predictions_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Load Model Evaluation Page
async function loadEvaluation() {
    try {
        // Load model comparison
        const comparison = await axios.get(`${API}/evaluation/model-comparison`);
        const tbody = document.getElementById('comparison-body');
        tbody.innerHTML = comparison.data.map(m => `
            <tr style="${m.is_selected ? 'background: #dbeafe;' : ''}">
                <td><strong>${m.model_name}</strong></td>
                <td>${m.f1_score.toFixed(4)}</td>
                <td>${(m.recall * 100).toFixed(2)}%</td>
                <td>${(m.precision * 100).toFixed(2)}%</td>
                <td>${(m.accuracy * 100).toFixed(2)}%</td>
                <td>${m.roc_auc.toFixed(4)}</td>
                <td>${m.pr_auc.toFixed(4)}</td>
                <td>${m.is_selected ? '✓ Selected' : ''}</td>
            </tr>
        `).join('');
        
        // Load and render charts
        await loadEvaluationCharts();
    } catch (error) {
        console.error('Error loading evaluation:', error);
    }
}

async function loadEvaluationCharts() {
    const [features, cm, roc, pr] = await Promise.all([
        axios.get(`${API}/evaluation/feature-importance`),
        axios.get(`${API}/evaluation/confusion-matrix`),
        axios.get(`${API}/evaluation/roc-curve`),
        axios.get(`${API}/evaluation/pr-curve`)
    ]);
    
    // Feature Importance Chart
    new Chart(document.getElementById('chart-feature-importance'), {
        type: 'bar',
        data: {
            labels: features.data.map(f => f.feature_name),
            datasets: [{
                label: 'Importance Score',
                data: features.data.map(f => f.importance_score),
                backgroundColor: '#2563eb'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.2,
            plugins: { legend: { display: false } }
        }
    });
    
    // Confusion Matrix
    const cmData = cm.data;
    new Chart(document.getElementById('chart-confusion-matrix'), {
        type: 'bar',
        data: {
            labels: ['True Positive', 'False Positive', 'True Negative', 'False Negative'],
            datasets: [{
                label: 'Count',
                data: [cmData.true_positive, cmData.false_positive, cmData.true_negative, cmData.false_negative],
                backgroundColor: ['#10b981', '#ef4444', '#10b981', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.5,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        afterLabel: (context) => {
                            const total = cmData.total;
                            const pct = ((context.parsed.y / total) * 100).toFixed(1);
                            return `${pct}% of total`;
                        }
                    }
                }
            }
        }
    });
    
    // ROC Curve
    new Chart(document.getElementById('chart-roc'), {
        type: 'line',
        data: {
            labels: roc.data.fpr,
            datasets: [{
                label: `ROC Curve (AUC = ${roc.data.auc})`,
                data: roc.data.tpr,
                borderColor: '#2563eb',
                fill: false,
                tension: 0.4
            }, {
                label: 'Random Classifier',
                data: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                borderColor: '#94a3b8',
                borderDash: [5, 5],
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.5,
            scales: {
                x: { title: { display: true, text: 'False Positive Rate' } },
                y: { title: { display: true, text: 'True Positive Rate' } }
            },
            plugins: { legend: { position: 'bottom' } }
        }
    });
    
    // PR Curve
    new Chart(document.getElementById('chart-pr'), {
        type: 'line',
        data: {
            labels: pr.data.recall,
            datasets: [{
                label: `PR Curve (AUC = ${pr.data.auc})`,
                data: pr.data.precision,
                borderColor: '#10b981',
                fill: false,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.5,
            scales: {
                x: { title: { display: true, text: 'Recall' } },
                y: { title: { display: true, text: 'Precision' } }
            },
            plugins: { legend: { position: 'bottom' } }
        }
    });
}
