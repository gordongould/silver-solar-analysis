#!/usr/bin/env python3
"""Charts 09-12: Silver supply deficits, substitution technologies, and bottleneck overlay."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = '/Users/tumples/silver-solar-analysis/charts'

# ============================================================
# CHART 9: The Grand Overlay — Demand vs Supply with Deficit
# ============================================================
years = np.arange(2024, 2032)

# Demand: Solar PV silver (Moz)
solar = np.array([232, 186.6, 151, 140, 130, 118, 105, 95])
# Demand: Data Center & AI silver (Moz)
dc = np.array([15, 22, 30, 40, 52, 65, 80, 95])
# Demand: Other industrial (electronics, EVs, investment, jewelry)
other = np.array([432, 421, 415, 410, 405, 400, 395, 390])
# Total demand
total_demand = solar + dc + other
# Total supply (mine + recycling) — roughly flat
total_supply = np.array([1030, 1035, 1040, 1040, 1045, 1045, 1050, 1050])
# Deficit
deficit = deficit = total_demand - total_supply

fig, ax1 = plt.subplots(figsize=(12, 6.5))
ax1.set_facecolor('#f8f9fa')

# Stacked area: demand components
ax1.stackplot(years, solar, dc, other,
              labels=['Solar PV Demand', 'Data Centers & AI', 'Other Demand (Electronics, EVs, Investment, Jewelry)'],
              colors=['#f4a261', '#264653', '#a8dadc'],
              alpha=0.7)

# Supply line
ax1.plot(years, total_supply, '-', color='#2a9d8f', linewidth=3, zorder=4,
         label='Total Supply (Mine + Recycling)')
ax1.fill_between(years, total_supply, total_demand, where=(total_demand > total_supply),
                 interpolate=True, alpha=0.25, color='#e63946', label='Deficit Gap')

# Annotate deficit values
for i, (y, d) in enumerate(zip(years, deficit)):
    if d > 0:
        ax1.annotate(f'-{d:.0f} Moz', (y, min(total_demand[i], total_supply[i]) + 10),
                    ha='center', fontsize=9, fontweight='bold', color='#e63946',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e63946', alpha=0.8))

# Cumulative deficit annotation
cumulative_deficit = np.cumsum(deficit)
ax1.text(0.98, 0.15, f'Cumulative Deficit\n2024-2031: ~{cumulative_deficit[-1]:.0f} Moz\n(London free float: ~136 Moz)\nAbove-ground stocks\nseverely depleted',
        transform=ax1.transAxes, fontsize=9, verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='#fce4ec', edgecolor='#e63946', alpha=0.95))

ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Million Ounces (Moz)', fontsize=11)
ax1.set_title('The Grand Overlay: Silver Demand, Supply & Structural Deficit (2024-2031)', fontsize=13, fontweight='bold')
ax1.set_ylim(0, 1300)
ax1.set_xlim(2023.5, 2031.5)
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(axis='y', alpha=0.3)

fig.tight_layout()
plt.savefig(f'{OUT}/09_grand_overlay_supply_demand.png', dpi=150)
plt.close()
print("Chart 9 done")

# ============================================================
# CHART 10: Cumulative Stock Depletion — The Emptying Vault
# ============================================================
years_d = np.arange(2021, 2032)

# Annual deficits from data (2021-2024 actual, 2025-2031 projected)
annual_deficit = np.array([50, 100, 200.6, 195, 40.3, 46.3, 65, 75, 70, 60, 45])
# Cumulative drawdown
cumulative = np.cumsum(annual_deficit)
# London free float trajectory (estimated)
london_float = np.array([750, 650, 500, 350, 220, 136, 110, 85, 60, 40, 25])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# Left: Annual deficits
ax1.set_facecolor('#f8f9fa')
colors_bar = ['#457b9d' if d < 50 else '#e63946' if d < 100 else '#c1121f' for d in annual_deficit]
bars1 = ax1.bar(years_d, annual_deficit, color=colors_bar, alpha=0.85, width=0.6)
ax1.axhline(y=0, color='black', linewidth=0.8)
for bar, val in zip(bars1, annual_deficit):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f'{val:.0f}', ha='center', fontsize=8, fontweight='bold')
ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('Annual Deficit (Moz)', fontsize=10)
ax1.set_title('Annual Silver Market Deficit\n(2021-2031)', fontsize=11, fontweight='bold')
ax1.set_ylim(-10, 250)
ax1.grid(axis='y', alpha=0.3)

# Right: Cumulative + London float
ax2.set_facecolor('#f8f9fa')
ax2.fill_between(years_d, cumulative, alpha=0.3, color='#e63946')
ax2.plot(years_d, cumulative, 'o-', color='#c1121f', linewidth=2.5, markersize=5, label='Cumulative Drawdown')
ax2.plot(years_d, london_float, 's-', color='#264653', linewidth=2.5, markersize=5, label='London Free Float (Est.)')

ax2.annotate('762 Moz drawn\ndown since 2021', xy=(2026, 762), xytext=(2022, 850),
            fontsize=9, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#c1121f', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Danger zone annotation
ax2.axhspan(0, 150, alpha=0.12, color='#e63946')
ax2.text(2025, 75, 'CRITICAL\nBUFFER\nZONE', fontsize=9, ha='center', fontweight='bold', color='#e63946')

ax2.set_xlabel('Year', fontsize=10)
ax2.set_ylabel('Million Ounces (Moz)', fontsize=10)
ax2.set_title('Cumulative Stock Depletion\n& London Vault Free Float', fontsize=11, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(axis='y', alpha=0.3)

fig.suptitle('The Emptying Vault: Silver Stock Depletion Dynamics', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
plt.savefig(f'{OUT}/10_cumulative_stock_depletion.png', dpi=150)
plt.close()
print("Chart 10 done")

# ============================================================
# CHART 11: Technologies That Reduce or Obviate Silver
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6.5))
ax.set_facecolor('#f8f9fa')
ax.axis('off')

# Define the substitution technology landscape as a table
tech_data = [
    ['Technology', 'Sector', 'Readiness\n(1-5)', 'Silver\nReduction', 'Maturity\nTimeline', 'Impact\nScore'],
    ['Copper paste in solar\n(rear-side substitution)', 'Solar PV', '★★★★★\n(5)', '30-50%\nper cell', 'NOW — 2026\nMainstream', 'CRITICAL\nAlready in production'],
    ['Aiko back-contact\n(silver-free module)', 'Solar PV', '★★★☆☆\n(3)', '80-100%', '2026-2028\nScaling', 'HIGH\nIf reliability proven'],
    ['Copper electroplating\n(HJT cells)', 'Solar PV', '★★★☆☆\n(3)', '90-100%', '2027-2030\nNeeds new equipment', 'HIGH\nNew fab lines needed'],
    ['Silver-coated copper\npastes (Jinko method)', 'Solar PV', '★★★★☆\n(4)', '40-60%', '2026-2027\nSpread rapidly', 'CRITICAL\nScreen-print compatible'],
    ['Graphene-based TIMs\n(for AI chips)', 'Data Centers\n& Electronics', '★★☆☆☆\n(2)', 'Partial\n(TIM only)', '2028-2032\nScaling challenges', 'MODERATE\nCost & scalability'],
    ['CNT Thermal Interface\nMaterials', 'Data Centers\n& Electronics', '★★☆☆☆\n(2)', 'Partial\n(TIM only)', '2028-2033\nContact resistance gap', 'LOW-MOD\nComparable to indium'],
    ['Copper wire bonding\n(semiconductor packaging)', 'Semiconductors', '★★★★★\n(5)', 'Reduced Ag\nin packaging', 'ALREADY\nMainstream', 'LOW\nAlready done'],
    ['Aluminum metallization\n(power semiconductors)', 'Semiconductors', '★★★★☆\n(4)', 'Reduced Ag\nin power devices', 'NOW\nOngoing shift', 'LOW-MOD\nNiche applications'],
    ['Perovskite-silicon\ntandems (less Ag/watt)', 'Solar PV', '★★★☆☆\n(3)', '20-40%\nvs pure c-Si', '2028-2032\nLimited share', 'MODERATE\nStill uses some silver'],
    ['CdTe thin film\n(First Solar - no silver)', 'Solar PV', '★★★★★\n(5)', '100%', 'NOW\n~5% global share', 'LOW\nTe supply capped'],
]

col_widths = [0.12, 0.1, 0.08, 0.08, 0.1, 0.08]
table = ax.table(cellText=tech_data, colWidths=col_widths, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.5)

# Style header
for j in range(6):
    cell = table[(0, j)]
    cell.set_facecolor('#264653')
    cell.set_text_props(color='white', fontweight='bold', fontsize=8.5)

# Color rows by sector
for i in range(1, len(tech_data)):
    sector = tech_data[i][1]
    if sector == 'Solar PV':
        bg = '#fce4ec' if i > 0 else 'white'
    elif sector == 'Data Centers\n& Electronics' or sector == 'Data Centers\n& Electronics':
        bg = '#e0f2f1'
    elif sector == 'Semiconductors':
        bg = '#fff3e0'
    else:
        bg = '#f3e5f5'
    
    if i % 2 == 0:
        bg = bg  # keep it
    
    for j in range(6):
        table[(i, j)].set_facecolor(bg)

# Add annotation below table
ax.text(0.5, -0.12,
    'Key Insight: The most impactful silver-substitution technologies are ALREADY in production in solar PV (copper paste, back-contact modules).\n'
    'Data center substitution (graphene/CNT TIMs) is 3-7 years away from scale and only addresses ~15-20% of DC silver use.\n'
    'Even with ALL substitutions maxed, silver faces a structural supply deficit through at least 2030.',
    transform=ax.transAxes, fontsize=9, ha='center', va='top',
    bbox=dict(boxstyle='round', facecolor='#fff3cd', edgecolor='#ffc107', alpha=0.9))

plt.title('Silver Substitution Technology Landscape (2026)', fontsize=13, fontweight='bold', pad=15)
plt.savefig(f'{OUT}/11_substitution_technologies.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 11 done")

# ============================================================
# CHART 12: The Bottleneck Map — Where, When, and How It Hits
# ============================================================
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_facecolor('#f8f9fa')

# Build a Gantt-style bottleneck timeline
bottlenecks = [
    # (y_start, duration, label, category, color)
    (2024.0, 2.5, 'London Free Float\nDepletion (136 Moz)', 'supply', '#e63946'),
    (2025.5, 3.0, 'Solar Silver Thrifting\nAccelerates (45%↓)', 'demand', '#457b9d'),
    (2026.0, 1.5, 'Silver-Copper Paste\nGoes Mainstream', 'substitution', '#2a9d8f'),
    (2026.5, 2.0, 'Aiko Silver-Free\nModule Scales Up', 'substitution', '#2a9d8f'),
    (2026.0, 5.0, 'Investment Demand\nSurge (India/Retail)', 'demand', '#e9c46a'),
    (2027.0, 3.0, 'Data Center Silver\nDemand Doubles (30 Moz)', 'demand', '#264653'),
    (2028.0, 4.0, 'Above-Ground Stocks\nApproach Zero', 'supply', '#c1121f'),
    (2028.5, 2.0, 'Hyperscaler Stargate\nProject Live (~50 DCs)', 'demand', '#264653'),
    (2029.0, 3.0, 'Graphene TIMs\nEnter Production', 'substitution', '#2a9d8f'),
    (2029.5, 2.0, 'Solar + DC Silver\nDemand Converge', 'inflection', '#6a4c93'),
    (2030.0, 2.0, 'Mine Supply Crisis:\nNo New Tier-1 Mines', 'supply', '#c1121f'),
]

categories = ['supply', 'demand', 'substitution', 'inflection']
cat_labels = ['Supply Constraint', 'Demand Driver', 'Substitution Effect', 'Inflection Point']
cat_colors = ['#c1121f', '#264653', '#2a9d8f', '#6a4c93']
cat_y = [1, 2, 3, 4]

for i, (name, label) in enumerate(zip(categories, cat_labels)):
    ax.barh(-i, 8, left=2024, height=0.8, color='#e8e8e8', alpha=0.3, zorder=0)
    ax.text(2023.8, -i, label, ha='right', va='center', fontsize=9, fontweight='bold', color=cat_colors[i])

for start, duration, label, category, color in bottlenecks:
    y_pos = -categories.index(category)
    ax.barh(y_pos, duration, left=start, height=0.6, color=color, alpha=0.8, edgecolor='white', linewidth=0.5, zorder=2)
    ax.text(start + duration/2, y_pos, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color='white', zorder=3)

# Critical path annotation
ax.axvline(x=2028.5, color='#e63946', linewidth=2, linestyle='--', alpha=0.6, zorder=1)
ax.text(2028.5, 1.5, 'CRITICAL\nWINDOW', ha='center', fontsize=10, fontweight='bold',
        color='#e63946', rotation=90, zorder=4)

# Bottleneck summary box
ax.text(0.98, 0.02,
    'BOTTLENECK SEQUENCE:\n'
    '① 2026: Free float depleted → price spikes on any demand shock\n'
    '② 2027: DC demand doubling + solar thrifting matures → net demand floor hardens\n'
    '③ 2028-2029: Above-ground stocks near zero → price discovery on scarcity\n'
    '④ 2030: Mine supply fails to grow → structural irreconcilable deficit\n'
    '→ Silver enters permanent deficit pricing regime',
    transform=ax.transAxes, fontsize=8.5, verticalalignment='bottom',
    horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='#fce4ec', edgecolor='#e63946', alpha=0.95))

ax.set_xlim(2024, 2032)
ax.set_ylim(-4.5, 0.5)
ax.set_xlabel('Year', fontsize=11)
ax.set_title('Silver Bottleneck Map: Where, When & How Supply Constraints Hit (2024-2031)', fontsize=13, fontweight='bold')
ax.set_yticks([])
ax.grid(axis='x', alpha=0.3)

fig.tight_layout()
plt.savefig(f'{OUT}/12_bottleneck_map.png', dpi=150)
plt.close()
print("Chart 12 done")

# ============================================================
# CHART 13: Bottleneck Expression — Which Companies/Commodities Benefit
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# Left: Winning assets in a silver bottleneck scenario
winners = {
    'Physical Silver\n(PSLV, SLV)': 10,
    'Silver Miners\n(PAAS, HL, EXK, HYMC)': 9,
    'Silver Streams/ Royalties\n(WPM, FNV Ag book)': 8,
    'Copper Miners\n(FCX, SCCO, HBM)': 7,
    'Gold (safe haven\nin supply crisis)': 6,
    'Uranium (DC power\n+ energy security)': 5,
    'Industrial Gases\n(Linde, Air Liquide)': 4,
    'Silver Recycling\n(SIMS, Li-Cycle)': 3,
}

ax1.set_facecolor('#f8f9fa')
names = list(winners.keys())
scores = list(winners.values())
colors = plt.cm.RdYlGn(np.array(scores) / 12)

bars = ax1.barh(names, scores, color=colors, alpha=0.85, height=0.6)
for bar, val in zip(bars, scores):
    ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val}/10', va='center', fontsize=9, fontweight='bold')

ax1.set_xlim(0, 12)
ax1.set_xlabel('Exposure Score (higher = benefits more from silver bottleneck)', fontsize=9)
ax1.set_title('Assets That Benefit From\na Silver Supply Bottleneck', fontsize=11, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Right: Venn-like visualization of where the bottleneck expresses
categories_v = ['Physical\nDelivery\nCrisis', 'Price\nDiscovery\n($150-200+/oz)', 'Mining\nMargins\nExplode',
                'Substitution\nAccelerates', 'Industrial\nDemand\nDestruction']
importance = [9, 8, 7, 5, 6]

ax2.set_facecolor('#f8f9fa')
bars2 = ax2.barh(categories_v, importance, color=['#c1121f', '#e63946', '#f4a261', '#2a9d8f', '#264653'], alpha=0.8, height=0.5)
for bar, val in zip(bars2, importance):
    ax2.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val}/10', va='center', fontsize=9, fontweight='bold')

ax2.set_xlim(0, 11)
ax2.set_xlabel('Intensity of Expression', fontsize=9)
ax2.set_title('Where the Bottleneck\nExpresses Itself', fontsize=11, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

fig.suptitle('How a Silver Bottleneck Regime Transforms the Investment Landscape', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
plt.savefig(f'{OUT}/13_bottleneck_expression.png', dpi=150)
plt.close()
print("Chart 13 done")

print("\n=== All 5 new charts generated successfully ===")