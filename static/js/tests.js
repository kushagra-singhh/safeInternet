// API URL (change this to your actual API URL)
const API_URL = '/api';

// Website Test
const websiteTestBtn = document.getElementById('websiteTestBtn');
const websiteInput = document.getElementById('websiteInput');
const websiteResults = document.getElementById('websiteResults');

websiteTestBtn.addEventListener('click', async () => {
    const domain = websiteInput.value.trim();
    if (!domain) {
        alert('Please enter a domain name');
        return;
    }
    
    websiteTestBtn.disabled = true;
    websiteTestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span lang="en">Testing...</span><span lang="hi">परीक्षण जारी...</span>';
    websiteResults.innerHTML = '<div class="test-result"><div class="test-name"><i class="fas fa-spinner spinner"></i> <span lang="en">Running tests...</span><span lang="hi">परीक्षण चल रहा है...</span></div></div>';
    
    try {
        const response = await fetch(`${API_URL}/test/website`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ domain })
        });
        
        const data = await response.json();
        displayResults(websiteResults, data);
    } catch (error) {
        websiteResults.innerHTML = `<div class="test-result failure"><div class="test-name"><i class="fas fa-exclamation-circle"></i> Error</div><div class="test-description">${error.message}</div></div>`;
    } finally {
        websiteTestBtn.disabled = false;
        websiteTestBtn.innerHTML = '<i class="fas fa-play"></i> <span lang="en">Start Test</span><span lang="hi">परीक्षण शुरू करें</span>';
    }
});

// Email Test
const emailTestBtn = document.getElementById('emailTestBtn');
const emailInput = document.getElementById('emailInput');
const emailResults = document.getElementById('emailResults');

