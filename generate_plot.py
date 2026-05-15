#!/usr/bin/env python3
"""
Generate visualization for Decline Curve Analysis blog post.
Creates a four-panel figure showing rate decline, cumulative production, 
decline rate evolution, and type curves.
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yaml


from pathlib import Path


def load_config(config_path=None):
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / 'config.yaml'
    if not config_path.exists():
        return {}
    with open(config_path) as _f:
        import yaml as _yaml
        return _yaml.safe_load(_f) or {}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Set publication-quality defaults

logger.info("Generating decline curve analysis plot...")
logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def hyperbolic_rate(t, qi, Di, b):
    return qi / (1 + b * Di * t) ** (1 / b)

def hyperbolic_cumulative(t, qi, Di, b):
    return (qi ** b) / ((1 - b) * Di) * (qi ** (1 - b) - 
           (qi / (1 + b * Di * t)) ** (1 - b))

np.random.seed(42)
n_months = 60

# Bakken well parameters
qi_oil = 750
Di = 0.08
b = 0.45

months = np.arange(n_months)
base_oil_rate = qi_oil / (1 + b * Di * months) ** (1 / b)
noise = np.random.normal(1.0, 0.1, n_months)
downtime = np.random.choice([0.9, 1.0], size=n_months, p=[0.1, 0.9])
oil_rate = base_oil_rate * noise * downtime

# Forecast
forecast_months = np.arange(0, 241)
forecast_rates = hyperbolic_rate(forecast_months, qi_oil, Di, b)
forecast_cumulative = hyperbolic_cumulative(forecast_months, qi_oil, Di, b)
cumulative_actual = np.cumsum(oil_rate * 30.44)

# Create figure
fig, axes = plt.subplots(2, 2, figsize=tuple(config.get('output', {}).get('figsize', [14, 10])))

# Rate decline - monochrome styling
ax1 = axes[0, 0]
ax1.scatter(months, oil_rate, alpha=0.5, s=20, color='black', label='Actual')
ax1.plot(forecast_months, forecast_rates, 'k-', linewidth=1.5, label='Hyperbolic Fit')
ax1.axhline(10, color='gray', linestyle='--', linewidth=1, label='Economic Limit (10 bbl/d)')
ax1.set_xlabel('Months On Production')
ax1.set_ylabel('Oil Rate (bbl/d)')
ax1.set_title('Production Rate Decline', fontsize=12)
ax1.legend(frameon=False, fontsize=9)
ax1.set_yscale('log')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Cumulative production - match units and scale
ax2 = axes[0, 1]
ax2.plot(months, cumulative_actual / 1000, 'k-', linewidth=1.5, label='Actual (60 mo)')
ax2.plot(forecast_months, forecast_cumulative / 1000, 'k--', linewidth=1.5, alpha=0.7, label='Forecast (240 mo)')

# EUR at 240 months
eur_value = forecast_cumulative[-1] / 1000
ax2.axhline(eur_value, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax2.text(120, eur_value + 20, f'EUR = {eur_value:.0f} Mbbl', fontsize=9, color='gray')

ax2.set_xlabel('Months On Production')
ax2.set_ylabel('Cumulative Oil (Mbbl)')
ax2.set_title('Cumulative Production', fontsize=12)
ax2.legend(frameon=False, fontsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Decline rate evolution - fix units to match model (per month, not per year)
instantaneous_decline_monthly = Di / (1 + b * Di * months)
ax3 = axes[1, 0]
ax3.plot(months, instantaneous_decline_monthly * 100, 'k-', linewidth=1.5)
ax3.set_xlabel('Months On Production')
ax3.set_ylabel('Nominal Decline Rate (%/month)')
ax3.set_title('Decline Rate Evolution', fontsize=12)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Type curve comparison - monochrome with b values in legend
ax4 = axes[1, 1]
time_normalized = np.linspace(0, 60, 100)

styles = [('k-', 1.5), ('k--', 1.5), ('k:', 1.5), ('k-', 1.0)]
alphas = [1.0, 0.85, 0.7, 0.5]

for idx, (b_val, label_base) in enumerate([(0, 'Exponential'), (0.3, 'Low Hyperbolic'), 
                                             (0.5, 'Mid Hyperbolic'), (0.8, 'High Hyperbolic')]):
    if b_val > 0:
        rate_curve = qi_oil / (1 + b_val * Di * time_normalized) ** (1 / b_val)
        label = f'{label_base} (b={b_val})'
    else:
        rate_curve = qi_oil * np.exp(-Di * time_normalized)
        label = f'{label_base} (b=0)'
    
    ax4.plot(time_normalized, rate_curve / qi_oil, styles[idx][0], 
            linewidth=styles[idx][1], alpha=alphas[idx], label=label)

ax4.set_xlabel('Months On Production')
ax4.set_ylabel('Normalized Rate (q/qi)')
ax4.set_title('Type Curve Comparison', fontsize=12)
ax4.legend(frameon=False, fontsize=9)
ax4.set_yscale('log')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('decline_curve_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

logger.info("Generated: decline_curve_analysis.png")
logger.info("Plot uses synthetic data for demonstration.\n")


