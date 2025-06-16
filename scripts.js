// scripts.js
// Language Toggle
const languageToggle = document.getElementById('languageToggle');
const languageLabel = languageToggle.querySelector('.language-label');

languageToggle.addEventListener('click', () => {
    document.body.classList.toggle('hindi');
    if (document.body.classList.contains('hindi')) {
        languageLabel.textContent = 'English';
    } else {
        languageLabel.textContent = 'हिंदी';
    }
    localStorage.setItem('language', document.body.classList.contains('hindi') ? 'hindi' : 'english');
});

if (localStorage.getItem('language') === 'hindi') {
    document.body.classList.add('hindi');
    languageLabel.textContent = 'English';
}

// Theme Toggle (Dark Mode Only)
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('i');
let themeState = 0; // 0 = light, 1 = dark

themeToggle.addEventListener('click', () => {
    themeState = (themeState + 1) % 2;
    document.body.classList.remove('dark-mode');
    if (themeState === 1) {
        document.body.classList.add('dark-mode');
        themeIcon.classList.remove('far', 'fa-moon');
        themeIcon.classList.add('fas', 'fa-sun');
        themeToggle.setAttribute('aria-label', 'Toggle light mode');
    } else {
        themeIcon.classList.remove('fas', 'fa-sun');
        themeIcon.classList.add('far', 'fa-moon');
        themeToggle.setAttribute('aria-label', 'Toggle dark mode');
    }
    localStorage.setItem('themeState', themeState.toString());
});

const savedThemeState = localStorage.getItem('themeState');
if (savedThemeState) {
    themeState = parseInt(savedThemeState);
    if (themeState === 1) {
        document.body.classList.add('dark-mode');
        themeIcon.classList.remove('far', 'fa-moon');
        themeIcon.classList.add('fas', 'fa-sun');
        themeToggle.setAttribute('aria-label', 'Toggle light mode');
    }
}

// Test Functions
async function dnsLookup(domain, type = 'A') {
    try {
        const response = await fetch(`https://dns.google/resolve?name=${encodeURIComponent(domain)}&type=${type}`);
        const data = await response.json();
        return data.Answer ? data.Answer.map(a => a.data) : [];
    } catch (error) {
        console.error('DNS lookup failed:', error);
        return [];
    }
}

async function isReachable(url) {
    try {
        const response = await fetch(url, {
            method: 'HEAD',
            mode: 'no-cors',
            cache: 'no-store'
        });
        return true;
    } catch (error) {
        return false;
    }
}

// Website Test Functions
async function testIPv6(domain) {
    try {
        const ipv6 = await dnsLookup(domain, 'AAAA');
        return ipv6.length > 0;
    } catch {
        return false;
    }
}

async function testDNSSEC(domain) {
    try {
        const response = await fetch(`https://dnssec-analyzer.vercel.app/api/analyze?domain=${encodeURIComponent(domain)}`);
        const data = await response.json();
        return data.dnssec === 'valid';
    } catch {
        return false;
    }
}

async function testHTTPS(domain) {
    return await isReachable(`https://${domain}`);
}

async function testSecurityHeaders(domain) {
    try {
        const response = await fetch(`https://securityheaders.com/?q=${encodeURIComponent(domain)}&hide=on&followRedirects=on`);
        const text = await response.text();
        return {
            hsts: text.includes('Strict-Transport-Security'),
            xss: text.includes('X-XSS-Protection'),
            frameOptions: text.includes('X-Frame-Options'),
            contentType: text.includes('X-Content-Type-Options'),
            csp: text.includes('Content-Security-Policy')
        };
    } catch {
        return false;
    }
}

// Email Test Functions
async function testSPF(domain) {
    try {
        const records = await dnsLookup(domain, 'TXT');
        return records.some(r => r.includes('v=spf1'));
    } catch {
        return false;
    }
}

async function testDKIM(domain) {
    try {
        const records = await dnsLookup(`default._domainkey.${domain}`, 'TXT');
        return records.length > 0;
    } catch {
        return false;
    }
}

async function testDMARC(domain) {
    try {
        const records = await dnsLookup(`_dmarc.${domain}`, 'TXT');
        return records.some(r => r.includes('v=DMARC1'));
    } catch {
        return false;
    }
}

// Connection Test Functions
async function testClientIPv6() {
    try {
        await fetch('https://ipv6-test.com/api/myip.php', { mode: 'no-cors' });
        return true;
    } catch {
        return false;
    }
}

