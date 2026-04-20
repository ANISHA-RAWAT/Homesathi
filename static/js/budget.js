
function formatINR(n) {
    if (n >= 10000000) return '₹' + (n/10000000).toFixed(2) + ' Cr';
    if (n >= 100000)   return '₹' + (n/100000).toFixed(2) + ' L';
    return '₹' + Math.round(n).toLocaleString('en-IN');
}

// Slider display
document.getElementById('interestSlider').addEventListener('input', function() {
    document.getElementById('interestDisplay').textContent = this.value + '%';
});
document.getElementById('tenureSlider').addEventListener('input', function() {
    document.getElementById('tenureDisplay').textContent = this.value + ' years';
});

function calculateEMI() {
    var P = parseFloat(document.getElementById('propPrice').value) || 0;
    var D = parseFloat(document.getElementById('downPayment').value) || 0;
    var r = parseFloat(document.getElementById('interestSlider').value) / 12 / 100;
    var n = parseFloat(document.getElementById('tenureSlider').value) * 12;
    var loan = P - D;
    if (loan <= 0 || r <= 0 || n <= 0) return;
    var emi = loan * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
    var totalPay = emi * n;
    var totalInt = totalPay - loan;
    document.getElementById('r-loan').textContent     = formatINR(loan);
    document.getElementById('r-emi').textContent      = formatINR(emi) + '/mo';
    document.getElementById('r-interest').textContent = formatINR(totalInt);
    document.getElementById('r-total').textContent    = formatINR(totalPay);
    document.getElementById('emiResult').classList.add('show');
}

function calculateAffordability() {
    var income   = parseFloat(document.getElementById('monthlyIncome').value) || 0;
    var expenses = parseFloat(document.getElementById('monthlyExpenses').value) || 0;
    var existing = parseFloat(document.getElementById('existingEMI').value) || 0;
    var savings  = parseFloat(document.getElementById('savings').value) || 0;
    var rate     = parseFloat(document.getElementById('affordRate').value) || 8.5;
    var maxEMI   = (income - expenses - existing) * 0.40;
    if (maxEMI <= 0) { alert('Your expenses exceed income. Please review your inputs.'); return; }
    var r = rate / 12 / 100;
    var n = 20 * 12; // 20 yr default
    var maxLoan = maxEMI * (Math.pow(1+r,n) - 1) / (r * Math.pow(1+r,n));
    var maxProp = maxLoan + savings;
    document.getElementById('afford-max').textContent = formatINR(maxProp);
    document.getElementById('afford-emi-note').textContent =
        'Max Monthly EMI: ' + formatINR(maxEMI) + ' | Loan: ' + formatINR(maxLoan) + ' | Down Payment: ' + formatINR(savings);
    // Build search link
    var searchUrl = "{% url 'property_search' %}?listing_type=sell";
    if (maxProp <= 5000000) searchUrl += '&max_price=5000000';
    else if (maxProp <= 15000000) searchUrl += '&max_price=15000000';
    document.getElementById('afford-search-link').href = searchUrl;
    document.getElementById('affordResult').classList.add('show');
}