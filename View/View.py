import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import geopandas as gpd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Trips import trip, graphing

class UserInterface:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("User Interface with Map")
        self.apiKey = api_key

        self.tour = None
        self.pos = None
        self.graph = None
        self.human = None

        # Create a frame for the map (placeholder)
        self.map_frame = tk.Frame(root, width=800, height=600, bg='lightgray')
        self.map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for the input fields
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Create a frame for the controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Name input
        tk.Label(self.input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Surname input
        tk.Label(self.input_frame, text="Surname:").grid(row=0, column=2, padx=5, pady=5)
        self.surname_entry = tk.Entry(self.input_frame)
        self.surname_entry.grid(row=0, column=3, padx=5, pady=5)

        # City input
        tk.Label(self.input_frame, text="City:").grid(row=0, column=4, padx=5, pady=5)
        self.city_entry = tk.Entry(self.input_frame)
        self.city_entry.grid(row=0, column=5, padx=5, pady=5)

        # File input
        tk.Label(self.input_frame, text="Files:").grid(row=0, column=6, padx=5, pady=5)
        self.file_entry = tk.Entry(self.input_frame)
        self.file_entry.grid(row=0, column=7, padx=5, pady=5)
        self.browse_button = tk.Button(self.input_frame, text="Browse", command=self.browse_files)
        self.browse_button.grid(row=0, column=8, padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=0, column=9, padx=5, pady=5)

        # Number of trips input
        tk.Label(self.controls_frame, text="Number of Trips:").grid(row=0, column=0, padx=5, pady=5)
        self.num_trips_combobox = Combobox(self.controls_frame, values=list(range(1, 11)))
        self.num_trips_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.num_trips_combobox.bind("<<ComboboxSelected>>", self.update_trip_selection)
        self.num_trips_combobox.current(0)

        # Trip selection input
        tk.Label(self.controls_frame, text="Select Trip:").grid(row=1, column=0, padx=5, pady=5)
        self.trip_selection_combobox = Combobox(self.controls_frame, values=["1"])
        self.trip_selection_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.trip_selection_combobox.config(state='disabled')

        # Distance input and Zoom button
        tk.Label(self.controls_frame, text="Distance:").grid(row=2, column=0, padx=5, pady=5)
        self.distance_entry = tk.Entry(self.controls_frame)
        self.distance_entry.grid(row=2, column=1, padx=5, pady=5)
        self.distance_entry.insert(0, "2000")
        self.distance_entry.config(state='disabled')

        self.zoom_button = tk.Button(self.controls_frame, text="Zoom", command=self.zoom)
        self.zoom_button.grid(row=2, column=2, padx=5, pady=5)
        self.zoom_button.config(state='disabled')

        self.change_trip_button = tk.Button(self.controls_frame, text="Change Trip", command=self.change_trip)
        self.change_trip_button.grid(row=1, column=2, padx=5, pady=5)
        self.change_trip_button.config(state='disabled')

    def browse_files(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if filenames:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, ', '.join(filenames))

    def submit(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        city = self.city_entry.get().strip()
        filepaths = self.file_entry.get().strip()

        # Validate input
        if not name or not surname or not city or not filepaths:
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        try:
            filepaths_list = filepaths.split(', ')
            # Create a HumanTraveller object and plan the trip
            self.human = trip.HumanTraveller(f'{name}_{surname}', "---", city, filepaths_list, self.apiKey, trip_type='drive')
            self.tour, self.pos, self.graph = self.human.trip_planner(n=1)
            distance = self.distance_entry.get().strip()
            nodes, routes, fig, ax, fig2, ax2 = graphing.create_and_plot_routes(self.tour, self.pos, self.graph, distance=int(distance))
            self.plot_map(fig, ax)
            # After plotting the map, add the Distance entry and Zoom button
            self.enable_additional_inputs()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def plot_map(self, fig, ax):
        try:
            for widget in self.map_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=self.map_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        except Exception as e:
            raise RuntimeError(f"Failed to plot map: {e}")

    def enable_additional_inputs(self):
        self.distance_entry.config(state='normal')
        self.zoom_button.config(state='normal')
        self.trip_selection_combobox.config(state='normal')
        self.change_trip_button.config(state='normal')

    def update_trip_selection(self, event):
        num_trips = int(self.num_trips_combobox.get())
        self.trip_selection_combobox['values'] = list(range(1, num_trips + 1))
        self.trip_selection_combobox.current(0)

    def zoom(self):
        distance = self.distance_entry.get().strip()
        try:
            nodes, routes, fig, ax, fig2, ax2 = graphing.create_and_plot_routes(self.tour, self.pos, self.graph, distance=int(distance))
            self.plot_map(fig, ax)
            print(f"Zooming to distance: {distance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during zoom: {str(e)}")

    def change_trip(self):
        selected_trip = int(self.trip_selection_combobox.get())
        try:
            # Replace this with your actual logic to change the trip and update the map
            self.tour, self.pos, self.graph = self.human.trip_planner(n=selected_trip)
            distance = self.distance_entry.get().strip()
            nodes, routes, fig, ax, fig2, ax2 = graphing.create_and_plot_routes(self.tour, self.pos, self.graph,
                                                                                distance=int(distance))
            self.plot_map(fig, ax)
            print(f"Changed to trip: {selected_trip}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while changing trip: {str(e)}")
