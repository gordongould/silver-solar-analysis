#!/usr/bin/env python3
"""Generate ALL charts with Tufte styling, numbering, and defense/space demand included."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.patches import FancyBboxPatch
import os

OUT = '/Users/tumples/silver-solar-analysis/charts'
os.makedirs(OUT, exist_ok=True)

# Tufte-style plot configuration
TUFTE_COLORS = {
    'blue': '#2166ac',
    'red': '#b2182b', 
    'green': '#4daf4a',
    'orange': '#ef8a62',
    'purple': '#762a83',
    'teal': '#1b9e77',
    'grey': '#bababa',
    'gold': '#d4a017',
}
FONT = {'family': 'sans-serif', 'size': 9}
plt.rc('font', **FONT)
plt.rc('axes', facecolor='white', edgecolor='#cccccc', linewidth=0.5, titlepad=10)
plt.rc('grid', color='#e0e0e0', alpha=0.5)
plt.rc('figure', facecolor='white', edgecolor='white')

def tufte_style(ax, x_grid=False, y_grid=True):
    """Apply Tufte-inspired clean styling."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(axis='both', colors='#666666', size=3)
    if y_grid:
        ax.yaxis.grid(True, alpha=0.3, color='#e0e0e0')
    if x_grid:
        ax.xaxis.grid(True, alpha=0.3, color='#e0e0e0')
    ax.set_axisbelow(True)

def save_chart(fig, name, dpi=150):
    path = f'{OUT}/{name}'
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ {name}")

# ============================================================
# CHART 1: Solar Silver Demand vs Installed Capacity (Decoupling)
# ============================================================
years = np.arange(2020, 2031)
installed_gw = np.array([150, 185, 240, 400, 593, 630, 680, 720, 760, 800, 830])
mg_per_w = np.array([18.0, 16.5, 15.0, 13.5, 12.2, 9.2, 6.7, 5.8, 5.0, 4.2, 3.5])
silver_moz = np.array([80, 95, 115, 175, 232, 187, 151, 140, 130, 118, 105])

fig, ax1 = plt.subplots(figsize=(9, 5))
tufte_style(ax1)
ax1.set_facecolor('white')

ax1.fill_between(years, silver_moz, alpha=0.15, color=TUFTE_COLORS['blue'])
ax1.plot(years, silver_moz, 'o-', color=TUFTE_COLORS['blue'], linewidth=2, markersize=4, zorder=3)
ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('Silver Demand (Moz)', color=TUFTE_COLORS['blue'], fontsize=10)
ax1.tick_params(axis='y', labelcolor=TUFTE_COLORS['blue'])
ax1.set_ylim(0, 300)

ax2 = ax1.twinx()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_color('#cccccc')
ax2.plot(years, installed_gw, 's-', color=TUFTE_COLORS['green'], linewidth=2, markersize=3, zorder=3)
ax2.set_ylabel('Installed Capacity (GW/yr)', color=TUFTE_COLORS['green'], fontsize=10)
ax2.tick_params(axis='y', labelcolor=TUFTE_COLORS['green'])
ax2.set_ylim(0, 1000)