// Main Test Functions
async function testWebsite() {
    const domain = document.querySelector('#websiteTestBtn').closest('.test-card').querySelector('input').value.trim();
    if (!domain) return alert('Please enter a domain name');
    const btn = document.getElementById('websiteTestBtn');
    const resultsContainer = document.getElementById('websiteResults');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    resultsContainer.innerHTML = '';
    try {
        const tests = [
            { name: 'IPv6', func: testIPv6, desc: 'Website is reachable via IPv6' },
            { name: 'DNSSEC', func: testDNSSEC, desc: 'Domain names are cryptographically signed' },
            { name: 'HTTPS', func: testHTTPS, desc: 'Website uses secure HTTPS connection' },
            { name: 'Security Headers', func: testSecurityHeaders, desc: 'Important security headers are set' }
        ];
        for (const test of tests) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'test-result';
            loadingDiv.innerHTML = `
                <div class="test-name"><i class="fas fa-spinner spinner"></i> ${test.name}</div>
                <div class="test-description">${test.desc}</div>
            `;
            resultsContainer.appendChild(loadingDiv);
            const result = await test.func(domain);
            loadingDiv.className = `test-result ${result ? 'success' : 'failure'}`;
            let resultContent = '';
            if (typeof result === 'object') {
                resultContent = Object.entries(result).map(([header, supported]) => `
                    <div class="test-description">
                        <i class="fas ${supported ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                        ${header}: ${supported ? 'Yes' : 'No'}
                    </div>
                `).join('');
            }
            loadingDiv.innerHTML = `
                <div class="test-name">
                    <i class="fas ${result ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                    ${test.name}
                </div>
                <div class="test-description">${test.desc}</div>
                ${resultContent}
            `;
        }
    } catch (error) {
        alert('Test failed: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play"></i> <span class="language-english">Start Test</span><span class="language-hindi">परीक्षण शुरू करें</span>';
    }
}

async function testEmail() {
    const domain = document.querySelector('#emailTestBtn').closest('.test-card').querySelector('input').value.trim();
    if (!domain) return alert('Please enter a domain name');
    const btn = document.getElementById('emailTestBtn');
    const resultsContainer = document.getElementById('emailResults');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    resultsContainer.innerHTML = '';
    try {
        const tests = [
            { name: 'SPF', func: testSPF, desc: 'Sender Policy Framework record exists' },
            { name: 'DKIM', func: testDKIM, desc: 'DomainKeys Identified Mail record exists' },
            { name: 'DMARC', func: testDMARC, desc: 'Domain-based Message Authentication reporting exists' }
        ];
        for (const test of tests) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'test-result';
            loadingDiv.innerHTML = `
                <div class="test-name"><i class="fas fa-spinner spinner"></i> ${test.name}</div>
                <div class="test-description">${test.desc}</div>
            `;
            resultsContainer.appendChild(loadingDiv);
            const result = await test.func(domain);
            loadingDiv.className = `test-result ${result ? 'success' : 'failure'}`;
            loadingDiv.innerHTML = `
                <div class="test-name">
                    <i class="fas ${result ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                    ${test.name}
                </div>
                <div class="test-description">${test.desc}</div>
            `;
        }
    } catch (error) {
        alert('Test failed: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play"></i> <span class="language-english">Start Test</span><span class="language-hindi">परीक्षण शुरू करें</span>';
    }
}

async function testConnection() {
    const btn = document.getElementById('connectionTestBtn');
    const resultsContainer = document.getElementById('connectionResults');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    resultsContainer.innerHTML = '';
    try {
        const tests = [
            { name: 'IPv6', func: testClientIPv6, desc: 'Your connection supports IPv6' }
        ];
        for (const test of tests) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'test-result';
            loadingDiv.innerHTML = `
                <div class="test-name"><i class="fas fa-spinner spinner"></i> ${test.name}</div>
                <div class="test-description">${test.desc}</div>
            `;
            resultsContainer.appendChild(loadingDiv);
            const result = await test.func();
            loadingDiv.className = `test-result ${result ? 'success' : 'failure'}`;
            loadingDiv.innerHTML = `
                <div class="test-name">
                    <i class="fas ${result ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                    ${test.name}
                </div>
                <div class="test-description">${test.desc}</div>
            `;
        }
    } catch (error) {
        alert('Test failed: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play"></i> <span class="language-english">Start Test</span><span class="language-hindi">परीक्षण शुरू करें</span>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('websiteTestBtn').addEventListener('click', testWebsite);
    document.getElementById('emailTestBtn').addEventListener('click', testEmail);
    document.getElementById('connectionTestBtn').addEventListener('click', testConnection);
    document.querySelector('#websiteTestBtn').closest('.test-card').querySelector('input')
        .addEventListener('keypress', (e) => {
            if (e.key === 'Enter') testWebsite();
        });
    document.querySelector('#emailTestBtn').closest('.test-card').querySelector('input')
        .addEventListener('keypress', (e) => {
            if (e.key === 'Enter') testEmail();
        });
});
