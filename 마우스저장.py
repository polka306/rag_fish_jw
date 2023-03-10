import tkinter as tk
import win32api
import win32con
import win32gui
import csv

points = []

def get_mouse_point():
    return win32api.GetCursorPos()

def get_window_point():
    window_name = "LDPlayer"
    hWnd = win32gui.FindWindow(None, window_name)
    if hWnd:
        return win32gui.GetWindowRect(hWnd)[:2]
    else:
        print("Window not found")
        return None
    
def get_window_point():
    window_name = "LDPlayer"
    hWnd = win32gui.FindWindow(None, window_name)
    if hWnd:
        return win32gui.GetWindowRect(hWnd)[:2]
    else:
        print("Window not found")
        return None

def save_button_clicked():
    with open('mouse_point.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(points)

def update_text():
    window_name = "LDPlayer"
    hWnd = win32gui.FindWindow(None, window_name)
    mouse_point = get_mouse_point()
    window_point = get_window_point()
    left, top, right, bottom = win32gui.GetWindowRect(hWnd)
    width, height = right - left, bottom - top

    if window_point is not None:
        rel_mouse_point = (mouse_point[0] - window_point[0], mouse_point[1] - window_point[1])
        output_text.delete(1.0, tk.END) # Clear previous text
        output_text.insert(tk.END, f"Mouse point: {mouse_point}\n")
        output_text.insert(tk.END, f"Relative mouse point: {rel_mouse_point}\n")

        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            rel_x, rel_y = (mouse_point[0] - left) / width * 100, (mouse_point[1] - top) / height * 100
            all_mouse_point = (mouse_point[0], mouse_point[1],mouse_point[0] - window_point[0], mouse_point[1] - window_point[1],rel_x,rel_y)
            points.append(all_mouse_point)
            output_text1.delete(1.0, tk.END) # Clear previous text
            output_text1.insert(tk.END, f"Left mouse button clicked. Points: {points}\n")

    output_text.after(50, update_text) # Update every 50 milliseconds

# Create GUI
root = tk.Tk()
root.geometry("400x300")
root.title("Mouse Position Tracker")

# Create text widget to display output
#text = tk.Text(root, font=("Courier", 12))
#text.pack(fill=tk.BOTH, expand=True)

output_text=tk.Text(root, width=50, height=5)
output_text.grid(row=0,column=0,columnspan=4)

output_text1=tk.Text(root, width=50, height=15)
output_text1.grid(row=1,column=0,columnspan=4)

stop_button = tk.Button(root, text="저장", command=save_button_clicked)
stop_button.grid(row=0,column=5,rowspan=2,sticky=tk.W+tk.E+tk.N+tk.S)

# Call update_text function to start updating the text widget
update_text()

root.mainloop()