# Decoupling arrow & annotation
ax1.annotate('Decoupling:\n+40% GW capacity\n−55% silver demand', xy=(2027, 140),
            xytext=(2027, 240), fontsize=8, ha='center',
            arrowprops=dict(arrowstyle='->', color=TUFTE_COLORS['blue'], lw=1),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc'))

fig.text(0.02, 0.97, 'Chart 1', fontsize=9, color='#999999', fontweight='bold')
ax1.set_title('Solar Silver Demand vs. Installed PV Capacity', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '01_solar_decoupling.png')

# ============================================================
# CHART 2: Silver Intensity Per Watt (Thrifting Trajectory)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 4.5))
tufte_style(ax)

ax.fill_between(years, mg_per_w, alpha=0.12, color=TUFTE_COLORS['orange'])
ax.plot(years, mg_per_w, 'o-', color=TUFTE_COLORS['orange'], linewidth=2, markersize=4, zorder=3)

# Annotate key milestones
milestones = {
    2020: ('18.0 mg/W\nPERC dominant', TUFTE_COLORS['grey']),
    2024: ('12.2 mg/W\nTOPCon/HJT\nenter mainsteam', TUFTE_COLORS['blue']),
    2026: ('6.7 mg/W\nCu paste\n45% drop in 2yr', TUFTE_COLORS['red']),
    2030: ('3.5 mg/W\nINES target', TUFTE_COLORS['green']),
}
for yr, (label, clr) in milestones.items():
    idx = np.where(years == yr)[0][0]
    ax.annotate(label, (yr, mg_per_w[idx]), xytext=(yr, mg_per_w[idx] + 3),
               ha='center', fontsize=7, color=clr, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=clr, lw=0.8))

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('mg Silver per Watt', fontsize=10)
ax.set_ylim(0, 22)
fig.text(0.02, 0.97, 'Chart 2', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver Intensity in Solar: The Thrifting Trajectory', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '02_silver_intensity.png')

# ============================================================
# CHART 3: Silver Demand by Sector (Stacked — includes Defense & Space)
# ============================================================
years_s = np.arange(2024, 2032)
solar_s = np.array([232, 187, 151, 140, 130, 118, 105, 95])
dc_s = np.array([15, 22, 30, 40, 52, 65, 80, 95])
defense_space_s = np.array([20, 25, 30, 35, 40, 45, 50, 55])
evs_s = np.array([72, 80, 88, 96, 105, 114, 124, 135])
other_s = np.array([300, 295, 290, 285, 280, 275, 270, 265])

fig, ax = plt.subplots(figsize=(9, 5))
tufte_style(ax)

components = [solar_s, dc_s, defense_space_s, evs_s, other_s]
labels = ['Solar PV', 'Data Centers & AI', 'Defense & Space ★ NEW', 'EVs & Automotive', 'Other Industrial']
colors = ['#f4a261', '#264653', '#d55e00', '#e76f51', '#a8dadc']

ax.stackplot(years_s, *components, labels=labels, colors=colors, alpha=0.85)

# Annotate defense/space segment
ax.annotate('Defense & Space\ngrowth: +175%\n(20→55 Moz)', xy=(2029, 110),
           ha='center', fontsize=7.5, fontweight='bold', color='#d55e00',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor='#d55e00', alpha=0.85))

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Million Ounces', fontsize=10)
ax.set_ylim(0, 750)
ax.legend(loc='upper right', fontsize=7.5, framealpha=0.9)
fig.text(0.02, 0.97, 'Chart 3', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Industrial Silver Demand by Sector (incl. Defense & Space)', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '03_demand_by_sector.png')

# ============================================================
# CHART 4: Grand Overlay — Demand, Supply & Deficit
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
tufte_style(ax)

total_demand = solar_s + dc_s + defense_space_s + evs_s + other_s
total_supply = np.array([1030, 1035, 1040, 1040, 1045, 1045, 1050, 1050])
deficit = total_demand - total_supply

ax.stackplot(years_s, solar_s, dc_s, defense_space_s, evs_s, other_s,
             labels=['Solar PV', 'Data Centers & AI', 'Defense & Space', 'EVs & Automotive', 'Other Industrial'],
             colors=['#f4a261', '#264653', '#d55e00', '#e76f51', '#a8dadc'],
             alpha=0.75)

ax.plot(years_s, total_supply, '-', color=TUFTE_COLORS['green'], linewidth=2.5, zorder=4,
        label='Total Supply (mine + recycling)')
ax.fill_between(years_s, total_supply, total_demand, where=(total_demand > total_supply),
                interpolate=True, alpha=0.2, color=TUFTE_COLORS['red'], label='Deficit Gap')

for i, (y, d) in enumerate(zip(years_s, deficit)):
    ax.annotate(f'{d:.0f}', (y, total_supply[i] + 18), ha='center', fontsize=8,
               color=TUFTE_COLORS['red'], fontweight='bold')
    ax.plot(y, total_supply[i], 'v', color=TUFTE_COLORS['red'], markersize=6, zorder=5)

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Million Ounces', fontsize=10)
ax.set_ylim(800, 1250)
ax.legend(loc='lower left', fontsize=7, ncol=2, framealpha=0.9)
fig.text(0.02, 0.97, 'Chart 4', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Total Silver: Demand, Supply & Structural Deficit', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '04_grand_overlay.png')

# ============================================================
# CHART 5: Cumulative Stock Depletion
# ============================================================
years_d = np.arange(2021, 2032)
annual_deficit = np.array([50, 100, 201, 195, 40, 46, 65, 75, 70, 60, 45])
cumulative = np.cumsum(annual_deficit)
london_float = np.array([750, 650, 500, 350, 220, 136, 110, 85, 60, 40, 25])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1, 1.3]})

