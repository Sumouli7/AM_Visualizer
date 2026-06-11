#!/usr/bin/env python3
"""
Analog Circuit Toolbox
----------------------
A comprehensive educational and engineering GUI application for analog electronic circuits,
specifically matching the MAKAUT EC402/EC492 syllabus.

Features:
1. Diode & BJT Amplifiers (Rectifiers, Clippers/Clampers, CE Amplifiers)
2. Power Amplifiers & Feedback Topologies
3. Sinusoidal Oscillators & MOSFET Parameter Extractor
4. Op-Amp Configurations & Active Filter Bode Design Wizard

Designed with a high-fidelity dark UI, try-except error catching, and dynamic matplotlib plots.
"""

import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define Color Palette for Dark UI
BG_DARK = "#121214"      # Main application background
CARD_BG = "#1e1e24"      # Cards and frames
BORDER_COLOR = "#2e2e38" # Borders
ACCENT_CYAN = "#00adb5"  # Primary highlights
ACCENT_BLUE = "#0081c9"  # Secondary accents
TEXT_WHITE = "#ffffff"   # Primary text
TEXT_MUTED = "#a0a0b2"   # Secondary text
GRID_COLOR = "#2e2e38"   # Plot grid color

class AnalogCircuitToolboxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analog Circuit Toolbox")
        self.geometry("1100x820")
        self.configure(bg=BG_DARK)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Core element styles
        style.configure(".", background=BG_DARK, foreground=TEXT_WHITE, fieldbackground=CARD_BG, font=("Segoe UI", 10))
        style.configure("TFrame", background=BG_DARK)
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_WHITE, font=("Segoe UI", 10))
        
        # Header text
        style.configure("Title.TLabel", background=BG_DARK, foreground=ACCENT_CYAN, font=("Segoe UI", 16, "bold"))
        style.configure("Section.TLabel", background=BG_DARK, foreground=ACCENT_BLUE, font=("Segoe UI", 12, "bold"))
        
        # Card style
        style.configure("Card.TFrame", background=CARD_BG, relief="solid", borderwidth=1)
        style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT_WHITE, font=("Segoe UI", 10))
        style.configure("CardHeader.TLabel", background=CARD_BG, foreground=ACCENT_CYAN, font=("Segoe UI", 12, "bold"))
        style.configure("CardMuted.TLabel", background=CARD_BG, foreground=TEXT_MUTED, font=("Segoe UI", 9, "italic"))
        style.configure("CardBold.TLabel", background=CARD_BG, foreground=TEXT_WHITE, font=("Segoe UI", 10, "bold"))
        style.configure("CardAccent.TLabel", background=CARD_BG, foreground=ACCENT_BLUE, font=("Segoe UI", 10, "bold"))

        # Notebook tabs
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=CARD_BG, foreground=TEXT_MUTED, font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT_CYAN), ("active", "#155a60")],
                  foreground=[("selected", BG_DARK), ("active", TEXT_WHITE)])
        
        # Buttons
        style.configure("TButton", background=ACCENT_CYAN, foreground=BG_DARK, font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#008c9e")])
        
        style.configure("Accent.TButton", background=ACCENT_BLUE, foreground=TEXT_WHITE, font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#006aa6")])
        
        # Inputs (Entry and Combobox)
        style.configure("TEntry", fieldbackground="#2c2c36", foreground=TEXT_WHITE, insertcolor=TEXT_WHITE, bordercolor=BORDER_COLOR)
        style.configure("TCombobox", fieldbackground="#2c2c36", foreground=TEXT_WHITE, selectbackground=ACCENT_CYAN, selectforeground=BG_DARK, bordercolor=BORDER_COLOR, arrowcolor=TEXT_WHITE)
        style.map("TCombobox", fieldbackground=[("readonly", "#2c2c36")], foreground=[("readonly", TEXT_WHITE)])

    def create_widgets(self):
        # Top banner
        banner = ttk.Frame(self, padding=10)
        banner.pack(fill="x")
        title_lbl = ttk.Label(banner, text="ANALOG CIRCUIT TOOLBOX", style="Title.TLabel")
        title_lbl.pack(side="left")
        
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add the 4 notebook tabs
        self.create_tab1_diode_bjt()
        self.create_tab2_power_feedback()
        self.create_tab3_oscillators_mosfet()
        self.create_tab4_opamp_filters()

    # ==========================================
    # TAB 1: DIODE & BJT AMPLIFIERS
    # ==========================================
    def create_tab1_diode_bjt(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Diode & BJT Amplifiers")
        
        # Scrollable layout container or two-column grid
        tab1.columnconfigure(0, weight=4, minsize=420)
        tab1.columnconfigure(1, weight=6, minsize=550)
        tab1.rowconfigure(0, weight=1)
        
        left_col = ttk.Frame(tab1, padding=5)
        left_col.grid(row=0, column=0, sticky="nsew")
        right_col = ttk.Frame(tab1, padding=5)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        # --- LEFT COLUMN CARDS ---
        # Card 1.1: Rectifier Calculator
        rect_card = ttk.Frame(left_col, style="Card.TFrame", padding=10)
        rect_card.pack(fill="x", pady=5)
        
        lbl = ttk.Label(rect_card, text="Rectifier Performance Calculator", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        # Inputs frame
        rect_inputs = ttk.Frame(rect_card, style="Card.TFrame")
        rect_inputs.pack(fill="x")
        
        # Peak input voltage (Vm)
        ttk.Label(rect_inputs, text="Peak Secondary Voltage Vm (V):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
        self.rect_vm_entry = ttk.Entry(rect_inputs, width=10)
        self.rect_vm_entry.insert(0, "15.0")
        self.rect_vm_entry.grid(row=0, column=1, sticky="e", pady=2, padx=5)
        
        # Diode drop (Vd)
        ttk.Label(rect_inputs, text="Diode Forward Voltage Drop V_D (V):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.rect_vd_entry = ttk.Entry(rect_inputs, width=10)
        self.rect_vd_entry.insert(0, "0.7")
        self.rect_vd_entry.grid(row=1, column=1, sticky="e", pady=2, padx=5)
        
        # Load resistance (Rl)
        ttk.Label(rect_inputs, text="Load Resistance R_L (Ω):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=2)
        self.rect_rl_entry = ttk.Entry(rect_inputs, width=10)
        self.rect_rl_entry.insert(0, "1000")
        self.rect_rl_entry.grid(row=2, column=1, sticky="e", pady=2, padx=5)
        
        # Dynamic diode & secondary resistance (rd + rs)
        ttk.Label(rect_inputs, text="Total Internal Resistance r_s + r_d (Ω):", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=2)
        self.rect_rd_entry = ttk.Entry(rect_inputs, width=10)
        self.rect_rd_entry.insert(0, "10")
        self.rect_rd_entry.grid(row=3, column=1, sticky="e", pady=2, padx=5)
        
        # Calc Button
        rect_btn = ttk.Button(rect_card, text="Calculate Rectifier Performance", command=self.calculate_rectifiers)
        rect_btn.pack(pady=8, fill="x")
        
        # Outputs frame
        self.rect_outputs_frame = ttk.Frame(rect_card, style="Card.TFrame")
        self.rect_outputs_frame.pack(fill="x", pady=2)
        
        self.rect_fwr_lbl = ttk.Label(self.rect_outputs_frame, text="Full-Wave Center-Tapped: N/A", style="CardAccent.TLabel")
        self.rect_fwr_lbl.pack(anchor="w", pady=2)
        self.rect_bridge_lbl = ttk.Label(self.rect_outputs_frame, text="Bridge Rectifier: N/A", style="CardAccent.TLabel")
        self.rect_bridge_lbl.pack(anchor="w", pady=2)

        # Card 1.2: BJT CE Amplifier Solver
        bjt_card = ttk.Frame(left_col, style="Card.TFrame", padding=10)
        bjt_card.pack(fill="both", expand=True, pady=5)
        
        lbl = ttk.Label(bjt_card, text="BJT Common-Emitter Amplifier Solver", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        bjt_inputs = ttk.Frame(bjt_card, style="Card.TFrame")
        bjt_inputs.pack(fill="x")
        
        # Inputs: Vcc, R1, R2, Rc, Re, Beta, Rl, Bypassed
        ttk.Label(bjt_inputs, text="Supply Voltage Vcc (V):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
        self.bjt_vcc = ttk.Entry(bjt_inputs, width=8)
        self.bjt_vcc.insert(0, "12")
        self.bjt_vcc.grid(row=0, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Base Resistor R1 (kΩ):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.bjt_r1 = ttk.Entry(bjt_inputs, width=8)
        self.bjt_r1.insert(0, "10")
        self.bjt_r1.grid(row=1, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Base Resistor R2 (kΩ):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=2)
        self.bjt_r2 = ttk.Entry(bjt_inputs, width=8)
        self.bjt_r2.insert(0, "2.2")
        self.bjt_r2.grid(row=2, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Collector Resistor Rc (kΩ):", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=2)
        self.bjt_rc = ttk.Entry(bjt_inputs, width=8)
        self.bjt_rc.insert(0, "1.0")
        self.bjt_rc.grid(row=3, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Emitter Resistor Re (kΩ):", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=2)
        self.bjt_re = ttk.Entry(bjt_inputs, width=8)
        self.bjt_re.insert(0, "0.47")
        self.bjt_re.grid(row=4, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Transistor Beta (β):", style="Card.TLabel").grid(row=5, column=0, sticky="w", pady=2)
        self.bjt_beta = ttk.Entry(bjt_inputs, width=8)
        self.bjt_beta.insert(0, "100")
        self.bjt_beta.grid(row=5, column=1, sticky="e", pady=2, padx=5)
        
        ttk.Label(bjt_inputs, text="Load Resistor R_L (kΩ):", style="Card.TLabel").grid(row=6, column=0, sticky="w", pady=2)
        self.bjt_rl = ttk.Entry(bjt_inputs, width=8)
        self.bjt_rl.insert(0, "10")
        self.bjt_rl.grid(row=6, column=1, sticky="e", pady=2, padx=5)
        
        self.bjt_bypass_val = tk.BooleanVar(value=True)
        self.bjt_bypass = ttk.Checkbutton(bjt_inputs, text="Emitter Resistor Bypassed (C_E)", variable=self.bjt_bypass_val)
        self.bjt_bypass.grid(row=7, columnspan=2, sticky="w", pady=4)
        
        # Calc Button
        bjt_btn = ttk.Button(bjt_card, text="Solve CE BJT Amplifier", command=self.calculate_bjt_ce)
        bjt_btn.pack(pady=8, fill="x")
        
        # Outputs Scrollable text or label grid
        self.bjt_output = ttk.Label(bjt_card, text="Solve to view bias point & gain parameters.", style="CardMuted.TLabel", justify="left")
        self.bjt_output.pack(anchor="w", fill="both", expand=True)
        
        # --- RIGHT COLUMN CARDS ---
        # Card 1.3: Clipper/Clamper Visualizer
        vis_card = ttk.Frame(right_col, style="Card.TFrame", padding=10)
        vis_card.pack(fill="both", expand=True, pady=5)
        
        lbl = ttk.Label(vis_card, text="Clipper & Clamper Waveform Visualizer", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        vis_inputs = ttk.Frame(vis_card, style="Card.TFrame")
        vis_inputs.pack(fill="x")
        
        # Waveform parameters
        ttk.Label(vis_inputs, text="Peak Input Vp (V):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
        self.cc_vp = ttk.Entry(vis_inputs, width=8)
        self.cc_vp.insert(0, "10")
        self.cc_vp.grid(row=0, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(vis_inputs, text="Reference Vref (V):", style="Card.TLabel").grid(row=0, column=2, sticky="w", pady=2)
        self.cc_vref = ttk.Entry(vis_inputs, width=8)
        self.cc_vref.insert(0, "3.0")
        self.cc_vref.grid(row=0, column=3, sticky="w", pady=2, padx=5)
        
        ttk.Label(vis_inputs, text="Diode Drop V_D (V):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.cc_vd = ttk.Entry(vis_inputs, width=8)
        self.cc_vd.insert(0, "0.7")
        self.cc_vd.grid(row=1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(vis_inputs, text="Select Mode:", style="Card.TLabel").grid(row=1, column=2, sticky="w", pady=2)
        self.cc_mode = ttk.Combobox(vis_inputs, values=["Positive Clipper", "Negative Clipper", "Positive Clamper", "Negative Clamper"], width=16, state="readonly")
        self.cc_mode.set("Positive Clipper")
        self.cc_mode.grid(row=1, column=3, sticky="w", pady=2, padx=5)
        
        cc_plot_btn = ttk.Button(vis_inputs, text="Plot Waveform", command=self.plot_clipper_clamper)
        cc_plot_btn.grid(row=0, column=4, rowspan=2, padx=10, sticky="nsew")
        
        # Plot Canvas
        self.cc_fig = Figure(figsize=(5, 3.8), dpi=100, facecolor=CARD_BG)
        self.cc_ax = self.cc_fig.add_subplot(111)
        self.cc_ax.set_facecolor(BG_DARK)
        self.cc_ax.tick_params(colors=TEXT_WHITE)
        self.cc_ax.spines['bottom'].set_color(BORDER_COLOR)
        self.cc_ax.spines['top'].set_color(BORDER_COLOR)
        self.cc_ax.spines['left'].set_color(BORDER_COLOR)
        self.cc_ax.spines['right'].set_color(BORDER_COLOR)
        self.cc_ax.set_title("Input vs Output Waveform", color=ACCENT_CYAN, fontname="Segoe UI", fontsize=10)
        self.cc_ax.grid(True, color=GRID_COLOR, linestyle="--")
        
        self.cc_canvas = FigureCanvasTkAgg(self.cc_fig, master=vis_card)
        self.cc_canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        # Initial Plot
        self.plot_clipper_clamper()

    # ==========================================
    # TAB 2: POWER AMPLIFIERS & FEEDBACK
    # ==========================================
    def create_tab2_power_feedback(self):
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Power Amplifiers & Feedback")
        
        tab2.columnconfigure(0, weight=1, minsize=480)
        tab2.columnconfigure(1, weight=1, minsize=480)
        tab2.rowconfigure(0, weight=1)
        
        left_col = ttk.Frame(tab2, padding=10)
        left_col.grid(row=0, column=0, sticky="nsew")
        right_col = ttk.Frame(tab2, padding=10)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        # --- LEFT COLUMN: Class B Push-Pull Calculator ---
        classb_card = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        classb_card.pack(fill="both", expand=True)
        
        lbl = ttk.Label(classb_card, text="Class B Push-Pull Power Amplifier Solver", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 15))
        
        cb_inputs = ttk.Frame(classb_card, style="Card.TFrame")
        cb_inputs.pack(fill="x", pady=5)
        
        ttk.Label(cb_inputs, text="DC Supply Voltage Vcc (V):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_vcc = ttk.Entry(cb_inputs, width=12)
        self.cb_vcc.insert(0, "15.0")
        self.cb_vcc.grid(row=0, column=1, sticky="e", pady=5, padx=10)
        
        ttk.Label(cb_inputs, text="Load Resistance R_L (Ω):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_rl = ttk.Entry(cb_inputs, width=12)
        self.cb_rl.insert(0, "8")
        self.cb_rl.grid(row=1, column=1, sticky="e", pady=5, padx=10)
        
        cb_btn = ttk.Button(classb_card, text="Calculate Performance", command=self.calculate_class_b)
        cb_btn.pack(pady=15, fill="x")
        
        self.cb_outputs = ttk.Label(classb_card, text="Enter values to compute amplifier outputs.", style="CardMuted.TLabel", justify="left")
        self.cb_outputs.pack(anchor="w", fill="both", expand=True)
        
        # --- RIGHT COLUMN: Feedback Topology Modifier ---
        fb_card = ttk.Frame(right_col, style="Card.TFrame", padding=15)
        fb_card.pack(fill="both", expand=True)
        
        lbl = ttk.Label(fb_card, text="Feedback Topology Analysis Tool", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 15))
        
        fb_inputs = ttk.Frame(fb_card, style="Card.TFrame")
        fb_inputs.pack(fill="x", pady=5)
        
        ttk.Label(fb_inputs, text="Open-Loop Gain (A):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.fb_a = ttk.Entry(fb_inputs, width=12)
        self.fb_a.insert(0, "1000")
        self.fb_a.grid(row=0, column=1, sticky="e", pady=5, padx=10)
        
        ttk.Label(fb_inputs, text="Input Resistance R_i (kΩ):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.fb_ri = ttk.Entry(fb_inputs, width=12)
        self.fb_ri.insert(0, "10.0")
        self.fb_ri.grid(row=1, column=1, sticky="e", pady=5, padx=10)
        
        ttk.Label(fb_inputs, text="Output Resistance R_o (kΩ):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.fb_ro = ttk.Entry(fb_inputs, width=12)
        self.fb_ro.insert(0, "1.0")
        self.fb_ro.grid(row=2, column=1, sticky="e", pady=5, padx=10)
        
        ttk.Label(fb_inputs, text="Feedback Factor (β):", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.fb_beta = ttk.Entry(fb_inputs, width=12)
        self.fb_beta.insert(0, "0.01")
        self.fb_beta.grid(row=3, column=1, sticky="e", pady=5, padx=10)
        
        ttk.Label(fb_inputs, text="Feedback Topology:", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        self.fb_topology = ttk.Combobox(fb_inputs, values=["Voltage-Series", "Current-Series", "Voltage-Shunt", "Current-Shunt"], width=14, state="readonly")
        self.fb_topology.set("Voltage-Series")
        self.fb_topology.grid(row=4, column=1, sticky="e", pady=5, padx=10)
        
        fb_btn = ttk.Button(fb_card, text="Apply Feedback", command=self.calculate_feedback)
        fb_btn.pack(pady=15, fill="x")
        
        self.fb_outputs = ttk.Label(fb_card, text="Solve to calculate closed-loop parameters.", style="CardMuted.TLabel", justify="left")
        self.fb_outputs.pack(anchor="w", fill="both", expand=True)

    # ==========================================
    # TAB 3: OSCILLATORS & MOSFET CHARACTERISTICS
    # ==========================================
    def create_tab3_oscillators_mosfet(self):
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Oscillators & MOSFET")
        
        tab3.columnconfigure(0, weight=1, minsize=480)
        tab3.columnconfigure(1, weight=1, minsize=480)
        tab3.rowconfigure(0, weight=1)
        
        left_col = ttk.Frame(tab3, padding=10)
        left_col.grid(row=0, column=0, sticky="nsew")
        right_col = ttk.Frame(tab3, padding=10)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        # --- LEFT COLUMN: Sinusoidal Oscillators ---
        osc_card = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        osc_card.pack(fill="both", expand=True)
        
        lbl = ttk.Label(osc_card, text="Sinusoidal Oscillator Solver", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 10))
        
        osc_selector = ttk.Frame(osc_card, style="Card.TFrame")
        osc_selector.pack(fill="x", pady=2)
        ttk.Label(osc_selector, text="Select Oscillator Type:", style="Card.TLabel").pack(side="left", padx=5)
        self.osc_type = ttk.Combobox(osc_selector, values=["RC Phase Shift", "Wien Bridge", "Hartley", "Colpitts"], width=18, state="readonly")
        self.osc_type.set("RC Phase Shift")
        self.osc_type.pack(side="left", padx=5)
        self.osc_type.bind("<<ComboboxSelected>>", self.on_oscillator_change)
        
        # Dynamic inputs container
        self.osc_inputs_frame = ttk.Frame(osc_card, style="Card.TFrame", padding=(0, 10))
        self.osc_inputs_frame.pack(fill="x")
        
        # Initialize the inputs
        self.on_oscillator_change(None)
        
        # Calc Button (packed inside on_oscillator_change layout or separately)
        # We will keep calculation buttons and output displays consistent
        osc_calc_btn = ttk.Button(osc_card, text="Solve Oscillator Frequency", command=self.calculate_oscillator)
        osc_calc_btn.pack(pady=10, fill="x")
        
        self.osc_output_lbl = ttk.Label(osc_card, text="Click solve to compute Barkhausen criteria details.", style="CardMuted.TLabel", justify="left")
        self.osc_output_lbl.pack(anchor="w", fill="both", expand=True, pady=5)
        
        # --- RIGHT COLUMN: MOSFET Dynamic Parameter Extractor ---
        mos_card = ttk.Frame(right_col, style="Card.TFrame", padding=15)
        mos_card.pack(fill="both", expand=True)
        
        lbl = ttk.Label(mos_card, text="MOSFET Dynamic Parameter Extractor", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 15))
        
        mos_inputs = ttk.Frame(mos_card, style="Card.TFrame")
        mos_inputs.pack(fill="x", pady=5)
        
        ttk.Label(mos_inputs, text="Gate-Source Voltage Change ΔV_GS (V):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=8)
        self.mos_dvgs = ttk.Entry(mos_inputs, width=12)
        self.mos_dvgs.insert(0, "0.5")
        self.mos_dvgs.grid(row=0, column=1, sticky="e", pady=8, padx=10)
        
        ttk.Label(mos_inputs, text="Drain-Source Voltage Change ΔV_DS (V):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=8)
        self.mos_dvds = ttk.Entry(mos_inputs, width=12)
        self.mos_dvds.insert(0, "2.0")
        self.mos_dvds.grid(row=1, column=1, sticky="e", pady=8, padx=10)
        
        ttk.Label(mos_inputs, text="Drain Current Change ΔI_D (mA):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=8)
        self.mos_did = ttk.Entry(mos_inputs, width=12)
        self.mos_did.insert(0, "1.5")
        self.mos_did.grid(row=2, column=1, sticky="e", pady=8, padx=10)
        
        mos_btn = ttk.Button(mos_card, text="Extract MOSFET Parameters", command=self.calculate_mosfet)
        mos_btn.pack(pady=15, fill="x")
        
        self.mos_outputs = ttk.Label(mos_card, text="Provide dynamic variations under saturation to calculate values.", style="CardMuted.TLabel", justify="left")
        self.mos_outputs.pack(anchor="w", fill="both", expand=True)

    def on_oscillator_change(self, event):
        # Clear previous inputs
        for child in self.osc_inputs_frame.winfo_children():
            child.destroy()
            
        osc = self.osc_type.get()
        
        # Build widgets dynamically based on selection
        if osc == "RC Phase Shift":
            ttk.Label(self.osc_inputs_frame, text="Feedback Resistor R (kΩ):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=4)
            self.osc_r1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_r1.insert(0, "10.0")
            self.osc_r1.grid(row=0, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Feedback Capacitor C (nF):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4)
            self.osc_c1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_c1.insert(0, "10.0")
            self.osc_c1.grid(row=1, column=1, sticky="e", pady=4, padx=10)
            
        elif osc == "Wien Bridge":
            ttk.Label(self.osc_inputs_frame, text="Bridge Resistor R (kΩ):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=4)
            self.osc_r1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_r1.insert(0, "10.0")
            self.osc_r1.grid(row=0, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Bridge Capacitor C (nF):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4)
            self.osc_c1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_c1.insert(0, "10.0")
            self.osc_c1.grid(row=1, column=1, sticky="e", pady=4, padx=10)
            
        elif osc == "Hartley":
            ttk.Label(self.osc_inputs_frame, text="Inductor L1 (mH):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=4)
            self.osc_l1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_l1.insert(0, "10.0")
            self.osc_l1.grid(row=0, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Inductor L2 (mH):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4)
            self.osc_l2 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_l2.insert(0, "20.0")
            self.osc_l2.grid(row=1, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Mutual Inductance M (mH):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=4)
            self.osc_m = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_m.insert(0, "0.0")
            self.osc_m.grid(row=2, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Tank Capacitor C (nF):", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=4)
            self.osc_c1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_c1.insert(0, "0.1")
            self.osc_c1.grid(row=3, column=1, sticky="e", pady=4, padx=10)
            
        elif osc == "Colpitts":
            ttk.Label(self.osc_inputs_frame, text="Inductor L (mH):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=4)
            self.osc_l1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_l1.insert(0, "10.0")
            self.osc_l1.grid(row=0, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Capacitor C1 (nF):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4)
            self.osc_c1 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_c1.insert(0, "100.0")
            self.osc_c1.grid(row=1, column=1, sticky="e", pady=4, padx=10)
            
            ttk.Label(self.osc_inputs_frame, text="Capacitor C2 (nF):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=4)
            self.osc_c2 = ttk.Entry(self.osc_inputs_frame, width=10)
            self.osc_c2.insert(0, "100.0")
            self.osc_c2.grid(row=2, column=1, sticky="e", pady=4, padx=10)

    # ==========================================
    # TAB 4: OP-AMP APPLICATIONS & ACTIVE FILTERS
    # ==========================================
    def create_tab4_opamp_filters(self):
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="Op-Amp & Active Filters")
        
        tab4.columnconfigure(0, weight=4, minsize=420)
        tab4.columnconfigure(1, weight=6, minsize=550)
        tab4.rowconfigure(0, weight=1)
        
        left_col = ttk.Frame(tab4, padding=5)
        left_col.grid(row=0, column=0, sticky="nsew")
        right_col = ttk.Frame(tab4, padding=5)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        # --- LEFT COLUMN: Op-Amp Operations & Waveform Generator ---
        opamp_card = ttk.Frame(left_col, style="Card.TFrame", padding=10)
        opamp_card.pack(fill="both", expand=True, pady=5)
        
        lbl = ttk.Label(opamp_card, text="Op-Amp Math & Waveform visualizer", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        op_sel = ttk.Frame(opamp_card, style="Card.TFrame")
        op_sel.pack(fill="x", pady=2)
        ttk.Label(op_sel, text="Configuration:", style="Card.TLabel").pack(side="left", padx=5)
        self.op_config = ttk.Combobox(op_sel, values=["Inverting", "Non-Inverting", "Integrator", "Differentiator"], width=15, state="readonly")
        self.op_config.set("Inverting")
        self.op_config.pack(side="left", padx=5)
        self.op_config.bind("<<ComboboxSelected>>", self.on_opamp_config_change)
        
        self.op_inputs_frame = ttk.Frame(opamp_card, style="Card.TFrame", padding=(0, 5))
        self.op_inputs_frame.pack(fill="x")
        
        self.on_opamp_config_change(None)
        
        op_btn = ttk.Button(opamp_card, text="Plot Op-Amp Output Response", command=self.plot_opamp_response)
        op_btn.pack(pady=5, fill="x")
        
        self.op_math_lbl = ttk.Label(opamp_card, text="", style="CardAccent.TLabel", justify="left")
        self.op_math_lbl.pack(anchor="w", pady=2)
        
        # Op-amp Plot Canvas
        self.op_fig = Figure(figsize=(4, 2.5), dpi=90, facecolor=CARD_BG)
        self.op_ax = self.op_fig.add_subplot(111)
        self.op_ax.set_facecolor(BG_DARK)
        self.op_ax.tick_params(colors=TEXT_WHITE)
        self.op_ax.spines['bottom'].set_color(BORDER_COLOR)
        self.op_ax.spines['top'].set_color(BORDER_COLOR)
        self.op_ax.spines['left'].set_color(BORDER_COLOR)
        self.op_ax.spines['right'].set_color(BORDER_COLOR)
        self.op_ax.grid(True, color=GRID_COLOR, linestyle="--")
        
        self.op_canvas = FigureCanvasTkAgg(self.op_fig, master=opamp_card)
        self.op_canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)
        self.plot_opamp_response()

        # --- RIGHT COLUMN: Active Filter Design Wizard ---
        filter_card = ttk.Frame(right_col, style="Card.TFrame", padding=10)
        filter_card.pack(fill="both", expand=True, pady=5)
        
        lbl = ttk.Label(filter_card, text="1st-Order Active Filter Design Wizard", style="CardHeader.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        filt_inputs = ttk.Frame(filter_card, style="Card.TFrame")
        filt_inputs.pack(fill="x")
        
        ttk.Label(filt_inputs, text="Filter Type:", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
        self.filt_type = ttk.Combobox(filt_inputs, values=["1st-Order Low-Pass", "1st-Order High-Pass"], width=18, state="readonly")
        self.filt_type.set("1st-Order Low-Pass")
        self.filt_type.grid(row=0, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(filt_inputs, text="Cutoff Frequency fc (Hz):", style="Card.TLabel").grid(row=0, column=2, sticky="w", pady=2)
        self.filt_fc = ttk.Entry(filt_inputs, width=10)
        self.filt_fc.insert(0, "1000")
        self.filt_fc.grid(row=0, column=3, sticky="w", pady=2, padx=5)
        
        ttk.Label(filt_inputs, text="Capacitor C (nF):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.filt_c = ttk.Entry(filt_inputs, width=10)
        self.filt_c.insert(0, "10")
        self.filt_c.grid(row=1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(filt_inputs, text="Passband Gain A0 (V/V):", style="Card.TLabel").grid(row=1, column=2, sticky="w", pady=2)
        self.filt_a0 = ttk.Entry(filt_inputs, width=10)
        self.filt_a0.insert(0, "1.5")
        self.filt_a0.grid(row=1, column=3, sticky="w", pady=2, padx=5)
        
        filt_btn = ttk.Button(filt_inputs, text="Design & Plot Bode", command=self.plot_filter_bode)
        filt_btn.grid(row=0, column=4, rowspan=2, padx=10, sticky="nsew")
        
        self.filt_output_lbl = ttk.Label(filter_card, text="Design results will be shown here.", style="CardAccent.TLabel")
        self.filt_output_lbl.pack(anchor="w", pady=5)
        
        # Bode plot Canvas
        self.filt_fig = Figure(figsize=(5, 3.8), dpi=100, facecolor=CARD_BG)
        self.filt_ax = self.filt_fig.add_subplot(111)
        self.filt_ax.set_facecolor(BG_DARK)
        self.filt_ax.tick_params(colors=TEXT_WHITE)
        self.filt_ax.spines['bottom'].set_color(BORDER_COLOR)
        self.filt_ax.spines['top'].set_color(BORDER_COLOR)
        self.filt_ax.spines['left'].set_color(BORDER_COLOR)
        self.filt_ax.spines['right'].set_color(BORDER_COLOR)
        self.filt_ax.grid(True, which="both", color=GRID_COLOR, linestyle="--")
        
        self.filt_canvas = FigureCanvasTkAgg(self.filt_fig, master=filter_card)
        self.filt_canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)
        self.plot_filter_bode()

    def on_opamp_config_change(self, event):
        for child in self.op_inputs_frame.winfo_children():
            child.destroy()
            
        cfg = self.op_config.get()
        if cfg in ["Inverting", "Non-Inverting"]:
            ttk.Label(self.op_inputs_frame, text="Input Resistor R1 (kΩ):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
            self.op_r1 = ttk.Entry(self.op_inputs_frame, width=8)
            self.op_r1.insert(0, "10.0")
            self.op_r1.grid(row=0, column=1, sticky="w", pady=2, padx=5)
            
            ttk.Label(self.op_inputs_frame, text="Feedback Resistor Rf (kΩ):", style="Card.TLabel").grid(row=0, column=2, sticky="w", pady=2)
            self.op_rf = ttk.Entry(self.op_inputs_frame, width=8)
            self.op_rf.insert(0, "100.0")
            self.op_rf.grid(row=0, column=3, sticky="w", pady=2, padx=5)
            
        elif cfg in ["Integrator", "Differentiator"]:
            ttk.Label(self.op_inputs_frame, text="Resistance R (kΩ):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=2)
            self.op_r1 = ttk.Entry(self.op_inputs_frame, width=8)
            self.op_r1.insert(0, "10.0")
            self.op_r1.grid(row=0, column=1, sticky="w", pady=2, padx=5)
            
            ttk.Label(self.op_inputs_frame, text="Capacitance C (nF):", style="Card.TLabel").grid(row=0, column=2, sticky="w", pady=2)
            self.op_c = ttk.Entry(self.op_inputs_frame, width=8)
            self.op_c.insert(0, "100.0")
            self.op_c.grid(row=0, column=3, sticky="w", pady=2, padx=5)

        ttk.Label(self.op_inputs_frame, text="Input Voltage Vp (V):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.op_vp = ttk.Entry(self.op_inputs_frame, width=8)
        self.op_vp.insert(0, "1.0")
        self.op_vp.grid(row=1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(self.op_inputs_frame, text="Frequency f (Hz):", style="Card.TLabel").grid(row=1, column=2, sticky="w", pady=2)
        self.op_freq = ttk.Entry(self.op_inputs_frame, width=8)
        self.op_freq.insert(0, "100")
        self.op_freq.grid(row=1, column=3, sticky="w", pady=2, padx=5)

    # ==========================================
    # CORE CALCULATIONS & GRAPHICS GENERATION
    # ==========================================

    def calculate_rectifiers(self):
        try:
            Vm = float(self.rect_vm_entry.get())
            Vd = float(self.rect_vd_entry.get())
            Rl = float(self.rect_rl_entry.get())
            r_int = float(self.rect_rd_entry.get())
            
            if Vm <= 0 or Rl <= 0 or r_int < 0 or Vd < 0:
                raise ValueError("All inputs must be non-negative, and Vm & RL must be positive.")
            
            # --- Center-Tapped Full Wave Rectifier ---
            # Center-Tapped has a single diode conduction loop per cycle -> 1 Vd drop
            Vm_out_fwr = Vm - Vd
            if Vm_out_fwr < 0:
                Vm_out_fwr = 0
            
            Vdc_fwr = (2 * Vm_out_fwr) / math.pi
            Vrms_fwr = Vm_out_fwr / math.sqrt(2)
            
            if Vdc_fwr > 0:
                ripple_fwr = math.sqrt(max(0, (Vrms_fwr / Vdc_fwr)**2 - 1))
            else:
                ripple_fwr = 0.0
            
            # Efficiency includes winding and diode resistances
            # Center-tapped efficiency = (8 / pi^2) * (Rl / (Rl + r_int))
            eff_fwr = (800 / (math.pi**2)) * (Rl / (Rl + r_int))
            
            # --- Bridge Rectifier ---
            # Bridge has two diodes conducting in series -> 2 Vd drop
            Vm_out_bridge = Vm - 2 * Vd
            if Vm_out_bridge < 0:
                Vm_out_bridge = 0
                
            Vdc_bridge = (2 * Vm_out_bridge) / math.pi
            Vrms_bridge = Vm_out_bridge / math.sqrt(2)
            
            if Vdc_bridge > 0:
                ripple_bridge = math.sqrt(max(0, (Vrms_bridge / Vdc_bridge)**2 - 1))
            else:
                ripple_bridge = 0.0
                
            # Bridge efficiency = (8 / pi^2) * (Rl / (Rl + 2*rd + rs))
            # Assuming r_int is input as total internal loop resistance in conducting path
            eff_bridge = (800 / (math.pi**2)) * (Rl / (Rl + r_int))
            
            # Update labels
            self.rect_fwr_lbl.configure(text=f"Full-Wave CT: Vdc = {Vdc_fwr:.3f} V | Ripple Factor = {ripple_fwr:.3f} | Efficiency = {eff_fwr:.2f}%")
            self.rect_bridge_lbl.configure(text=f"Bridge Rectifier: Vdc = {Vdc_bridge:.3f} V | Ripple Factor = {ripple_bridge:.3f} | Efficiency = {eff_bridge:.2f}%")
            
        except Exception as e:
            messagebox.showerror("Rectifier Input Error", f"Invalid input parameters:\n{str(e)}")

    def plot_clipper_clamper(self):
        try:
            Vp = float(self.cc_vp.get())
            Vref = float(self.cc_vref.get())
            Vd = float(self.cc_vd.get())
            mode = self.cc_mode.get()
            
            if Vp <= 0 or Vd < 0:
                raise ValueError("Vp must be positive and Vd non-negative.")
            
            t = np.linspace(0, 0.04, 1000)  # Plot 2 cycles of 50Hz (T = 0.02s)
            f = 50.0
            vin = Vp * np.sin(2 * np.pi * f * t)
            
            # Clipper / Clamper logic
            if mode == "Positive Clipper":
                # Clips signals above Vref + Vd
                limit = Vref + Vd
                vout = np.minimum(vin, limit)
            elif mode == "Negative Clipper":
                # Clips signals below Vref - Vd
                limit = Vref - Vd
                vout = np.maximum(vin, limit)
            elif mode == "Positive Clamper":
                # Shifts negative peaks up to Vref (ideal) or Vref - Vd
                # Clamped minimum voltage is Vref - Vd, shift is Vp - Vd + Vref
                shift = Vp - Vd + Vref
                vout = vin + shift
            elif mode == "Negative Clamper":
                # Shifts positive peaks down to Vref (ideal) or Vref + Vd
                # Clamped maximum voltage is Vref + Vd, shift is -(Vp - Vd - Vref)
                shift = -(Vp - Vd - Vref)
                vout = vin + shift
            
            self.cc_ax.clear()
            self.cc_ax.plot(t * 1000, vin, label="Input (Vin)", color="#888888", linestyle="--", linewidth=1.5)
            self.cc_ax.plot(t * 1000, vout, label=f"Output ({mode})", color=ACCENT_CYAN, linewidth=2)
            
            # Plot reference voltage line if relevant for clippers
            if "Clipper" in mode:
                self.cc_ax.axhline(y=Vref, color=ACCENT_BLUE, linestyle=":", label="Vref")
                
            self.cc_ax.set_facecolor(BG_DARK)
            self.cc_ax.tick_params(colors=TEXT_WHITE)
            self.cc_ax.spines['bottom'].set_color(BORDER_COLOR)
            self.cc_ax.spines['top'].set_color(BORDER_COLOR)
            self.cc_ax.spines['left'].set_color(BORDER_COLOR)
            self.cc_ax.spines['right'].set_color(BORDER_COLOR)
            self.cc_ax.set_title(f"Waveform Analysis: {mode}", color=ACCENT_CYAN, fontname="Segoe UI", fontsize=10)
            self.cc_ax.set_xlabel("Time (ms)", color=TEXT_WHITE, fontname="Segoe UI", fontsize=9)
            self.cc_ax.set_ylabel("Voltage (V)", color=TEXT_WHITE, fontname="Segoe UI", fontsize=9)
            self.cc_ax.grid(True, color=GRID_COLOR, linestyle="--")
            self.cc_ax.legend(facecolor=CARD_BG, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=8)
            
            self.cc_canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Clipper/Clamper Input Error", f"Invalid input parameters:\n{str(e)}")

    def calculate_bjt_ce(self):
        try:
            Vcc = float(self.bjt_vcc.get())
            R1 = float(self.bjt_r1.get())
            R2 = float(self.bjt_r2.get())
            Rc = float(self.bjt_rc.get())
            Re = float(self.bjt_re.get())
            beta = float(self.bjt_beta.get())
            bypassed = self.bjt_bypass_val.get()
            
            rl_str = self.bjt_rl.get().strip()
            Rl = float(rl_str) if rl_str else None
            
            if Vcc <= 0 or R1 <= 0 or R2 <= 0 or Rc <= 0 or Re <= 0 or beta <= 0:
                raise ValueError("Resistances, Gain, and Power supply must be positive.")
            if Rl is not None and Rl <= 0:
                raise ValueError("Load Resistance must be positive.")
                
            Vbe = 0.7  # V
            Vt = 0.026  # V (Thermal Voltage at Room Temp)
            
            # Thevenin equivalents
            Rth = (R1 * R2) / (R1 + R2)
            Vth = Vcc * R2 / (R1 + R2)
            
            # DC bias calculation
            # Vth = Ib*Rth + Vbe + Ie*Re = Ib*Rth + Vbe + (beta + 1)*Ib*Re
            Ib = (Vth - Vbe) / (Rth + (beta + 1) * Re)
            
            if Ib < 0:
                self.bjt_output.configure(
                    text=f"ERROR: Transistor is cut-off!\n"
                         f"Vth ({Vth:.2f}V) is less than Vbe (0.7V).\n"
                         f"Increase R2 or decrease R1.",
                    foreground="#ff5555"
                )
                return
                
            Ic = beta * Ib
            Ie = (beta + 1) * Ib
            Vce = Vcc - Ic * Rc - Ie * Re
            
            status = "ACTIVE"
            if Vce <= 0.2:
                status = "SATURATED"
                # Limit currents to saturating level
                Ic = (Vcc - 0.2) / (Rc + Re)
                Ib = Ic / beta
                Ie = Ic + Ib
                Vce = 0.2
                
            # DC Bias Stability Factor S
            # S = (1 + beta) * [ 1 + Rth/Re ] / [ 1 + beta + Rth/Re ]
            S = (1 + beta) * (1 + Rth / Re) / (1 + beta + Rth / Re)
            
            # Dynamic dynamic resistance re & r_pi
            # gm = Ic / Vt. Since Ic is in mA, gm is in mS
            # r_pi = beta / gm (kΩ)
            # if transistor is saturated, gains will drop dramatically, but we solver for active region gain
            gm = Ic / Vt  # mS
            rpi = beta / gm  # kΩ
            
            # Effective AC Collector Load
            Rc_ac = (Rc * Rl) / (Rc + Rl) if Rl is not None else Rc
            
            # Gains and Impedances
            if bypassed:
                # Emitter is fully bypassed by Ce
                Rin = (Rth * rpi) / (Rth + rpi)
                Av = -gm * Rc_ac
                Rout = Rc
            else:
                # Emitter is unbypassed
                Rin_base = rpi + (1 + beta) * Re
                Rin = (Rth * Rin_base) / (Rth + Rin_base)
                # Av = -beta * Rc_ac / [ Rth + rpi + (1 + beta) * Re ]
                Av = -beta * Rc_ac / (rpi + (1 + beta) * Re)
                Rout = Rc
                
            Av_db = 20 * math.log10(abs(Av)) if abs(Av) > 0 else 0
            
            saturation_warning = "\nWARNING: Transistor in SATURATION (Vce <= 0.2V)" if status == "SATURATED" else ""
            
            self.bjt_output.configure(
                text=f"Operating Point (Q-Point):\n"
                     f"  - IB = {Ib*1000:.2f} μA, IC = {Ic:.2f} mA\n"
                     f"  - VCE = {Vce:.2f} V ({status}){saturation_warning}\n\n"
                     f"Bias Stability:\n"
                     f"  - Stability Factor S = {S:.2f} (lower is better)\n\n"
                     f"Small Signal AC Performance:\n"
                     f"  - Transconductance gm = {gm:.2f} mS\n"
                     f"  - Dynamic Resistance rπ = {rpi:.2f} kΩ\n"
                     f"  - Input Resistance Rin = {Rin:.2f} kΩ\n"
                     f"  - Output Resistance Rout = {Rout:.2f} kΩ\n"
                     f"  - Midband Voltage Gain Av = {Av:.2f} V/V ({Av_db:.2f} dB)",
                style="CardAccent.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("BJT CE Input Error", f"Invalid input parameters:\n{str(e)}")

    def calculate_class_b(self):
        try:
            Vcc = float(self.cb_vcc.get())
            Rl = float(self.cb_rl.get())
            
            if Vcc <= 0 or Rl <= 0:
                raise ValueError("Vcc and Rl must be greater than zero.")
                
            # Ideal calculations (max output amplitude Vm = Vcc)
            Po_max = (Vcc**2) / (2 * Rl)
            Pdc = (2 * Vcc**2) / (math.pi * Rl)
            efficiency = 100 * (math.pi / 4)
            
            # Power Dissipated
            Pd_total = Pdc - Po_max
            Pd_per_trans = Pd_total / 2
            
            # Worst-case collector dissipation (occurs when Vm = 2*Vcc/pi)
            Vout_worst = (2 * Vcc) / math.pi
            Pd_worst_per_trans = (Vcc**2) / ((math.pi**2) * Rl)
            
            self.cb_outputs.configure(
                text=f"Ideal Max Outputs (Peak Output Vm = Vcc):\n"
                     f"  - Max Output Power (Po,max) = {Po_max:.2f} W\n"
                     f"  - Supplied DC Power (Pdc) = {Pdc:.2f} W\n"
                     f"  - Peak Efficiency (η) = {efficiency:.2f}% (Theoretical limit 78.54%)\n"
                     f"  - Max Heat Dissipated (Total) = {Pd_total:.2f} W\n"
                     f"  - Max Heat Dissipated (Per Transistor) = {Pd_per_trans:.2f} W\n\n"
                     f"Worst-Case Thermal Point:\n"
                     f"  - Max possible dissipation/transistor occurs at Vm = {Vout_worst:.2f} V\n"
                     f"  - Peak Transistor Dissipation = {Pd_worst_per_trans:.2f} W",
                style="CardAccent.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("Class B Input Error", f"Invalid input parameters:\n{str(e)}")

    def calculate_feedback(self):
        try:
            A = float(self.fb_a.get())
            Ri = float(self.fb_ri.get())
            Ro = float(self.fb_ro.get())
            beta = float(self.fb_beta.get())
            topology = self.fb_topology.get()
            
            if A <= 0 or Ri <= 0 or Ro <= 0 or beta < 0:
                raise ValueError("Gain and resistances must be positive. Beta must be non-negative.")
            
            # Desensitization factor
            D = 1 + A * beta
            
            Af = A / D
            
            if topology == "Voltage-Series":
                # Input impedance increases, output impedance decreases
                Rif = Ri * D
                Rof = Ro / D
            elif topology == "Current-Series":
                # Input impedance increases, output impedance increases
                Rif = Ri * D
                Rof = Ro * D
            elif topology == "Voltage-Shunt":
                # Input impedance decreases, output impedance decreases
                Rif = Ri / D
                Rof = Ro / D
            elif topology == "Current-Shunt":
                # Input impedance decreases, output impedance increases
                Rif = Ri / D
                Rof = Ro * D
                
            self.fb_outputs.configure(
                text=f"Closed-Loop Parameters:\n"
                     f"  - Feedback Modifier (1 + Aβ) = {D:.2f}\n"
                     f"  - Gain with Feedback (Af) = {Af:.2f}\n"
                     f"  - Input Resistance (Rif) = {Rif:.3f} kΩ\n"
                     f"  - Output Resistance (Rof) = {Rof:.3f} kΩ\n\n"
                     f"Topology Analysis Summary:\n"
                     f"  - Type: {topology}\n"
                     f"  - Feedback Voltage/Current is sampled and fed back in series/shunt.\n"
                     f"  - Under {topology}, input impedance is {'increased' if 'Series' in topology else 'decreased'} "
                     f"and output impedance is {'decreased' if 'Voltage' in topology else 'increased'}.",
                style="CardAccent.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("Feedback Calculator Error", f"Invalid input parameters:\n{str(e)}")

    def calculate_oscillator(self):
        try:
            osc = self.osc_type.get()
            
            if osc == "RC Phase Shift":
                R = float(self.osc_r1.get()) * 1e3  # convert kΩ to Ω
                C = float(self.osc_c1.get()) * 1e-9 # convert nF to F
                if R <= 0 or C <= 0: raise ValueError("Values must be positive.")
                
                f = 1 / (2 * math.pi * R * C * math.sqrt(6))
                beta = 1 / 29.0
                req_gain = 29.0
                summary = "RC Phase Shift requirements:\n- 3 RC sections, each contributing 60° phase shift.\n- Barkhausen Loop Gain: |Aβ| = 1 with 360° (or 0°) loop phase shift."
                
            elif osc == "Wien Bridge":
                R = float(self.osc_r1.get()) * 1e3  # convert kΩ to Ω
                C = float(self.osc_c1.get()) * 1e-9 # convert nF to F
                if R <= 0 or C <= 0: raise ValueError("Values must be positive.")
                
                f = 1 / (2 * math.pi * R * C)
                beta = 1 / 3.0
                req_gain = 3.0
                summary = "Wien Bridge requirements:\n- Positive feedback network (lead-lag network) provides 0° shift at resonance.\n- Negative feedback controls amplifier gain to exactly 3."
                
            elif osc == "Hartley":
                L1 = float(self.osc_l1.get()) * 1e-3 # mH to H
                L2 = float(self.osc_l2.get()) * 1e-3 # mH to H
                M = float(self.osc_m.get()) * 1e-3    # mH to H
                C = float(self.osc_c1.get()) * 1e-9   # nF to F
                if L1 <= 0 or L2 <= 0 or C <= 0 or M < 0: raise ValueError("Inductances, capacitance must be positive. M non-negative.")
                
                Leq = L1 + L2 + 2 * M
                f = 1 / (2 * math.pi * math.sqrt(Leq * C))
                req_gain = (L1 + M) / (L2 + M)
                beta = 1 / req_gain
                summary = f"Hartley requirements:\n- Tank equivalent inductance Leq = {Leq*1e3:.2f} mH.\n- Feedback factor β = (L2 + M) / (L1 + M)."
                
            elif osc == "Colpitts":
                L = float(self.osc_l1.get()) * 1e-3   # mH to H
                C1 = float(self.osc_c1.get()) * 1e-9  # nF to F
                C2 = float(self.osc_c2.get()) * 1e-9  # nF to F
                if L <= 0 or C1 <= 0 or C2 <= 0: raise ValueError("Values must be positive.")
                
                Ceq = (C1 * C2) / (C1 + C2)
                f = 1 / (2 * math.pi * math.sqrt(L * Ceq))
                req_gain = C2 / C1
                beta = 1 / req_gain
                summary = f"Colpitts requirements:\n- Tank equivalent capacitance Ceq = {Ceq*1e9:.2f} nF.\n- Feedback factor β = C1 / C2."

            # Format frequency output
            if f >= 1e6:
                freq_str = f"{f/1e6:.3f} MHz"
            elif f >= 1e3:
                freq_str = f"{f/1e3:.3f} kHz"
            else:
                freq_str = f"{f:.2f} Hz"
                
            self.osc_output_lbl.configure(
                text=f"Oscillation Analysis Results:\n"
                     f"  - Frequency of Oscillation (fo) = {freq_str}\n"
                     f"  - Minimum Gain Required for Oscillation (Amin) = {req_gain:.3f}\n"
                     f"  - Feedback Attenuation Factor (β) = {beta:.4f}\n\n"
                     f"Syllabus Criteria:\n"
                     f"  - {summary}",
                style="CardAccent.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("Oscillator Calculator Error", f"Invalid input parameters:\n{str(e)}")

    def calculate_mosfet(self):
        try:
            dvgs = float(self.mos_dvgs.get())
            dvds = float(self.mos_dvds.get())
            did = float(self.mos_did.get()) # in mA
            
            if dvgs <= 0 or dvds <= 0 or did <= 0:
                raise ValueError("Dynamic voltage and current changes must be positive.")
                
            # gm = delta_Id / delta_Vgs (mA/V) -> convert to mS (millisiemens)
            gm = did / dvgs
            # rd = delta_Vds / delta_Id (V/mA) -> kΩ
            rd = dvds / did
            # mu = gm * rd
            mu = gm * rd
            
            self.mos_outputs.configure(
                text=f"Extracted Dynamic Parameters:\n"
                     f"  - Transconductance (gm) = {gm:.2f} mA/V (mS) = {gm*1000:.0f} μS\n"
                     f"  - AC Drain Resistance (rd) = {rd:.2f} kΩ = {rd*1000:.0f} Ω\n"
                     f"  - Amplification Factor (μ) = {mu:.2f} (Dimensionless)\n\n"
                     f"Formulas Used:\n"
                     f"  - rd = ΔVds / ΔId  (Vgs constant)\n"
                     f"  - gm = ΔId / ΔVgs  (Vds constant)\n"
                     f"  - μ = rd * gm = ΔVds / ΔVgs",
                style="CardAccent.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("MOSFET Extraction Error", f"Invalid input parameters:\n{str(e)}")

    def plot_opamp_response(self):
        try:
            cfg = self.op_config.get()
            Vp = float(self.op_vp.get())
            freq = float(self.op_freq.get())
            
            if Vp <= 0 or freq <= 0:
                raise ValueError("Amplitude and Frequency must be positive.")
                
            t = np.linspace(0, 2/freq, 1000)
            vin = Vp * np.sin(2 * np.pi * freq * t)
            
            if cfg in ["Inverting", "Non-Inverting"]:
                R1 = float(self.op_r1.get())
                Rf = float(self.op_rf.get())
                if R1 <= 0 or Rf <= 0: raise ValueError("Resistances must be positive.")
                
                if cfg == "Inverting":
                    gain = -Rf / R1
                    math_txt = f"Gain Av = -Rf / R1 = -{Rf}/{R1} = {gain:.2f} V/V"
                else:
                    gain = 1 + (Rf / R1)
                    math_txt = f"Gain Av = 1 + Rf / R1 = 1 + {Rf}/{R1} = {gain:.2f} V/V"
                vout = gain * vin
                
            elif cfg in ["Integrator", "Differentiator"]:
                R = float(self.op_r1.get()) * 1e3 # kΩ to Ω
                C = float(self.op_c.get()) * 1e-9  # nF to F
                if R <= 0 or C <= 0: raise ValueError("Resistance and capacitance must be positive.")
                
                RC = R * C
                omega = 2 * np.pi * freq
                
                if cfg == "Integrator":
                    # Vin = Vp * sin(omega * t) -> Vout = -1/RC * Integral(Vin dt) = 1/(RC * omega) * Vp * cos(omega * t)
                    gain_factor = 1.0 / (RC * omega)
                    vout = Vp * gain_factor * np.cos(2 * np.pi * freq * t)
                    math_txt = f"Integrator Time Constant RC = {RC*1e3:.2f} ms\nVo(t) = -1/RC ∫ Vi(t) dt\nGain at {freq} Hz = {gain_factor:.2f}"
                else:
                    # Vin = Vp * sin(omega * t) -> Vout = -RC * d(Vin)/dt = -RC * omega * Vp * cos(omega * t)
                    gain_factor = RC * omega
                    vout = -Vp * gain_factor * np.cos(2 * np.pi * freq * t)
                    math_txt = f"Differentiator Time Constant RC = {RC*1e3:.2f} ms\nVo(t) = -RC dVi(t)/dt\nGain at {freq} Hz = {gain_factor:.2f}"
            
            # Update math label
            self.op_math_lbl.configure(text=math_txt)
            
            # Plot
            self.op_ax.clear()
            self.op_ax.plot(t * 1000, vin, label="Vin", color="#888888", linestyle="--")
            self.op_ax.plot(t * 1000, vout, label="Vout (Op-Amp Output)", color=ACCENT_BLUE, linewidth=1.8)
            
            self.op_ax.set_facecolor(BG_DARK)
            self.op_ax.tick_params(colors=TEXT_WHITE)
            self.op_ax.spines['bottom'].set_color(BORDER_COLOR)
            self.op_ax.spines['top'].set_color(BORDER_COLOR)
            self.op_ax.spines['left'].set_color(BORDER_COLOR)
            self.op_ax.spines['right'].set_color(BORDER_COLOR)
            self.op_ax.set_xlabel("Time (ms)", color=TEXT_WHITE, fontsize=8)
            self.op_ax.set_ylabel("Voltage (V)", color=TEXT_WHITE, fontsize=8)
            self.op_ax.grid(True, color=GRID_COLOR, linestyle="--")
            self.op_ax.legend(facecolor=CARD_BG, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=8)
            
            self.op_canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Op-Amp Visualizer Error", f"Invalid input parameters:\n{str(e)}")

    def plot_filter_bode(self):
        try:
            filt = self.filt_type.get()
            fc = float(self.filt_fc.get())
            C = float(self.filt_c.get()) * 1e-9 # nF to F
            A0 = float(self.filt_a0.get())
            
            if fc <= 0 or C <= 0 or A0 <= 0:
                raise ValueError("Cutoff frequency, capacitance, and gain must be positive.")
                
            # R = 1 / (2 * pi * fc * C)
            R = 1 / (2 * math.pi * fc * C)
            
            # Format R output
            if R >= 1e3:
                r_str = f"{R/1e3:.2f} kΩ"
            else:
                r_str = f"{R:.2f} Ω"
                
            self.filt_output_lbl.configure(
                text=f"Design Parameters: Calculated Required Resistor R = {r_str} (fc = {fc:.1f} Hz, C = {C*1e9:.1f} nF)",
                style="CardAccent.TLabel"
            )
            
            # Generate frequencies on log scale: 0.05 * fc to 50 * fc
            freqs = np.logspace(np.log10(max(1, 0.05 * fc)), np.log10(50 * fc), 500)
            
            if filt == "1st-Order Low-Pass":
                # H = A0 / (1 + j (f / fc))
                mag = A0 / np.sqrt(1 + (freqs / fc)**2)
            else:
                # H = A0 * j(f / fc) / (1 + j (f / fc))
                mag = (A0 * (freqs / fc)) / np.sqrt(1 + (freqs / fc)**2)
                
            mag_db = 20 * np.log10(mag)
            
            self.filt_ax.clear()
            self.filt_ax.semilogx(freqs, mag_db, color=ACCENT_CYAN, linewidth=2, label="Magnitude Response")
            
            # Cutoff marker
            fc_db = 20 * np.log10(A0 / math.sqrt(2))
            self.filt_ax.axvline(x=fc, color=ACCENT_BLUE, linestyle="--", label=f"Cutoff fc = {fc:.0f} Hz")
            self.filt_ax.axhline(y=fc_db, color="#ff7582", linestyle=":", label=f"-3 dB point ({fc_db:.1f} dB)")
            self.filt_ax.plot(fc, fc_db, "ro", markersize=6)
            
            self.filt_ax.set_facecolor(BG_DARK)
            self.filt_ax.tick_params(colors=TEXT_WHITE)
            self.filt_ax.spines['bottom'].set_color(BORDER_COLOR)
            self.filt_ax.spines['top'].set_color(BORDER_COLOR)
            self.filt_ax.spines['left'].set_color(BORDER_COLOR)
            self.filt_ax.spines['right'].set_color(BORDER_COLOR)
            self.filt_ax.set_title(f"Bode Plot: {filt}", color=ACCENT_CYAN, fontname="Segoe UI", fontsize=10)
            self.filt_ax.set_xlabel("Frequency (Hz)", color=TEXT_WHITE, fontsize=8)
            self.filt_ax.set_ylabel("Gain (dB)", color=TEXT_WHITE, fontsize=8)
            self.filt_ax.grid(True, which="both", color=GRID_COLOR, linestyle="--")
            self.filt_ax.legend(facecolor=CARD_BG, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=8)
            
            self.filt_canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Filter Design Wizard Error", f"Invalid input parameters:\n{str(e)}")

# ==========================================
# MAIN EXECUTION LOOP
# ==========================================
if __name__ == "__main__":
    app = AnalogCircuitToolboxApp()
    # Handle clean close
    def on_closing():
        app.quit()
        app.destroy()
        sys.exit(0)
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
