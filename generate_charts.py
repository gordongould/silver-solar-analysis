#!/usr/bin/env python3
"""Generate charts for silver-solar-AI commodity analysis."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ============================================================
# CHART 1: Solar Silver Demand vs. Installed Capacity (Decoupling)
# ============================================================
years = np.arange(2020, 2031)
# Annual solar installations (GW) — IEA/BNEF estimates
installed_gw = np.array([150, 185, 240, 400, 593, 630, 680, 720, 760, 800, 830])
# PV silver intensity (mg/W)
mg_per_w = np.array([18.0, 16.5, 15.0, 13.5, 12.2, 9.2, 6.7, 5.8, 5.0, 4.2, 3.5])
# Implied total PV silver demand (Moz)
silver_moz_pv = (installed_gw * mg_per_w * 1e9 / 31.1035 / 1e6).astype(int)

# Override first 4 years with real data
silver_moz_pv[:5] = [80, 95, 115, 175, 232]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax1.set_facecolor('#f8f9fa')

color1 = '#1a73e8'
color2 = '#ea4335'

ax1.bar(years, silver_moz_pv, color=color1, alpha=0.7, width=0.6, label='PV Silver Demand (Moz)')
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Million Ounces (Moz)', color=color1, fontsize=11)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 350)

ax2 = ax1.twinx()
ax2.plot(years, installed_gw, 'o-', color=color2, linewidth=2.5, markersize=6, label='Solar Installations (GW)')
ax2.set_ylabel('Gigawatts Installed', color=color2, fontsize=11)
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 1000)

# Annotate key data points
for i, (y, moz) in enumerate(zip(years, silver_moz_pv)):
    if i >= 4:  # Only label projected after 2024
        ax1.annotate(f'{moz}', (y, moz), textcoords="offset points",
                     xytext=(0, 5), ha='center', fontsize=8, color=color1, fontweight='bold')
        
for i, (y, gw) in enumerate(zip(years, installed_gw)):
    if i % 2 == 0:
        ax2.annotate(f'{gw}GW', (y, gw), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=8, color=color2, fontweight='bold')

# Decoupling annotation
ax1.annotate('Decoupling:\nGW up, Moz down', xy=(2026, 140), fontsize=9,
             ha='center', fontweight='bold', color='#1a1a1a',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3cd', edgecolor='#ffc107', alpha=0.9))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

plt.title('Solar Silver Demand vs. Installed Capacity (2020-2030)\nThe Decoupling', fontsize=13, fontweight='bold')
fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/01_solar_silver_decoupling.png', dpi=150)
plt.close()
print("Chart 1 done")

# ============================================================
# CHART 2: Silver Intensity Per Watt (mg/W) — Thrifting Trajectory
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor('#f8f9fa')

# Historical and projected silver intensity
years_int = np.arange(2020, 2031)
intensity = [18.0, 16.5, 15.0, 13.5, 12.2, 9.2, 6.7, 5.8, 5.0, 4.2, 3.5]

# Sources for specific datapoints
ax.plot(years_int, intensity, 'o-', color='#7b2d8e', linewidth=2.5, markersize=7, zorder=3)
ax.fill_between(years_int, intensity, alpha=0.15, color='#7b2d8e')

# Add data labels with source notes
annotations = {
    2024: ('12.2 mg/W\n(actual)', '#7b2d8e'),
    2026: ('6.7 mg/W\n(-45% in 2yr)', '#e63946'),
    2030: ('3.0 mg/W\n(INES target)', '#2d6a4f'),
}
for yr, (label, clr) in annotations.items():
    idx = list(years_int).index(yr)
    ax.annotate(label, (yr, intensity[idx]), textcoords="offset points",
                xytext=(20, -15), ha='center', fontsize=9, color=clr, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=clr, lw=1.5))

# Thrifting drivers table
ax.text(0.98, 0.05, 
    'Thrifting Drivers:\n' +
    '• Copper paste substitution (rear-side)\n' +
    '• Aiko silver-free back-contact module\n' +
    '• LONGi base-metal substitution (Q2 2026)\n' +
    '• CEA at INES: <14 mg/Wp demonstrated\n' +
    '• Jinko silver-coated copper pastes',
    transform=ax.transAxes, fontsize=8, verticalalignment='bottom',
    horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.9))

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Silver Intensity (mg per Watt)', fontsize=11)
ax.set_title('Silver Intensity in Solar: The Thrifting Trajectory (2020-2030)', fontsize=13, fontweight='bold')
ax.set_ylim(0, 22)
ax.grid(axis='y', alpha=0.3)

fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/02_silver_intensity_thrifting.png', dpi=150)
plt.close()
print("Chart 2 done")

# ============================================================
# CHART 3: Silver Demand by Sector — Stacked Area (2020-2030)
# ============================================================
years_s = np.arange(2020, 2031)

# Solar PV (Moz)
solar = [80, 95, 115, 175, 232, 186.6, 151, 140, 130, 118, 105]

# Data Centers & AI (Moz) — smaller base, fast growth
datacenter = [5, 6, 8, 11, 15, 22, 30, 40, 52, 65, 80]

# EVs & Automotive
evs = [30, 35, 42, 50, 72, 80, 88, 96, 105, 114, 124]

# Other industrial (electronics, etc.)
other = [220, 225, 235, 245, 250, 252, 248, 245, 242, 240, 238]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor('#f8f9fa')

ax.stackplot(years_s, solar, datacenter, evs, other,
             labels=['Solar PV', 'Data Centers & AI', 'EVs & Automotive', 'Other Industrial'],
             colors=['#f4a261', '#264653', '#e76f51', '#a8dadc'],
             alpha=0.85)

# Cross-over annotation
ax.annotate('Data Centers &\nAI crossover\ninto solar\nterritory?', 
            xy=(2029, 165), fontsize=9, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3cd', edgecolor='#ffc107', alpha=0.9))

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Million Ounces (Moz)', fontsize=11)
ax.set_title('Industrial Silver Demand by Sector (2020-2030)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.set_ylim(0, 700)
ax.grid(axis='y', alpha=0.3)

fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/03_silver_demand_by_sector.png', dpi=150)
plt.close()
print("Chart 3 done")

# ============================================================
# CHART 4: Growth Rates Comparison — Solar Silver vs DC Silver
# ============================================================
categories = ['Solar PV\nSilver Demand\n(2024→2030)', 'Data Centers\n& AI Silver\n(2024→2030)', 'EVs &\nAutomotive\n(2024→2030)', 'Solar\nInstalled\nCapacity\n(GW, 2024→2030)']
growth_rates = [-54.7, 433.3, 72.2, 40.0]  # percent

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor('#f8f9fa')

colors_bar = ['#e63946', '#264653', '#e76f51', '#2a9d8f']
bars = ax.bar(categories, growth_rates, color=colors_bar, alpha=0.85, width=0.55)

# Value labels
for bar in bars:
    val = bar.get_height()
    label = f'{val:+.1f}%'
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (8 if val > 0 else -20),
            label, ha='center', fontsize=11, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_ylabel('Growth Rate (%)', fontsize=11)
ax.set_title('Crossover Math: Which Sector Grows Faster?', fontsize=13, fontweight='bold')
ax.text(0.01, 0.95, 
    'Key Insight:\nData Center silver demand grows 433%\nvs solar silver declines 55%.\nBut solar starts from 232 Moz base;\nDC starts from ~15 Moz.\nAbsolute crossover ~2029-2031.',
    transform=ax.transAxes, fontsize=9, verticalalignment='top',
    bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.9))
ax.set_ylim(-80, 500)
ax.grid(axis='y', alpha=0.3)

fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/04_growth_rates_comparison.png', dpi=150)
plt.close()
print("Chart 4 done")

# ============================================================
# CHART 5: Absolute Moz Crossover — Solar vs Data Centers
# ============================================================
years_c = np.arange(2024, 2032)
solar_abs = np.array([232, 186.6, 151, 140, 130, 118, 105, 95])
dc_abs = np.array([15, 22, 30, 40, 52, 65, 80, 95])

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor('#f8f9fa')

ax.plot(years_c, solar_abs, 'o-', color='#1a73e8', linewidth=2.5, markersize=7, label='Solar PV Silver Demand (Moz)')
ax.plot(years_c, dc_abs, 's-', color='#ea4335', linewidth=2.5, markersize=7, label='Data Center Silver Demand (Moz)')

# Fill between
ax.fill_between(years_c, solar_abs, dc_abs, where=(solar_abs > dc_abs),
                interpolate=True, alpha=0.1, color='#1a73e8')
ax.fill_between(years_c, solar_abs, dc_abs, where=(solar_abs <= dc_abs),
                interpolate=True, alpha=0.15, color='#ea4335')

# Find crossover point
for i in range(len(years_c)-1):
    if solar_abs[i] > dc_abs[i] and solar_abs[i+1] <= dc_abs[i+1]:
        cross_x = years_c[i+1]
        cross_y = dc_abs[i+1]
        ax.annotate(f'Crossover ~{int(cross_x)}', xy=(cross_x, cross_y),
                    xytext=(cross_x-2, cross_y-35),
                    fontsize=11, fontweight='bold', color='#1a1a1a',
                    arrowprops=dict(arrowstyle='->', color='#1a1a1a', lw=2),
                    bbox=dict(boxstyle='round', facecolor='#fff3cd', edgecolor='none', alpha=0.8))
        break

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Silver Demand (Million Ounces)', fontsize=11)
ax.set_title('The Crossover: Solar vs. Data Center Silver Demand (2024-2031)', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.set_xlim(2023.5, 2031.5)
ax.set_ylim(0, 260)

fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/05_crossover_solar_vs_dc.png', dpi=150)
plt.close()
print("Chart 5 done")

# ============================================================
# CHART 6: Solar Cost Per Watt Trajectory
# ============================================================
years_lcoe = np.arange(2010, 2031)
# Utility-scale solar LCOE ($/MWh nominal)
lcoe = [300, 250, 180, 130, 100, 75, 60, 50, 43, 38, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25]
# Equivalent $/W (rough: /200 conversion for utility scale)
cost_per_watt = [l/200 for l in lcoe]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: LCOE
ax1.set_facecolor('#f8f9fa')
ax1.plot(years_lcoe, lcoe, 'o-', color='#2a9d8f', linewidth=2, markersize=4)
ax1.fill_between(years_lcoe, lcoe, alpha=0.15, color='#2a9d8f')
ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('LCOE ($/MWh)', fontsize=10)
ax1.set_title('Utility-Scale Solar LCOE\n(2010-2030)', fontsize=11, fontweight='bold')
ax1.grid(alpha=0.3)
ax1.set_ylim(0, 350)

# Annotate key milestones
ax1.annotate('DOE SunShot\n$0.03/kWh goal met', xy=(2025, 29), xytext=(2018, 80),
            fontsize=8, arrowprops=dict(arrowstyle='->', color='#2a9d8f'),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax1.annotate('DOE target:\n$0.02/kWh', xy=(2030, 25), xytext=(2026, 60),
            fontsize=8, arrowprops=dict(arrowstyle='->', color='#2a9d8f'),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Right: Silver cost as % of panel
ax2.set_facecolor('#f8f9fa')
years_pct = np.array([2020, 2021, 2022, 2023, 2024, 2025, 2026])
silver_pct = [5, 6, 8, 9, 11, 14, 10]  # percent of module cost, based on silver price fluctuations
ax2.fill_between(years_pct, silver_pct, alpha=0.4, color='#f4a261')
ax2.plot(years_pct, silver_pct, 'o-', color='#e76f51', linewidth=2.5, markersize=7)
ax2.set_xlabel('Year', fontsize=10)
ax2.set_ylabel('Silver as % of Panel Cost', fontsize=10)
ax2.set_title('Silver Cost Pressure\non Solar Manufacturers', fontsize=11, fontweight='bold')
ax2.grid(alpha=0.3)
ax2.set_ylim(0, 20)
ax2.annotate('Silver hit $117/oz\nJan 2026 → thrifting\nkicks into overdrive',
            xy=(2026, 10), xytext=(2022, 17), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='#e76f51'),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

fig.suptitle("Solar Economics: Cost Per Watt and Silver's Share", fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/06_solar_costs.png', dpi=150)
plt.close()
print("Chart 6 done")

# ============================================================
# CHART 7: Thin Film Solar Market Share Forecast
# ============================================================
categories_tf = ['2024\n(Actual)', '2025', '2027', '2030']
# Thin film as % of total PV market
thin_film_pct = [5, 7, 12, 20]
c_si_pct = [95, 93, 88, 80]

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_facecolor('#f8f9fa')

x = np.arange(len(categories_tf))
width = 0.35

bars1 = ax.bar(x - width/2, c_si_pct, width, label='Crystalline Silicon (c-Si)', color='#457b9d', alpha=0.8)
bars2 = ax.bar(x + width/2, thin_film_pct, width, label='Thin Film (CdTe, CIGS, Perovskite)', color='#2a9d8f', alpha=0.8)

for bar in bars2:
    val = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{int(val)}%', ha='center', fontsize=9, fontweight='bold', color='#2a9d8f')

ax.set_xticks(x)
ax.set_xticklabels(categories_tf)
ax.set_ylabel('Market Share (%)', fontsize=11)
ax.set_title('Thin Film Solar Market Share Forecast\n(2024-2030)', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(0, 105)
ax.grid(axis='y', alpha=0.3)

# Bottleneck annotation
ax.text(0.5, 0.85, 
    'Key Bottlenecks:\n'
    '• Perovskite stability & scale-up (lab→fab gap)\n'
    '• CdTe: tellurium supply constraint (~2,000t/yr)\n'
    '• CIGS: indium price & availability\n'
    '• Thin film ≈3% of global market in 2024\n'
    '• Mordor Intelligence: 58.8→149.4 GW by 2030 (20.5% CAGR)\n'
    '• First Solar (CdTe) dominant in US utility',
    transform=ax.transAxes, fontsize=8, verticalalignment='top',
    bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.9))

fig.tight_layout()
plt.savefig('/Users/tumples/silver-solar-analysis/charts/07_thin_film_share.png', dpi=150)
plt.close()
print("Chart 7 done")

# ============================================================
# CHART 8: Summary — Key Metrics Table
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')

table_data = [
    ['Metric', '2024', '2025', '2026E', '2030E', 'Trend'],
    ['Solar Installations (GW/yr)', '593', '630', '680', '830', '↑ +40%'],
    ['PV Silver Demand (Moz)', '232', '186.6', '151', '105', '↓ -55%'],
    ['Silver Intensity (mg/W)', '12.2', '9.2', '6.7', '3.5', '↓ -71%'],
    ['Data Center Silver (Moz)', '15', '22', '30', '80', '↑ +433%'],
    ['EV Silver Demand (Moz)', '72', '80', '88', '124', '↑ +72%'],
    ['Thin Film Share (%)', '5%', '7%', '10%', '20%', '↑ 4×'],
    ['Silver Weight in EV (g)', '25-50', '25-50', '25-50', '35-60*', '↑ *SSB'],
    ['Silver Market Deficit (Moz)', '-195', '-40', '-46', '~150', 'Persistent'],
    ['Gold Price ($/oz)', '~$2,700', '~$3,650', '~$4,250', '~$5,500**', '↑ **est'],
    ['Copper Price ($/lb)', '~$4.50', '~$4.90', '~$6.33', '~$6.80**', '↑ **est'],
]

table = ax.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.16]*6)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.6)

# Style header
for j in range(6):
    table[(0, j)].set_facecolor('#264653')
    table[(0, j)].set_text_props(color='white', fontweight='bold')

# Color rows by theme
for i in range(1, len(table_data)):
    bg = '#e8f4f8' if i % 2 == 0 else 'white'
    if i in [2, 3]:  # Solar silver
        bg = '#fce4ec'
    elif i == 4:  # Data centers
        bg = '#e0f2f1'
    for j in range(6):
        table[(i, j)].set_facecolor(bg)

plt.title('Silver & Solar Commodity Dashboard — Key Metrics (2024-2030)', fontsize=14, fontweight='bold', pad=20)
plt.savefig('/Users/tumples/silver-solar-analysis/charts/08_summary_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 8 done")

print("\n=== All 8 charts generated successfully ===")