# Left: annual deficits
tufte_style(ax1)
colors_deficit = ['#457b9d' if d < 50 else '#e63946' if d < 100 else '#c1121f' for d in annual_deficit]
ax1.bar(years_d, annual_deficit, color=colors_deficit, alpha=0.8, width=0.6)
ax1.set_xlabel('Year', fontsize=9)
ax1.set_ylabel('Deficit (Moz)', fontsize=9)
fig.text(0.02, 0.93, 'Chart 5', fontsize=9, color='#999999', fontweight='bold')
ax1.set_title('Annual Deficit', fontsize=11, fontweight='bold')

# Right: cumulative + London float
tufte_style(ax2)
ax2.fill_between(years_d, cumulative, alpha=0.12, color=TUFTE_COLORS['red'])
ax2.plot(years_d, cumulative, 'o-', color=TUFTE_COLORS['red'], linewidth=2, markersize=3, label='Cumulative Drawdown')
ax2.plot(years_d, london_float, 's-', color='#264653', linewidth=2, markersize=3, label='London Free Float (est.)')
ax2.axhline(y=150, color=TUFTE_COLORS['red'], linestyle='--', linewidth=0.8, alpha=0.5)
ax2.text(2025, 155, 'Fragile threshold: 150 Moz', fontsize=6.5, color=TUFTE_COLORS['red'], fontweight='bold')
ax2.set_xlabel('Year', fontsize=9)
ax2.set_ylabel('Moz', fontsize=9)
ax2.set_title('Cumulative Depletion & Vault Stocks', fontsize=11, fontweight='bold')
ax2.legend(fontsize=7, framealpha=0.9)
ax2.set_ylim(0, 1000)

fig.suptitle('Silver Stock Depletion: 762 Moz Drawn Since 2021', fontsize=12, fontweight='bold')
save_chart(fig, '05_stock_depletion.png')

# ============================================================
# CHART 6: Growth Rates Comparison
# ============================================================
cats = ['Solar PV\nSilver Demand\n2024→2030', 'Data Centers\n& AI Silver\n2024→2030', 'Defense &\nSpace Silver\n2024→2030', 'EVs &\nAutomotive\n2024→2030', 'Solar Installed\nCapacity (GW)\n2024→2030']
growth = [-54.7, 433.3, 150.0, 72.2, 40.0]

fig, ax = plt.subplots(figsize=(9, 4))
tufte_style(ax)
colors_g = ['#e63946', '#264653', '#d55e00', '#e76f51', '#2a9d8f']
bars = ax.bar(cats, growth, color=colors_g, alpha=0.8, width=0.55)
for bar, val in zip(bars, growth):
    lbl = f'{val:+.1f}%'
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (6 if val > 0 else -18),
            lbl, ha='center', fontsize=8, fontweight='bold')
