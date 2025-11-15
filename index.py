import random
import tkinter as tk
import time

# Pixel fire generator settings
WIDTH = 48
HEIGHT = 28
DELAY = 100 # Delay in milliseconds between canvas updates (animation speed)
RESET_INTERVAL = 3000 # Time in milliseconds before the fire resets completely

PALETTE_COLORS = [
    "#0a0a0a",  # dark background
    "#b40000",  # deep red
    "#ff5000",  # orange red
    "#ff8c00",  # flame orange
    "#ffc832",  # yellow
    "#ffffff"   # white hot
]
PALETTE_RGB = [
    (10, 10, 10),
    (180, 0, 0),
    (255, 80, 0),
    (255, 140, 0),
    (255, 200, 50),
    (255, 255, 255)
]

#/

class FireSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Fire Simulation")
        self.canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE, bg=PALETTE_COLORS[0])
        self.canvas.pack()
        self.fire_data = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.rectangles = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

        self.create_canvas_rectangles()
        self.last_reset_time = time.time()
        self.update_fire()

    def create_canvas_rectangles(self):
        """Pre-create all canvas items for faster updates."""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.rectangles[y][x] = self.canvas.create_rectangle(
                    x * SCALE, y * SCALE,
                    (x + 1) * SCALE, (y + 1) * SCALE,
                    outline="", fill=PALETTE_COLORS[0]
                )

    def seed_fire(self):
        """Seed the bottom few rows with heat values."""
        for y in range(HEIGHT - 6, HEIGHT):
            for x in range(WIDTH):
                # Seed with a heat value from 1 to 5
                self.fire_data[y][x] = random.randint(1, 5)

    def calculate_fire_frame(self):
        """Calculate the next frame of the fire simulation."""
        for y in range(HEIGHT - 1): # Stop one row early to prevent index error
            for x in range(WIDTH):
                # Simulate the heat rising and dissipating slightly
                # This logic mimics the original code's pixel shifting
                source_y = min(HEIGHT - 1, y + random.randint(1, 3))
                source_x = min(WIDTH - 1, max(0, x + random.randint(-1, 1)))

                # Get the heat value from the source pixel below/around
                heat_from_below = self.fire_data[source_y][source_x]
                
                # Apply a slight cooling effect as it rises
                new_heat = max(0, heat_from_below - (random.randint(0, 1) if y < HEIGHT - 6 else 0))
                self.fire_data[y][x] = new_heat

    def draw_fire(self):
        """Update the tkinter canvas with the new fire data."""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                heat = self.fire_data[y][x]
                color = PALETTE_COLORS[min(heat, len(PALETTE_COLORS) - 1)]
                self.canvas.itemconfig(self.rectangles[y][x], fill=color)

    def update_fire(self):
        """Main update loop for animation and resetting."""
        current_time = time.time()
        if (current_time - self.last_reset_time) * 1000 > RESET_INTERVAL:
            print("Resetting fire simulation...")
            self.fire_data = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)] # Clear data
            self.seed_fire()
            self.last_reset_time = current_time

        self.calculate_fire_frame()
        self.draw_fire()
        # Schedule the next update
        self.root.after(DELAY, self.update_fire)

if __name__ == "__main__":
    root = tk.Tk()
    sim = FireSimulation(root)
    sim.seed_fire()
    root.mainloop()
