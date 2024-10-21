import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import folium
import webbrowser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main UI window
root = tk.Tk()
root.title("Sensor Data Visualization")
root.geometry("1000x800")

sensor_type = None
sonar_canvas = None
tracking_dot = None

# Function to generate random temperature or humidity values
def generate_random_values():
    return [random.uniform(20, 40) for _ in range(10)]  # Random values for temperature/humidity

# Function to create a map using Folium and display it in a browser
def create_map(latitudes, longitudes):
    m = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=5)
    for lat, lon in zip(latitudes, longitudes):
        folium.Marker([lat, lon], popup=f"Location: {lat}, {lon}").add_to(m)
    
    # Save the map as an HTML file and open it in the default web browser
    map_file = "map.html"
    m.save(map_file)
    webbrowser.open(map_file)

# Function to update graphs for temperature/humidity
def update_graph(sensor_type, ax, fig):
    if sensor_type == "Temperature":
        y_data = generate_random_values()
        ax.clear()
        ax.plot(range(10), y_data, label="Temperature (°C)")
        ax.set_title("Temperature over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature")
        ax.legend()
    elif sensor_type == "Humidity":
        y_data = generate_random_values()
        ax.clear()
        ax.plot(range(10), y_data, label="Humidity (%)")
        ax.set_title("Humidity over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Humidity")
        ax.legend()

    fig.canvas.draw()

# Function to simulate live sonar tracking
def live_sonar_update():
    global sonar_canvas, tracking_dot

    # Move the dot randomly on the canvas
    x_new, y_new = random.randint(50, 350), random.randint(50, 350)
    sonar_canvas.coords(tracking_dot, x_new - 5, y_new - 5, x_new + 5, y_new + 5)

    # Repeat the movement every 500 milliseconds
    root.after(500, live_sonar_update)

# Function to show the final visualization after sensor selection
def show_visualization():
    if sensor_type in ["Temperature", "Humidity"]:
        lat1, lat2, lat3, lat4 = float(entry_lat1.get()), float(entry_lat2.get()), float(entry_lat3.get()), float(entry_lat4.get())
        lon1, lon2, lon3, lon4 = float(entry_lon1.get()), float(entry_lon2.get()), float(entry_lon3.get()), float(entry_lon4.get())
        latitudes = [lat1, lat2, lat3, lat4]
        longitudes = [lon1, lon2, lon3, lon4]

        # Create graph for temperature/humidity
        fig, ax = plt.subplots(figsize=(5, 4))
        update_graph(sensor_type, ax, fig)

        # Create Tkinter canvas to display the graph
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create and display the map
        create_map(latitudes, longitudes)
    
    elif sensor_type == "Sonar":
        # Create a sonar canvas for live tracking
        global sonar_canvas, tracking_dot

        sonar_canvas = tk.Canvas(root, width=400, height=400, bg="black")
        sonar_canvas.pack(pady=20)
        sonar_canvas.create_oval(50, 50, 350, 350, outline="green", width=2)  # Outer sonar circle

        # Add a tracking dot
        tracking_dot = sonar_canvas.create_oval(190, 190, 210, 210, fill="red")

        # Start live sonar updates
        live_sonar_update()

# Function to ask for sensor selection
def select_sensor(sensor):
    global sensor_type
    sensor_type = sensor
    messagebox.showinfo("Selected Sensor", f"You have selected {sensor} sensor.")
    
    # Clear the previous widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    # If sonar is selected, skip latitude and longitude inputs
    if sensor_type == "Sonar":
        tk.Button(root, text="Start Sonar Tracking", command=show_visualization).pack(pady=10)
        return

    # Otherwise, ask for latitudes and longitudes
    global entry_lat1, entry_lat2, entry_lat3, entry_lat4, entry_lon1, entry_lon2, entry_lon3, entry_lon4
    tk.Label(root, text="Enter Latitude and Longitude").pack()
    
    entry_lat1 = create_entry(root, "Enter latitude 1")
    entry_lat1.pack()

    entry_lat2 = create_entry(root, "Enter latitude 2")
    entry_lat2.pack()

    entry_lat3 = create_entry(root, "Enter latitude 3")
    entry_lat3.pack()

    entry_lat4 = create_entry(root, "Enter latitude 4")
    entry_lat4.pack()

    entry_lon1 = create_entry(root, "Enter longitude 1")
    entry_lon1.pack()

    entry_lon2 = create_entry(root, "Enter longitude 2")
    entry_lon2.pack()

    entry_lon3 = create_entry(root, "Enter longitude 3")
    entry_lon3.pack()

    entry_lon4 = create_entry(root, "Enter longitude 4")
    entry_lon4.pack()

    tk.Button(root, text="Submit", command=show_visualization).pack()

# Utility functions for managing placeholder text in entries
def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(event, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")

def create_entry(root, placeholder):
    entry = tk.Entry(root, fg="gray")
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, entry, placeholder))
    return entry

# Main UI layout for sensor selection
tk.Label(root, text="Choose Sensor Type").pack()

tk.Button(root, text="Temperature", command=lambda: select_sensor("Temperature")).pack(pady=10)
tk.Button(root, text="Humidity", command=lambda: select_sensor("Humidity")).pack(pady=10)
tk.Button(root, text="Sonar", command=lambda: select_sensor("Sonar")).pack(pady=10)

root.mainloop()
