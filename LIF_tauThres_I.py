# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Global style
# -----------------------
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 40, 
    "axes.labelsize": 34,
    "lines.linewidth": 3.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 3.5,      # Ejes más gruesos
})

blue_grad = ["#2d6cdf", "#7fb6ff", "#9ecbff"]
purple_grad = ["#6f2dbd", "#b892ff", "#d4b3ff"]

dt = 0.02
T  = 120.0
t = np.arange(0.0, T, dt)
E_L, V_0, R, t0 = -70.0, -80.0, 10.0, 20.0

def make_rect_pulse(t, t0, width_ms, amp):
    I = np.zeros_like(t)
    I[(t >= t0) & (t < t0 + width_ms)] = amp
    return I

def simulate_lif(t, I, tau_m, v_threshold):
    V = np.full_like(t, E_L) 
    for k in range(1, len(t)):
        dv = (-(V[k-1] - E_L) + R * I[k-1]) * (dt / tau_m)
        V[k] = V[k-1] + dv
        if V[k] >= v_threshold:
            V[k-1] = 20 
            V[k] = V_0  
    return V

I_fixed = make_rect_pulse(t, t0, width_ms=75, amp=2.2)
taus, thresholds = [10, 25, 50], [-55, -50, -45]
tau_ref, vth_ref = 25.0, -50.0

right_pulses_cfg = [{"w": 15, "a": 5.0}, {"w": 40, "a": 3.0}, {"w": 70, "a": 2.2}]
I_right_list = [make_rect_pulse(t, t0, p["w"], p["a"]) for p in right_pulses_cfg]

def apply_custom_legend(ax):
    leg = ax.legend(
        frameon=True, 
        loc="upper right", 
        handlelength=0,      # Ya lo tenías
        handleheight=0,      # <--- AÑADE ESTO para quitar el espacio vertical del punto
        handletextpad=0,
        fancybox=True, 
        facecolor='#f0f0f0', 
        edgecolor='#ffffff', 
        fontsize=35
    )
    for handle in leg.legend_handles:
        handle.set_visible(False)
        
    for text in leg.get_texts():
        label = text.get_text()
        for line in ax.get_lines():
            if line.get_label() == label:
                text.set_color(line.get_color())
                text.set_weight("bold")

# --- PLOT ---
fig = plt.figure(figsize=(14, 14))
gs = fig.add_gridspec(3, 2, height_ratios=[0.75, 2, 2])

# --- IONOTROPIC (AHORA A LA IZQUIERDA) ---
ax_i_right = fig.add_subplot(gs[0, 0]) # Cambiado a columna 0
for I, col in zip(I_right_list, purple_grad):
    ax_i_right.plot(t, I, color=col)
ax_i_right.set_title("Ionotropic", fontweight="bold", color="#b892ff", pad=50)
ax_i_right.set_ylabel("Input (pA)")

ax_v_right = fig.add_subplot(gs[1:, 0]) # Cambiado a columna 0 (ocupa filas 1 y 2)
ax_v_right.axhline(vth_ref, color='gray', ls='--', lw=2.0, alpha=0.7) # Threshold line
for i, (I, col) in enumerate(zip(I_right_list, purple_grad), 1):
    ax_v_right.plot(t, simulate_lif(t, I, tau_ref, vth_ref), color=col, label=rf"$i_{i}$")
ax_v_right.set_ylabel("Voltage (mV)")
ax_v_right.set_xlabel("time (ms)")
apply_custom_legend(ax_v_right)

# --- METABOTROPIC (AHORA A LA DERECHA) ---
ax_i_left = fig.add_subplot(gs[0, 1], sharex=ax_i_right) # Cambiado a columna 1
ax_i_left.plot(t, I_fixed, color='slategray', lw=3)
ax_i_left.set_title("Metabotropic", fontweight="bold", color="#7fb6ff", pad=50)
ax_i_left.set_ylabel("Input (pA)")

# Tau
ax_tau = fig.add_subplot(gs[1, 1], sharex=ax_i_right) # Cambiado a columna 1
ax_tau.axhline(vth_ref, color='gray', ls='--', lw=3.0, alpha=0.7) # Threshold line
for i, (tau, col) in enumerate(zip(taus, blue_grad), 1):
    ax_tau.plot(t, simulate_lif(t, I_fixed, tau, vth_ref), color=col, label=rf"$\tau_{i}$")
ax_tau.set_ylabel("Voltage (mV)")
apply_custom_legend(ax_tau)

# Vth
ax_vth = fig.add_subplot(gs[2, 1], sharex=ax_i_right) # Cambiado a columna 1
for i, (vth, col) in enumerate(zip(thresholds, blue_grad), 1):
    ax_vth.axhline(vth, color=col, ls='--', lw=3.0, alpha=0.75) # Threshold lines per level
    ax_vth.plot(t, simulate_lif(t, I_fixed, tau_ref, vth), color=col, label=rf"$V_{{th{i}}}$")
ax_vth.set_ylabel("Voltage (mV)")
ax_vth.set_xlabel("time (ms)")
apply_custom_legend(ax_vth)

for ax in fig.axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['left'].set_linewidth(3.5)
    ax.spines['bottom'].set_linewidth(3.5)

fig.tight_layout(pad=4.0)
# plt.savefig("LIF_tauThresh_I2.png", dpi=600, bbox_inches='tight')
# plt.savefig("LIF_tauThresh_I2.svg", format="svg", bbox_inches="tight", dpi=600)


plt.show()