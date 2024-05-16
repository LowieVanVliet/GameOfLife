import tkinter as tk
from tkinter import messagebox

class ClickableGrid(tk.Frame):
    def __init__(self, parent, rows, columns, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.rows = rows
        self.columns = columns
        self.cells = [[None]*columns for _ in range(rows)]
        self.elapsed_time = 0  # Track elapsed time
        self.started = False  # Track if the updates have started
        self.previous_colors = None  # Track previous grid state
        self.create_grid()

    def create_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        total_width = self.winfo_reqwidth()
        total_height = self.winfo_reqheight()
        cell_width = total_width // self.columns
        cell_height = total_height // self.rows
        
        for row_index in range(self.rows):
            self.grid_rowconfigure(row_index, weight=1, minsize=cell_height)
            for col_index in range(self.columns):
                self.grid_columnconfigure(col_index, weight=1, minsize=cell_width)
                cell = tk.Frame(self, width=cell_width, height=cell_height, 
                                borderwidth=1, relief="solid", bg="white")
                cell.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")
                cell.bind("<Button-1>", lambda event, row=row_index, col=col_index: self.on_click(row, col))
                self.cells[row_index][col_index] = cell

    def on_click(self, row, col):
        cell = self.cells[row][col]
        current_bg = cell.cget("bg")
        new_bg = "blue" if current_bg == "white" else "white"
        cell.configure(bg=new_bg)

    def all_cells_white(self):
        for row_index in range(self.rows):
            for col_index in range(self.columns):
                if self.cells[row_index][col_index].cget("bg") == "blue":
                    return False
        return True

    def neighbour_count(self, current_colors, row, col):
        blue_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the current cell
                if 0 <= row + i < self.rows and 0 <= col + j < self.columns:
                    if current_colors[row + i][col + j] == "blue":
                        blue_count += 1
        return blue_count


    def start_updates(self):
        if not self.started:
            self.started = True
            self.update_colors()

    def stop_updates(self):
        self.started = False

    def update_colors(self):
        if self.started:
            self.elapsed_time += 1  # Increment elapsed time
            
            # Create a copy of the current grid's colors
            current_colors = [[self.cells[row][col].cget("bg") for col in range(self.columns)] for row in range(self.rows)]

            if self.all_cells_white():
                print("All cells are white. Stopping updates.")
                self.show_popup_message("Update Stopped", "All cells are white.")  # Show pop-up message
                self.started = False
                return  # Stop updating if all cells are white

            # Check if the current state is different from the previous state
            if current_colors != self.previous_colors:
                self.previous_colors = current_colors
            else:
                print("Grid state unchanged. Stopping updates.")
                self.show_popup_message("Update Stopped", "Grid state unchanged.")  # Show pop-up message
                self.started = False
                return  # Stop updating if grid state has not changed

            # Iterate over each cell to update its color based on the current state of its neighbors
            for row_index in range(self.rows):
                for col_index in range(self.columns):
                    current_color = current_colors[row_index][col_index]
                    if current_color == "blue":
                        if self.neighbour_count(current_colors, row_index, col_index) < 2 or self.neighbour_count(current_colors, row_index, col_index) > 3:
                            next_color = "white"
                        else:
                            next_color = "blue"
                    else:
                        if self.neighbour_count(current_colors, row_index, col_index) == 3:
                            next_color = "blue"
                        else:
                            next_color = "white"
                    
                    self.cells[row_index][col_index].configure(bg=next_color)

            self.after(250, self.update_colors) 


    def show_popup_message(self, title, message):
        messagebox.showinfo(title, message)





    def single_update(self):
        print("Single update triggered.")  # Debug print
        self.started = True 
        self.update_colors()  # Call update_colors method directly to perform a single update
        self.started = False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")  # Set initial size for the window
    grid = ClickableGrid(root, rows=40, columns=40)
    grid.pack(fill="both", expand=True)
    
    # Create a button to start updates
    start_button = tk.Button(root, text="Start Updates", command=grid.start_updates)
    start_button.pack(side="left")

    # Create a button to stop updates
    stop_button = tk.Button(root, text="Stop Updates", command=grid.stop_updates)
    stop_button.pack(side="left")

    # Create a button to trigger a single update
    update_button = tk.Button(root, text="Single Update", command=grid.single_update)
    update_button.pack(side="left")

    root.mainloop()