ax.axhline(y=0, color='black', linewidth=0.6)
ax.set_ylabel('Growth Rate 2024→2030 (%)', fontsize=10)
fig.text(0.02, 0.95, 'Chart 6', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Which Sectors Grow Faster? (2024→2030)', fontsize=12, fontweight='bold')
ax.set_ylim(-70, 500)
save_chart(fig, '06_growth_rates.png')

# ============================================================
# CHART 7: Crossover — Solar vs DC Silver Demand
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
tufte_style(ax)

ax.plot(years_s, solar_s, 'o-', color=TUFTE_COLORS['blue'], linewidth=2, markersize=4, label='Solar PV Silver Demand (Moz)')
ax.plot(years_s, dc_s, 's-', color=TUFTE_COLORS['red'], linewidth=2, markersize=4, label='Data Center Silver Demand (Moz)')

ax.fill_between(years_s, solar_s, dc_s, where=(solar_s >= dc_s), alpha=0.06, color=TUFTE_COLORS['blue'])
ax.fill_between(years_s, solar_s, dc_s, where=(solar_s < dc_s), alpha=0.1, color=TUFTE_COLORS['red'])

crossover_idx = np.argmax(solar_s <= dc_s)
ax.annotate(f'Crossover\n~{int(years_s[crossover_idx])}', 
           xy=(years_s[crossover_idx], dc_s[crossover_idx]),
           xytext=(years_s[crossover_idx]-2, dc_s[crossover_idx]-30),
           fontsize=10, fontweight='bold',
           arrowprops=dict(arrowstyle='->', lw=1.5),
           bbox=dict(boxstyle='round', facecolor='#fff3cd', edgecolor='none', alpha=0.8))

# Add defense as annotation
ax.text(0.98, 0.05, 'Defense & Space adds\n~20-55 Moz on top\n(shifts total demand\nupward by 3-5%)',
       transform=ax.transAxes, fontsize=7, ha='right', va='bottom',
       bbox=dict(boxstyle='round', facecolor='#fce4ec', edgecolor='#d55e00', alpha=0.8))

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Million Ounces', fontsize=10)
ax.set_ylim(0, 260)
ax.legend(fontsize=9, framealpha=0.9)
fig.text(0.02, 0.97, 'Chart 7', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('The Crossover: Solar vs. Data Center Silver Demand', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '07_crossover.png')

# ============================================================
# CHART 8: Substitution Technology Landscape
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axis('off')

tech_data = [
    ['Technology', 'Sector', 'Readiness\n(1-5)', 'Ag\nReduction', 'Timeline', 'Impact'],
    ['Copper paste (rear-side)', 'Solar', '5/5', '30-50%', 'NOW', 'CRITICAL'],
    ['Aiko back-contact module', 'Solar', '3/5', '80-100%', '2026-28', 'HIGH'],
    ['Cu electroplating (HJT)', 'Solar', '3/5', '90-100%', '2027-30', 'HIGH'],
    ['Ag-coated Cu pastes', 'Solar', '4/5', '40-60%', '2026-27', 'CRITICAL'],
    ['Graphene/CNT TIMs', 'DC/AI', '2/5', 'Partial', '2028-33', 'LOW-MOD'],
    ['Cu wire bonding (chips)', 'Semi', '5/5', 'Moderate', 'NOW', 'LOW'],
    ['Al metallization (power)', 'Semi', '4/5', 'Moderate', 'NOW', 'LOW-MOD'],
    ['Perovskite-Si tandems', 'Solar', '3/5', '20-40%', '2028-32', 'MODERATE'],
    ['CdTe thin film (First Solar)', 'Solar', '5/5', '100%', 'NOW', 'LOW (Te cap)'],
]

table = ax.table(cellText=tech_data, colWidths=[0.13, 0.07, 0.08, 0.08, 0.08, 0.08],
                loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 1.6)

for j in range(6):
    table[(0, j)].set_facecolor('#264653')
    table[(0, j)].set_text_props(color='white', fontweight='bold', fontsize=8)

for i in range(1, len(tech_data)):
    sector = tech_data[i][1]
    if sector == 'Solar': bg = '#fce4ec' if i % 2 == 0 else '#fff5f5'
    elif sector == 'DC/AI': bg = '#e0f2f1' if i % 2 == 0 else '#f0faf9'
    elif sector == 'Semi': bg = '#fff3e0' if i % 2 == 0 else '#fffaf0'
    else: bg = '#f3e5f5' if i % 2 == 0 else '#faf0ff'
    for j in range(6):
        table[(i, j)].set_facecolor(bg)

ax.text(0.5, -0.08,
    'Key: Solar has credible substitutes in production NOW. Data centers lack substitutes for critical high-frequency silver applications (TIM, connectors).\nEven maxing all substitution, structural deficit persists through 2030.',
    transform=ax.transAxes, fontsize=7.5, ha='center', va='top', color='#666666')

fig.text(0.02, 0.97, 'Chart 8', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver Substitution Technology Landscape (2026)', fontsize=12, fontweight='bold', pad=10)
save_chart(fig, '08_substitution_tech.png')

# ============================================================
# CHART 9: Bottleneck Map (Gantt timeline)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_facecolor('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.spines['left'].set_color('#cccccc')

bottlenecks = [
    (2024.0, 2.5, 'London Free Float Depleted', 'supply', TUFTE_COLORS['red']),
    (2025.5, 3.0, 'Solar Thrifting Accelerates (45%↓)', 'demand', '#457b9d'),
    (2026.5, 2.0, 'Aiko Silver-Free Module Scales', 'substitution', TUFTE_COLORS['green']),
    (2026.0, 5.0, 'Investment Demand Surge (India/Retail)', 'demand', TUFTE_COLORS['gold']),
    (2026.5, 3.5, 'EU ReArm: Defense Silver +175%', 'demand', '#d55e00'),
    (2027.0, 3.0, 'DC Silver Demand Doubles (30 Moz)', 'demand', '#264653'),
    (2028.0, 4.0, 'Above-Ground Stocks → Zero', 'supply', TUFTE_COLORS['red']),
    (2028.5, 2.0, 'Stargate / Orbital DCs Go Live', 'demand', '#264653'),
    (2029.0, 3.0, 'Graphene/CNT TIMs Enter Production', 'substitution', TUFTE_COLORS['green']),
    (2029.5, 2.0, 'Solar + DC Demand Converge', 'inflection', TUFTE_COLORS['purple']),
    (2030.0, 2.0, 'No New Tier-1 Mines → Supply Crisis', 'supply', TUFTE_COLORS['red']),
]

cat_pos = {'supply': 0, 'demand': 1, 'substitution': 2, 'inflection': 3}
cat_lbl = ['Supply Constraint', 'Demand Driver', 'Substitution Effect', 'Inflection']
cat_clr = [TUFTE_COLORS['red'], '#264653', TUFTE_COLORS['green'], TUFTE_COLORS['purple']]

for i, (cat, lbl, clr) in enumerate(zip(cat_pos.keys(), cat_lbl, cat_clr)):
    ax.barh(-i, 8, left=2024, height=0.7, color='#f0f0f0', alpha=0.4, zorder=0)
    ax.text(2023.7, -i, lbl, ha='right', va='center', fontsize=8.5, fontweight='bold', color=clr)

for start, dur, label, cat, color in bottlenecks:
    y = -cat_pos[cat]
    ax.barh(y, dur, left=start, height=0.55, color=color, alpha=0.8, edgecolor='white', linewidth=0.5, zorder=2)
    ax.text(start + dur/2, y, label, ha='center', va='center', fontsize=7, fontweight='bold', color='white', zorder=3)

ax.axvline(x=2028.5, color=TUFTE_COLORS['red'], linewidth=2, linestyle='--', alpha=0.5, zorder=1)
ax.text(2028.5, 0.5, 'CRITICAL WINDOW', ha='center', fontsize=8, fontweight='bold',
        color=TUFTE_COLORS['red'])

ax.set_xlim(2024, 2032)
ax.set_ylim(-4.5, 0.5)
ax.set_xlabel('Year', fontsize=10)
ax.set_yticks([])
ax.grid(axis='x', alpha=0.3)
fig.text(0.02, 0.97, 'Chart 9', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver Bottleneck Map: Sequence of Crunch Points', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '09_bottleneck_map.png')

# ============================================================
# CHART 10: Defense & Space Silver Demand Breakdown
# ============================================================
years_ds = np.arange(2024, 2032)
mil_connectors = np.array([2.2, 2.3, 2.4, 2.5, 2.5, 2.6, 2.6, 2.7])  # $B
mil_radar_ew = np.array([8, 9, 11, 13, 15, 17, 19, 21])  # estimated Moz silver in radar/EW
mil_drones = np.array([2, 3, 4, 5, 6, 7, 8, 9])  # Moz
mil_comms = np.array([4, 5, 6, 7, 8, 9, 10, 11])  # Moz
mil_other = np.array([4, 5, 5, 6, 6, 7, 7, 8])  # Moz
space_total = np.array([4, 5, 6, 8, 10, 12, 14, 17])  # Moz (Starlink, satellites, space stations)

total_ds = mil_radar_ew + mil_drones + mil_comms + mil_other + space_total

fig, ax = plt.subplots(figsize=(9, 5))
tufte_style(ax)

ax.stackplot(years_ds, mil_radar_ew, mil_drones, mil_comms, mil_other, space_total,
             labels=['Radar & Electronic Warfare', 'Military Drones/UAVs', 'C4ISR & Communications',
                     'Other Defense (weapons, vehicles)', 'Space (Starlink, sats, orbit)'],
             colors=['#264653', '#d55e00', '#f4a261', '#457b9d', '#762a83'],
             alpha=0.8)

ax.plot(years_ds, total_ds, '-', color='#1a1a1a', linewidth=1.5, zorder=4, label=f'Total: +{((total_ds[-1]/total_ds[0]-1)*100):.0f}%')
for y, v in zip(years_ds, total_ds):
    ax.text(y, v + 1, f'{v}', ha='center', fontsize=7, fontweight='bold', color='#333')

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Million Ounces', fontsize=10)
ax.set_ylim(0, 80)
ax.legend(loc='upper left', fontsize=7, framealpha=0.9)
fig.text(0.02, 0.97, 'Chart 10', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Defense & Space Silver Demand Breakdown', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '10_defense_space.png')

# ============================================================
# CHART 11: How the Bottleneck Expresses (Asset Winners)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Left: Winners
ax1.set_facecolor('white')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color('#cccccc')
ax1.spines['left'].set_color('#cccccc')
ax1.tick_params(colors='#666666', size=3)
ax1.xaxis.grid(True, alpha=0.3, color='#e0e0e0')
ax1.set_axisbelow(True)

winners = {
    'Physical Silver (PSLV, SLV)': 10,
    'Silver Miners (PAAS, HL, EXK)': 9,
    'Silver Streams (WPM, FNV)': 8,
    'Copper Miners (FCX, SCCO)': 7,
    'Gold (safe haven)': 6,
    'Uranium (DC power)': 5,
    'Industrial Gases (LIN)': 4,
    'Space/Defense ETFs': 4,
}
names = list(winners.keys())
scores = list(winners.values())
ax1.barh(names, scores, color=plt.cm.RdYlGn(np.array(scores)/12), alpha=0.8, height=0.55)
for bar, val in zip(ax1.patches, scores):
    ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f'{val}/10', va='center', fontsize=7.5)
ax1.set_xlim(0, 12)
ax1.set_xlabel('Exposure Score', fontsize=8)
ax1.set_title('Who Benefits in a Silver Bottleneck?', fontsize=11, fontweight='bold', pad=8)

# Right: Expression
ax2.set_facecolor('white')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#cccccc')
ax2.spines['left'].set_color('#cccccc')
ax2.tick_params(colors='#666666', size=3)
ax2.xaxis.grid(True, alpha=0.3, color='#e0e0e0')
ax2.set_axisbelow(True)

expr = ['Physical\nDelivery Crisis\n(most acute)', 'Price Discovery\n($150-200+/oz)', 'Mining Margins\nExplode (5-10×)', 'Substitution\nAccelerates', 'Industrial\nDemand Destruction']
expr_scores = [9, 8, 7, 6, 5]
ax2.barh(expr, expr_scores, color=[TUFTE_COLORS['red'], '#e63946', '#f4a261', TUFTE_COLORS['green'], '#264653'], alpha=0.8, height=0.5)
for bar, val in zip(ax2.patches, expr_scores):
    ax2.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f'{val}/10', va='center', fontsize=7.5)
ax2.set_xlim(0, 11)
ax2.set_xlabel('Intensity', fontsize=8)
ax2.set_title('Where the Bottleneck Expresses', fontsize=11, fontweight='bold', pad=8)

fig.text(0.02, 0.94, 'Chart 11', fontsize=9, color='#999999', fontweight='bold')
fig.suptitle('How a Silver Bottleneck Regime Transforms the Landscape', fontsize=12, fontweight='bold', y=1.02)
save_chart(fig, '11_bottleneck_expression.png')

# ============================================================
# CHART 12: Demand Sources Comparison — All Sectors
# ============================================================
labels_d = ['Solar PV\n232→105 Moz', 'Data Centers\n15→80 Moz', 'Defense &\nSpace\n20→55 Moz', 'EVs &\nAuto\n72→135 Moz', 'Other\nIndustrial\n300→265 Moz']
sizes_2024 = [232, 15, 20, 72, 300]
sizes_2030 = [105, 80, 50, 124, 265]

x = np.arange(len(labels_d))
w = 0.35

fig, ax = plt.subplots(figsize=(9, 4.5))
tufte_style(ax)
bars1 = ax.bar(x - w/2, sizes_2024, w, label='2024', color='#457b9d', alpha=0.8)
bars2 = ax.bar(x + w/2, sizes_2030, w, label='2030 (projected)', color='#e63946', alpha=0.8)
for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 4, f'{int(h)}', ha='center', fontsize=8, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels_d, fontsize=8)
ax.set_ylabel('Million Ounces (Moz)', fontsize=10)
ax.legend(fontsize=9, framealpha=0.9)
fig.text(0.02, 0.97, 'Chart 12', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver Demand by Source: 2024 vs. 2030', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '12_demand_2024_vs_2030.png')

# ============================================================
# CHART 13: Summary Dashboard (Key Metrics Table)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axis('off')

table_data = [
    ['Metric', '2024', '2025', '2026E', '2030E', 'Trend'],
    ['Solar PV Demand (Moz)', '232', '187', '151', '105', '↓ −55%'],
    ['Data Center Demand (Moz)', '15', '22', '30', '80', '↑ +433%'],
    ['Defense & Space (Moz) ★', '20', '25', '30', '50', '↑ +150%'],
    ['EV Demand (Moz)', '72', '80', '88', '124', '↑ +72%'],
    ['Total Demand (Moz)', '639', '609', '589', '629', '→ Flat'],
    ['Total Supply (Moz)', '1,030', '1,035', '1,040', '1,050', '→ +2%'],
    ['Annual Deficit (Moz)', '−195', '−40', '−46', '−45', 'Persistent'],
    ['Cumulative Drawdown (Moz)', '−546', '−586', '−632', '−892', '↓ Accelerating'],
    ['London Free Float (Moz, est.)', '350', '220', '110', '40', '↓ Critically low'],
    ['Silver Intensity (mg/W)', '12.2', '9.2', '6.7', '3.5', '↓ −71%'],
    ['Thin Film Solar Share (%)', '5%', '7%', '10%', '20%', '↑ Growing'],
    ['Gold Price ($/oz)', '~2,700', '~3,650', '~4,250', '~5,500', '↑ Central bank bid'],
    ['Copper Price ($/lb)', '~4.50', '~4.90', '~6.33', '~6.80', '↑ Structural deficit'],
]

table = ax.table(cellText=table_data, colWidths=[0.15, 0.08, 0.08, 0.08, 0.08, 0.07],
                loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 1.5)

for j in range(6):
    table[(0, j)].set_facecolor('#264653')
    table[(0, j)].set_text_props(color='white', fontweight='bold')

for i in range(1, len(table_data)):
    if i == 3:  # Defense & Space row
        bg = '#fce4ec' if i % 2 == 0 else '#fff5f5'
    elif i in [6, 7, 8, 9]:  # Deficit/supply rows
        bg = '#e8f4f8' if i % 2 == 0 else '#f0faff'
    else:
        bg = '#f8f9fa' if i % 2 == 0 else 'white'
    for j in range(6):
        table[(i, j)].set_facecolor(bg)

fig.text(0.02, 0.97, 'Chart 13', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver & Commodity Dashboard — Key Metrics (2024-2030)', fontsize=12, fontweight='bold', pad=15)
save_chart(fig, '13_summary_dashboard.png')

# ============================================================
# CHART 14: All Demand Sources — Line Chart (the "big picture")
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
tufte_style(ax)

ax.plot(years_s, solar_s, '-', color='#f4a261', linewidth=2, label='Solar PV', marker='o', markersize=3)
ax.plot(years_s, dc_s, '-', color='#264653', linewidth=2, label='Data Centers & AI', marker='s', markersize=3)
ax.plot(years_s, defense_space_s, '-', color='#d55e00', linewidth=2, label='Defense & Space ★', marker='^', markersize=3)
ax.plot(years_s, evs_s, '-', color='#e76f51', linewidth=2, label='EVs & Automotive', marker='D', markersize=3)
ax.plot(years_s, total_supply[:8], '--', color=TUFTE_COLORS['green'], linewidth=1.5, label='Supply (flat)')

# Net demand trend
net_demand = total_demand[:8]
ax.fill_between(years_s, total_supply[:8], net_demand, where=(net_demand > total_supply[:8]),
                interpolate=True, alpha=0.08, color=TUFTE_COLORS['red'])

ax.text(2024.5, 1080, 'Total Supply\n~1,040 Moz', fontsize=8, color=TUFTE_COLORS['green'], fontweight='bold')
ax.text(2029.5, 1190, 'Deficit', fontsize=8, color=TUFTE_COLORS['red'], fontweight='bold')

ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Million Ounces', fontsize=10)
ax.set_ylim(0, 1250)
ax.legend(loc='center left', fontsize=7.5, framealpha=0.9, ncol=2)
fig.text(0.02, 0.97, 'Chart 14', fontsize=9, color='#999999', fontweight='bold')
ax.set_title('Silver Demand Growth Vectors with Supply Constraint', fontsize=12, fontweight='bold', pad=8)
save_chart(fig, '14_all_demand_vectors.png')

print("=== All 14 charts generated ===")
print(f"   Output: {OUT}/")
