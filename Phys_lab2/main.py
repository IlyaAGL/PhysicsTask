import tkinter as tk
import graphics


def submit_number():
    angle = entryAngle.get()
    speed = entrySpeed.get()
    height = entryHeight.get()

    if angle.isdigit() and speed.isdigit() and height.isdigit():
        if int(angle) < 0 or int(speed) < 0 or int(height) < 0:
            result_label.config(text='Please enter a valid number')
        else:
            graphics.trajectory_parameters(int(height), int(speed), int(angle))
    else:
        result_label.config(text='Please enter a valid number')


root = tk.Tk()
root.title('Number Input')
root.geometry('300x200')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

labelAngle = tk.Label(root, text='Angle (deg):')
labelAngle.grid(row=0, column=0, padx=10, pady=5, sticky='e')
entryAngle = tk.Entry(root)
entryAngle.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

labelSpeed = tk.Label(root, text='Speed (m/s):')
labelSpeed.grid(row=1, column=0, padx=10, pady=5, sticky='e')
entrySpeed = tk.Entry(root)
entrySpeed.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

labelHeight = tk.Label(root, text='Height (m):')
labelHeight.grid(row=2, column=0, padx=10, pady=5, sticky='e')
entryHeight = tk.Entry(root)
entryHeight.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

submit_button = tk.Button(root, text='Submit', command=submit_number)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text='')
result_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
