import tkinter as tk
from tkinter import filedialog, messagebox
import geopandas as gpd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Trips import trip

class UserInterface:
    def __init__(self, root, api_key):
        self.root = root
        self.apiKey = api_key
        self.root.title("User Interface with Map")

        # Create a frame for the map (placeholder)
        self.map_frame = tk.Frame(root, width=800, height=600, bg='lightgray')
        self.map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for the input fields
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Name input
        tk.Label(self.input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Surname input
        tk.Label(self.input_frame, text="Surname:").grid(row=1, column=0, padx=5, pady=5)
        self.surname_entry = tk.Entry(self.input_frame)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=5)

        # City input
        tk.Label(self.input_frame, text="City:").grid(row=2, column=0, padx=5, pady=5)
        self.city_entry = tk.Entry(self.input_frame)
        self.city_entry.grid(row=2, column=1, padx=5, pady=5)

        # File input
        tk.Label(self.input_frame, text="Files:").grid(row=3, column=0, padx=5, pady=5)
        self.file_entry = tk.Entry(self.input_frame)
        self.file_entry.grid(row=3, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.input_frame, text="Browse", command=self.browse_files)
        self.browse_button.grid(row=3, column=2, padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=3, pady=10)

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
            # For demonstration, we will create a simple GeoDataFrame and plot it
            human = trip.HumanTraveller(f'{name}_{surname}', "---", city, filepaths_list, self.apiKey)
            # human.trip_planner()
            self.plot_map(filepaths_list)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def plot_map(self, filepaths):
        # Create a simple GeoDataFrame for demonstration
        try:
            # Load a GeoDataFrame (this is just an example, replace with your logic)
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            world.plot(ax=ax)

            # Clear the map frame and add the new canvas
            for widget in self.map_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=self.map_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except Exception as e:
            raise RuntimeError(f"Failed to plot map: {e}")