emailTestBtn.addEventListener('click', async () => {
    const domain = emailInput.value.trim();
    if (!domain) {
        alert('Please enter a domain name');
        return;
    }
    
    emailTestBtn.disabled = true;
    emailTestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span lang="en">Testing...</span><span lang="hi">परीक्षण जारी...</span>';
    emailResults.innerHTML = '<div class="test-result"><div class="test-name"><i class="fas fa-spinner spinner"></i> <span lang="en">Running tests...</span><span lang="hi">परीक्षण चल रहा है...</span></div></div>';
    
    try {
        const response = await fetch(`${API_URL}/test/email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ domain })
        });
        
        const data = await response.json();
        displayResults(emailResults, data);
    } catch (error) {
        emailResults.innerHTML = `<div class="test-result failure"><div class="test-name"><i class="fas fa-exclamation-circle"></i> Error</div><div class="test-description">${error.message}</div></div>`;
    } finally {
        emailTestBtn.disabled = false;
        emailTestBtn.innerHTML = '<i class="fas fa-play"></i> <span lang="en">Start Test</span><span lang="hi">परीक्षण शुरू करें</span>';
    }
});

// Connection Test
const connectionTestBtn = document.getElementById('connectionTestBtn');
const connectionResults = document.getElementById('connectionResults');

connectionTestBtn.addEventListener('click', async () => {
    connectionTestBtn.disabled = true;
    connectionTestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span lang="en">Testing...</span><span lang="hi">परीक्षण जारी...</span>';
    connectionResults.innerHTML = '<div class="test-result"><div class="test-name"><i class="fas fa-spinner spinner"></i> <span lang="en">Running tests...</span><span lang="hi">परीक्षण चल रहा है...</span></div></div>';
    
    try {
        const response = await fetch(`${API_URL}/test/connection`);
        const data = await response.json();
        displayResults(connectionResults, data);
    } catch (error) {
        connectionResults.innerHTML = `<div class="test-result failure"><div class="test-name"><i class="fas fa-exclamation-circle"></i> Error</div><div class="test-description">${error.message}</div></div>`;
    } finally {
        connectionTestBtn.disabled = false;
        connectionTestBtn.innerHTML = '<i class="fas fa-play"></i> <span lang="en">Start Test</span><span lang="hi">परीक्षण शुरू करें</span>';
    }
});

// Function to display test results
function displayResults(container, data) {
    if (data.error) {
        container.innerHTML = `
        <div class="test-result failure">
            <div class="test-name">
                <i class="fas fa-exclamation-circle"></i> 
                <span lang="en">Error</span>
                <span lang="hi">त्रुटि</span>
            </div>
            <div class="test-description">${data.error}</div>
        </div>`;
        return;
    }
    
    let html = '';
    
    // Display overall score
    if (data.score !== null) {
        const scoreClass = data.score >= 80 ? 'success' : data.score >= 50 ? 'warning' : 'failure';
        html += `
        <div class="test-result ${scoreClass}">
            <div class="test-name">
                <i class="fas ${data.score >= 80 ? 'fa-check-circle' : data.score >= 50 ? 'fa-exclamation-triangle' : 'fa-times-circle'}"></i>
                <span lang="en">Overall Score: ${data.score}/100</span>
                <span lang="hi">समग्र स्कोर: ${data.score}/100</span>
            </div>
        </div>`;
    }
    
    // Display category results
    if (data.categories) {
        for (const [category, categoryData] of Object.entries(data.categories)) {
            const categoryScoreClass = categoryData.score >= 80 ? 'success' : categoryData.score >= 50 ? 'warning' : 'failure';
            
            html += `
            <div class="test-result ${categoryScoreClass}">
                <div class="test-name">
                    <i class="fas ${categoryData.score >= 80 ? 'fa-check-circle' : categoryData.score >= 50 ? 'fa-exclamation-triangle' : 'fa-times-circle'}"></i>
                    <span lang="en">${categoryData.name}: ${categoryData.score}/100</span>
                    <span lang="hi">${getCategoryNameHindi(categoryData.name)}: ${categoryData.score}/100</span>
                </div>`;
            
            // Display individual tests
            if (categoryData.tests) {
                for (const [testName, testData] of Object.entries(categoryData.tests)) {
                    const testScoreClass = testData.score >= 80 ? 'success' : testData.score >= 50 ? 'warning' : 'failure';
                    
                    html += `
                    <div class="test-description">
                        <i class="fas ${testData.score >= 80 ? 'fa-check' : testData.score >= 50 ? 'fa-exclamation' : 'fa-times'}" style="font-size: 0.8em;"></i>
                        <span lang="en">${testData.name}: ${testData.status}</span>
                        <span lang="hi">${getTestNameHindi(testData.name)}: ${getStatusHindi(testData.status)}</span>
                    </div>`;
                }
            }
            
            html += `</div>`;
        }
    }
    
    container.innerHTML = html;
}

// Helper function to translate category names to Hindi
function getCategoryNameHindi(name) {
    const translations = {
        'HTTPS': 'HTTPS',
        'IPv6': 'IPv6',
        'DNSSEC': 'DNSSEC',
        'Security Headers': 'सुरक्षा हेडर्स',
        'Email Security': 'ईमेल सुरक्षा',
        'SPF': 'SPF',
        'DKIM': 'DKIM',
        'DMARC': 'DMARC',
        'Connection': 'कनेक्शन',
        'SSL/TLS': 'SSL/TLS'
    };
    return translations[name] || name;
}

// Helper function to translate test names to Hindi
function getTestNameHindi(name) {
    const translations = {
        'HTTPS Available': 'HTTPS उपलब्ध',
        'Modern TLS': 'आधुनिक TLS',
        'HSTS': 'HSTS',
        'IPv6 Support': 'IPv6 समर्थन',
        'DNSSEC Enabled': 'DNSSEC सक्षम',
        'Content Security Policy': 'कंटेंट सिक्योरिटी पॉलिसी',
        'X-XSS-Protection': 'X-XSS-प्रोटेक्शन',
        'X-Frame-Options': 'X-फ्रेम-ऑप्शन्स',
        'SPF Record': 'SPF रिकॉर्ड',
        'DKIM Record': 'DKIM रिकॉर्ड',
        'DMARC Record': 'DMARC रिकॉर्ड',
        'STARTTLS Support': 'STARTTLS समर्थन'
    };
    return translations[name] || name;
}

// Helper function to translate status messages to Hindi
function getStatusHindi(status) {
    const translations = {
        'Passed': 'पास',
        'Failed': 'फेल',
        'Warning': 'चेतावनी',
        'Not Found': 'नहीं मिला',
        'Found': 'मिला',
        'Enabled': 'सक्षम',
        'Disabled': 'अक्षम',
        'Valid': 'मान्य',
        'Invalid': 'अमान्य',
        'Secure': 'सुरक्षित',
        'Insecure': 'असुरक्षित'
    };
    return translations[status] || status;
}
