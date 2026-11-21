
import tkinter as tk
from tkinter import ttk, messagebox

from Bankers import run_bankers_algorithm
from Validation import validate_all, ValidationError

class BankersSimulator:

    def __init__(self, root):
        self.root = root

        # ==============================
        # WINDOW CONFIGURATION
        # ==============================

        self.root.title("BANKER'S ALGORITHM | SYSTEM SIMULATOR")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 680)
        self.root.configure(bg="#080F1D")

        self.colors = {
            "bg": "#080F1D",
            "sidebar": "#0D192B",
            "panel": "#122238",
            "card": "#172B43",
            "input": "#0B1728",
            "cyan": "#00E5FF",
            "blue": "#168BFF",
            "white": "#F0F9FF",
            "muted": "#8BA4BD",
            "green": "#00E5A0",
            "red": "#FF5577",
            "border": "#23435E"
        }

        # Application data
        self.process_count = 0
        self.resource_count = 0

        self.total_entries = []
        self.allocation_entries = []
        self.maximum_entries = []

        self.current_page = "Dashboard"
        self.last_result = None

        self.setup_styles()
        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

    # ==============================
    # STYLE CONFIGURATION
    # ==============================

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.colors["panel"],
            foreground=self.colors["white"],
            fieldbackground=self.colors["panel"],
            rowheight=35,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.colors["sidebar"],
            foreground=self.colors["cyan"],
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#164E63")],
            foreground=[("selected", self.colors["white"])]
        )

    # ==============================
    # REUSABLE UI COMPONENTS
    # ==============================

    def create_label(self, parent, text, size=10,
                     color=None, bold=False):

        return tk.Label(
            parent,
            text=text,
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal"
            ),
            fg=color or self.colors["white"],
            bg=parent.cget("bg")
        )

    def create_button(self, parent, text, command,
                      primary=True):

        bg = (
            self.colors["cyan"]
            if primary else self.colors["card"]
        )

        fg = (
            "#061321"
            if primary else self.colors["white"]
        )

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground="#67E8F9",
            activeforeground="#061321",
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
            cursor="hand2"
        )

    def create_entry(self, parent, width=12):

        return tk.Entry(
            parent,
            width=width,
            font=("Segoe UI", 10),
            bg=self.colors["input"],
            fg=self.colors["white"],
            insertbackground=self.colors["cyan"],
            relief="flat",
            bd=0,
            justify="center"
        )

    def create_card(self, parent, title, value,
                    subtitle, accent=None):

        card = tk.Frame(
            parent,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        tk.Label(
            card,
            text=title.upper(),
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=18, pady=(17, 5))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 26, "bold"),
            fg=accent or self.colors["cyan"],
            bg=self.colors["card"]
        )
        value_label.pack(anchor="w", padx=18)

        tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=18, pady=(3, 17))

        return card, value_label

    # ==============================
    # SIDEBAR
    # ==============================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=235
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )
        logo.pack(fill="x", padx=22, pady=(30, 5))

        tk.Label(
            logo,
            text="◈",
            font=("Segoe UI", 27, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["sidebar"]
        ).pack(side="left")

        tk.Label(
            logo,
            text="BANKER'S",
            font=("Segoe UI", 17, "bold"),
            fg=self.colors["white"],
            bg=self.colors["sidebar"]
        ).pack(side="left", padx=7)

        tk.Label(
            self.sidebar,
            text="RESOURCE ALLOCATION SYSTEM",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["sidebar"]
        ).pack(anchor="w", padx=25, pady=(0, 35))

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 8, "bold"),
            fg="#59748E",
            bg=self.colors["sidebar"]
        ).pack(anchor="w", padx=23, pady=(0, 10))

        self.nav_buttons = {}

        navigation = [
            ("Dashboard", "▦"),
            ("System Input", "▤"),
            ("Simulation", "◉"),
            ("Results", "▣")
        ]

        for page, symbol in navigation:

            btn = tk.Button(
                self.sidebar,
                text=f"   {symbol}    {page}",
                command=lambda p=page: self.navigate(p),
                font=("Segoe UI", 10, "bold"),
                fg=self.colors["muted"],
                bg=self.colors["sidebar"],
                activebackground=self.colors["panel"],
                activeforeground=self.colors["cyan"],
                relief="flat",
                bd=0,
                anchor="w",
                padx=12,
                pady=15,
                cursor="hand2"
            )

            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[page] = btn

        # Sidebar footer
        footer = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )
        footer.pack(side="bottom", fill="x", padx=20, pady=22)

        tk.Frame(
            footer,
            bg=self.colors["border"],
            height=1
        ).pack(fill="x", pady=(0, 15))

        tk.Label(
            footer,
            text="PLATFORM TECHNOLOGIES",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["sidebar"]
        ).pack(anchor="w")

        tk.Label(
            footer,
            text="FINAL PROJECT  |  PYTHON",
            font=("Segoe UI", 8),
            fg="#59748E",
            bg=self.colors["sidebar"]
        ).pack(anchor="w", pady=4)

    def navigate(self, page):

        self.current_page = page

        for name, button in self.nav_buttons.items():

            if name == page:
                button.configure(
                    bg="#12374A",
                    fg=self.colors["cyan"]
                )
            else:
                button.configure(
                    bg=self.colors["sidebar"],
                    fg=self.colors["muted"]
                )

        pages = {
            "Dashboard": self.show_dashboard,
            "System Input": self.show_input,
            "Simulation": self.show_simulation,
            "Results": self.show_results
        }

        pages[page]()

    # ==============================
    # MAIN CONTENT AREA
    # ==============================

    def create_main_area(self):

        self.main_area = tk.Frame(
            self.root,
            bg=self.colors["bg"]
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Top status bar
        topbar = tk.Frame(
            self.main_area,
            bg=self.colors["bg"],
            height=55
        )

        topbar.pack(fill="x", padx=35, pady=(10, 0))
        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="SYSTEM CONTROL CENTER",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["bg"]
        ).pack(side="left", pady=15)

        tk.Label(
            topbar,
            text="●  INTERFACE ONLINE",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["green"],
            bg=self.colors["bg"]
        ).pack(side="right", pady=15)

        self.page_area = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        self.page_area.pack(
            fill="both",
            expand=True
        )

    def clear_page(self):

        for widget in self.page_area.winfo_children():
            widget.destroy()

    def create_page_header(self, title, description):

        header = tk.Frame(
            self.page_area,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(20, 22)
        )

        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 25, "bold"),
            fg=self.colors["white"],
            bg=self.colors["bg"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text=description,
            font=("Segoe UI", 10),
            fg=self.colors["muted"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(5, 0))

    def create_section(self, parent, title):

        frame = tk.Frame(
            parent,
            bg=self.colors["panel"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        tk.Label(
            frame,
            text=title.upper(),
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["panel"]
        ).pack(anchor="w", padx=18, pady=(16, 12))

        return frame

    # ==============================
    # DASHBOARD
    # ==============================

    def show_dashboard(self):

        self.clear_page()

        self.create_page_header(
            "Dashboard",
            "Monitor your system and manage resource allocation."
        )

        cards = tk.Frame(
            self.page_area,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x", padx=28, pady=10)

        self.process_card, self.process_value = self.create_card(
            cards, "Processes", str(self.process_count),
            "Configured processes"
        )

        self.process_card.pack(
            side="left", fill="both", expand=True, padx=7
        )

        self.resource_card, self.resource_value = self.create_card(
            cards, "Resources", str(self.resource_count),
            "Resource types"
        )

        self.resource_card.pack(
            side="left", fill="both", expand=True, padx=7
        )

        self.status_card, self.status_value = self.create_card(
            cards, "System Status", "NOT RUN",
            "Waiting for simulation", self.colors["muted"]
        )

        self.status_card.pack(
            side="left", fill="both", expand=True, padx=7
        )

        # Welcome section
        panel = self.create_section(
            self.page_area,
            "System Overview"
        )

        panel.pack(fill="x", padx=35, pady=22)

        tk.Label(
            panel,
            text="DEADLOCK AVOIDANCE SYSTEM",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors["white"],
            bg=self.colors["panel"]
        ).pack(anchor="w", padx=20, pady=(8, 5))

        description = (
            "Welcome to the Banker's Algorithm Simulator. "
            "This application demonstrates how an operating "
            "system avoids deadlock by checking resource "
            "allocation and determining whether a system "
            "can remain in a safe state."
        )

        tk.Label(
            panel,
            text=description,
            font=("Segoe UI", 10),
            fg=self.colors["muted"],
            bg=self.colors["panel"],
            justify="left",
            wraplength=800
        ).pack(anchor="w", padx=20, pady=10)

        self.create_button(
            panel,
            "CONFIGURE SYSTEM  →",
            lambda: self.navigate("System Input")
        ).pack(anchor="w", padx=20, pady=(10, 20))

        # Quick information
        info = tk.Frame(
            self.page_area,
            bg=self.colors["bg"]
        )
        info.pack(fill="x", padx=35, pady=5)

        tk.Label(
            info,
            text="HOW IT WORKS",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=8)

        steps = [
            "01  Configure processes and resources",
            "02  Enter Allocation and Max matrices",
            "03  Execute the Safety Algorithm",
            "04  Review the system safety result"
        ]

        for step in steps:
            tk.Label(
                info,
                text="   " + step,
                font=("Segoe UI", 10),
                fg=self.colors["muted"],
                bg=self.colors["bg"]
            ).pack(anchor="w", pady=4)

    # ==============================
    # SYSTEM INPUT PAGE
    # ==============================

    def show_input(self):

        self.clear_page()

        self.create_page_header(
            "System Configuration",
            "Define the number of processes and resource types."
        )

        config = self.create_section(
            self.page_area,
            "Configuration Settings"
        )

        config.pack(fill="x", padx=35, pady=10)

        fields = tk.Frame(
            config,
            bg=self.colors["panel"]
        )
        fields.pack(anchor="w", padx=20, pady=5)

        # Process count
        tk.Label(
            fields,
            text="NUMBER OF PROCESSES",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        ).grid(row=0, column=0, sticky="w", padx=(0, 35))

        self.process_entry = self.create_entry(fields, 15)
        self.process_entry.insert(0, str(self.process_count or 5))
        self.process_entry.grid(row=1, column=0, ipady=9, pady=8)

        # Resource count
        tk.Label(
            fields,
            text="NUMBER OF RESOURCE TYPES",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        ).grid(row=0, column=1, sticky="w")

        self.resource_entry = self.create_entry(fields, 15)
        self.resource_entry.insert(0, str(self.resource_count or 3))
        self.resource_entry.grid(row=1, column=1, ipady=9, pady=8)

        self.create_button(
            config,
            "GENERATE MATRICES  →",
            self.generate_matrices
        ).pack(anchor="w", padx=20, pady=(12, 20))

        # Matrix area
        self.matrix_container = tk.Frame(
            self.page_area,
            bg=self.colors["bg"]
        )

        self.matrix_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        self.matrix_canvas = tk.Canvas(
            self.matrix_container,
            bg=self.colors["bg"],
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            self.matrix_container,
            orient="vertical",
            command=self.matrix_canvas.yview
        )

        self.matrix_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.matrix_canvas.pack(
            side="left", fill="both", expand=True
        )

        self.matrix_content = tk.Frame(
            self.matrix_canvas,
            bg=self.colors["bg"]
        )

        self.canvas_window = self.matrix_canvas.create_window(
            (0, 0),
            window=self.matrix_content,
            anchor="nw"
        )

        self.matrix_content.bind(
            "<Configure>",
            lambda event: self.matrix_canvas.configure(
                scrollregion=self.matrix_canvas.bbox("all")
            )
        )

        self.matrix_canvas.bind(
            "<Configure>",
            lambda event: self.matrix_canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )
        )

        if self.process_count and self.resource_count:
            self.build_matrix_editor(
                self.process_count,
                self.resource_count
            )

    # ==============================
    # DYNAMIC MATRIX GENERATOR
    # ==============================

    def generate_matrices(self):

        try:
            processes = int(self.process_entry.get())
            resources = int(self.resource_entry.get())

            if processes <= 0 or resources <= 0:
                raise ValueError

            if processes > 15 or resources > 10:
                messagebox.showwarning(
                    "Configuration Limit",
                    "For this prototype, use a maximum of "
                    "15 processes and 10 resource types."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Configuration",
                "Enter positive whole numbers for processes "
                "and resource types."
            )
            return

        self.process_count = processes
        self.resource_count = resources

        self.build_matrix_editor(processes, resources)

    def build_matrix_editor(self, processes, resources):

        for widget in self.matrix_content.winfo_children():
            widget.destroy()

        self.total_entries = []
        self.allocation_entries = []
        self.maximum_entries = []

        # TOTAL RESOURCE VECTOR
        total_panel = self.create_section(
            self.matrix_content,
            "Total Resource Vector"
        )

        total_panel.pack(fill="x", pady=(5, 15))

        total_grid = tk.Frame(
            total_panel,
            bg=self.colors["panel"]
        )
        total_grid.pack(anchor="w", padx=18, pady=(0, 18))

        for j in range(resources):

            cell = tk.Frame(
                total_grid,
                bg=self.colors["panel"]
            )
            cell.grid(row=0, column=j, padx=6)

            tk.Label(
                cell,
                text=f"R{j}",
                font=("Segoe UI", 9, "bold"),
                fg=self.colors["cyan"],
                bg=self.colors["panel"]
            ).pack(pady=5)

            entry = self.create_entry(cell, 7)
            entry.insert(0, "10")
            entry.pack(ipady=7)

            self.total_entries.append(entry)

        # ALLOCATION AND MAX MATRICES
        matrix_row = tk.Frame(
            self.matrix_content,
            bg=self.colors["bg"]
        )
        matrix_row.pack(fill="x", pady=5)

        allocation_panel = self.create_section(
            matrix_row,
            "Allocation Matrix"
        )

        allocation_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        maximum_panel = self.create_section(
            matrix_row,
            "Maximum Matrix"
        )

        maximum_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        self.create_matrix_inputs(
            allocation_panel,
            processes,
            resources,
            self.allocation_entries
        )

        self.create_matrix_inputs(
            maximum_panel,
            processes,
            resources,
            self.maximum_entries
        )

        # ACTION BUTTONS
        actions = tk.Frame(
            self.matrix_content,
            bg=self.colors["bg"]
        )
        actions.pack(fill="x", pady=18)

        self.create_button(
            actions,
            "PREVIEW INPUT",
            self.preview_input
        ).pack(side="left", padx=(0, 10))

        self.create_button(
            actions,
            "RUN SIMULATION  →",
            self.run_simulation
        ).pack(side="left")

        # Update dashboard data
        self.process_count = processes
        self.resource_count = resources

    def create_matrix_inputs(
        self, parent, processes, resources, storage
    ):

        grid = tk.Frame(
            parent,
            bg=self.colors["panel"]
        )

        grid.pack(anchor="w", padx=10, pady=(0, 18))

        # Column labels
        tk.Label(
            grid,
            text="PROCESS",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        ).grid(row=0, column=0, padx=5, pady=7)

        for j in range(resources):

            tk.Label(
                grid,
                text=f"R{j}",
                font=("Segoe UI", 8, "bold"),
                fg=self.colors["cyan"],
                bg=self.colors["panel"]
            ).grid(row=0, column=j + 1, padx=4, pady=7)

        # Process rows
        for i in range(processes):

            tk.Label(
                grid,
                text=f"P{i}",
                font=("Segoe UI", 9, "bold"),
                fg=self.colors["white"],
                bg=self.colors["panel"]
            ).grid(row=i + 1, column=0, padx=5, pady=5)

            row_entries = []

            for j in range(resources):

                entry = self.create_entry(grid, 5)

                entry.grid(
                    row=i + 1,
                    column=j + 1,
                    padx=4,
                    pady=5,
                    ipady=6
                )

                entry.insert(0, "0")
                row_entries.append(entry)

            storage.append(row_entries)

    # ==============================
    # INPUT PREVIEW
    # ==============================

    def preview_input(self):

        try:
            total = [
                int(entry.get())
                for entry in self.total_entries
            ]

            allocation = [
                [int(entry.get()) for entry in row]
                for row in self.allocation_entries
            ]

            maximum = [
                [int(entry.get()) for entry in row]
                for row in self.maximum_entries
            ]

            values = total + [
                value
                for row in allocation + maximum
                for value in row
            ]

            if any(value < 0 for value in values):
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "All resource values must be "
                "non-negative whole numbers."
            )
            return

        messagebox.showinfo(
            "Input Preview",
            f"Processes: {self.process_count}\n"
            f"Resource Types: {self.resource_count}\n\n"
            f"Total Resources: {total}\n\n"
            f"Allocation Matrix:\n{allocation}\n\n"
            f"Maximum Matrix:\n{maximum}\n\n"
            "Input format preview completed."
        )

    # ==============================
    # RUN BANKER'S ALGORITHM
    # ==============================

    def run_simulation(self):
        """Read GUI values, validate them, and run the algorithm."""
        try:
            if not self.total_entries:
                raise ValidationError("Please generate and complete the matrices first.")

            total = [int(entry.get().strip()) for entry in self.total_entries]
            allocation = [
                [int(entry.get().strip()) for entry in row]
                for row in self.allocation_entries
            ]
            maximum = [
                [int(entry.get().strip()) for entry in row]
                for row in self.maximum_entries
            ]

            # Validate the dimensions and resource constraints before calculation.
            validate_all(
                self.process_count,
                self.resource_count,
                total,
                allocation,
                maximum
            )

            self.last_result = run_bankers_algorithm(total, allocation, maximum)
            self.navigate("Simulation")

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                "Please enter non-negative whole numbers in every field.\n\n" + str(error)
            )
        except ValidationError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror(
                "Simulation Error",
                f"The simulation could not be completed:\n{error}"
            )

    # ==============================
    # SIMULATION PAGE
    # ==============================

    def show_simulation(self):
        self.clear_page()

        self.create_page_header(
            "Algorithm Simulation",
            "Review the resource calculations and each step of the Safety Algorithm."
        )

        if self.last_result is None:
            panel = self.create_section(self.page_area, "Simulation Control")
            panel.pack(fill="x", padx=35, pady=10)
            tk.Label(
                panel,
                text="NO SIMULATION HAS BEEN RUN",
                font=("Segoe UI", 16, "bold"),
                fg=self.colors["muted"],
                bg=self.colors["panel"]
            ).pack(anchor="w", padx=20, pady=20)
            self.create_button(
                panel, "OPEN SYSTEM INPUT",
                lambda: self.navigate("System Input"), primary=False
            ).pack(anchor="w", padx=20, pady=(0, 20))
            return

        result = self.last_result
        summary = self.create_section(self.page_area, "Calculated Resource Values")
        summary.pack(fill="x", padx=35, pady=8)

        summary_text = (
            f"Total:     {result['total']}\n"
            f"Available: {result['available']}\n\n"
            f"Need Matrix (Max - Allocation):\n"
            + "\n".join(f"P{i}: {row}" for i, row in enumerate(result['need']))
        )
        tk.Label(
            summary, text=summary_text, justify="left",
            font=("Consolas", 10), fg=self.colors["white"],
            bg=self.colors["panel"]
        ).pack(anchor="w", padx=20, pady=(0, 18))

        trace_panel = self.create_section(self.page_area, "Execution Trace")
        trace_panel.pack(fill="both", expand=True, padx=35, pady=8)

        trace_frame = tk.Frame(trace_panel, bg=self.colors["panel"])
        trace_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        trace_scroll = ttk.Scrollbar(trace_frame, orient="vertical")
        trace_text = tk.Text(
            trace_frame, height=12, wrap="word",
            bg=self.colors["input"], fg=self.colors["white"],
            insertbackground=self.colors["white"],
            font=("Consolas", 9), relief="flat",
            yscrollcommand=trace_scroll.set
        )
        trace_scroll.config(command=trace_text.yview)
        trace_scroll.pack(side="right", fill="y")
        trace_text.pack(side="left", fill="both", expand=True)

        for item in result["trace"]:
            event = item.get("event", "STEP")
            step = item.get("step", "-")
            message = item.get("message", "")
            trace_text.insert("end", f"STEP {step} | {event}\n")
            if "process" in item:
                trace_text.insert("end", f"Process: {item['process']}\n")
            if "need" in item:
                trace_text.insert("end", f"Need: {item['need']}\n")
            if "can_execute" in item:
                trace_text.insert(
                    "end",
                    f"Can execute: {'YES' if item['can_execute'] else 'NO'}\n"
                )
            if "previous_work" in item:
                trace_text.insert("end", f"Previous Work: {item['previous_work']}\n")
            if "allocation" in item:
                trace_text.insert("end", f"Released Allocation: {item['allocation']}\n")
            if "work" in item:
                trace_text.insert("end", f"Work: {item['work']}\n")
            if "finish" in item:
                trace_text.insert("end", f"Finish: {item['finish']}\n")
            trace_text.insert("end", f"{message}\n{'-' * 55}\n")

        trace_text.configure(state="disabled")

        actions = tk.Frame(self.page_area, bg=self.colors["bg"])
        actions.pack(fill="x", padx=35, pady=(5, 15))
        self.create_button(
            actions, "VIEW FINAL RESULTS  →",
            lambda: self.navigate("Results")
        ).pack(side="left", padx=(0, 10))
        self.create_button(
            actions, "EDIT INPUTS",
            lambda: self.navigate("System Input"), primary=False
        ).pack(side="left")

    # ==============================
    # RESULTS PAGE
    # ==============================

    def show_results(self):
        self.clear_page()

        self.create_page_header(
            "Simulation Results",
            "Final safety status, safe sequence, and algorithm calculations."
        )

        if self.last_result is None:
            panel = self.create_section(self.page_area, "Final System Status")
            panel.pack(fill="x", padx=35, pady=10)
            tk.Label(
                panel, text="NO SIMULATION RESULTS",
                font=("Segoe UI", 18, "bold"),
                fg=self.colors["muted"], bg=self.colors["panel"]
            ).pack(anchor="w", padx=20, pady=20)
            return

        result = self.last_result
        safe = result["safe"]
        status = "SAFE STATE" if safe else "UNSAFE STATE"
        status_color = self.colors["green"] if safe else self.colors["red"]

        status_panel = self.create_section(self.page_area, "Final System Status")
        status_panel.pack(fill="x", padx=35, pady=10)
        tk.Label(
            status_panel, text=status,
            font=("Segoe UI", 25, "bold"),
            fg=status_color, bg=self.colors["panel"]
        ).pack(anchor="w", padx=20, pady=(12, 5))
        explanation = (
            "All processes can finish in a safe order." if safe
            else "The system is unsafe because no unfinished process can proceed with the currently available resources."
        )
        tk.Label(
            status_panel, text=explanation,
            font=("Segoe UI", 10), fg=self.colors["muted"],
            bg=self.colors["panel"], wraplength=850, justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        sequence_panel = self.create_section(self.page_area, "Safe Sequence")
        sequence_panel.pack(fill="x", padx=35, pady=10)
        sequence = ("  →  ".join(result["safe_sequence"])
                    if safe else "No complete safe sequence exists.")
        tk.Label(
            sequence_panel, text=sequence,
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["cyan"] if safe else self.colors["red"],
            bg=self.colors["panel"]
        ).pack(anchor="w", padx=20, pady=20)

        details = self.create_section(self.page_area, "Final Algorithm Values")
        details.pack(fill="both", expand=True, padx=35, pady=10)
        detail_text = (
            f"Process count: {result['process_count']}\n"
            f"Resource types: {result['resource_count']}\n"
            f"Available: {result['available']}\n"
            f"Final Work: {result['final_work']}\n"
            f"Finish flags: {result['finish']}\n\n"
            f"Need Matrix:\n"
            + "\n".join(f"P{i}: {row}" for i, row in enumerate(result['need']))
        )
        tk.Label(
            details, text=detail_text, justify="left",
            font=("Consolas", 10), fg=self.colors["white"],
            bg=self.colors["panel"]
        ).pack(anchor="w", padx=20, pady=(0, 18))

        self.create_button(
            self.page_area, "BACK TO SIMULATION",
            lambda: self.navigate("Simulation"), primary=False
        ).pack(anchor="w", padx=35, pady=(0, 15))


# ==================================
# APPLICATION ENTRY POINT
# ==================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BankersSimulator(root)

    root.mainloop()
