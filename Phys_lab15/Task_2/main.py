import tkinter as tk
from tkinter import ttk, messagebox

class CondenserParametersApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Расчет параметров")
        self.geometry("700x550")
        self.configure(bg="#e5e5ea")

        self.setup_ui()

    def setup_ui(self):
        self.create_title_bar()
        self.build_input_form()
        self.add_action_buttons()
        self.display_result_area()

    def create_title_bar(self):
        title = tk.Label(self, text="Расчет параметров плоского конденсатора",
                         font=("Helvetica", 20, "bold"), bg="#e5e5ea", fg="#333333")
        title.pack(pady=(25, 15))

    def build_input_form(self):
        form_container = tk.Frame(self, bg="#ffffff", highlightthickness=1, highlightbackground="#d3d3d3")
        form_container.pack(padx=30, pady=15)

        field_data = [
            {"label": "Напряженность (В)", "var": tk.StringVar()},
            {"label": "Расстояние между пластинами (м)", "var": tk.StringVar()},
            {"label": "Диэлектрическая постоянная", "var": tk.StringVar()},
            {"label": "Площадь пластин (м²)", "var": tk.StringVar()}
        ]

        for idx, field in enumerate(field_data):
            label = tk.Label(form_container, text=field["label"], font=("Arial", 12), bg="#ffffff")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(form_container, textvariable=field["var"], font=("Arial", 12), width=22)
            entry.grid(row=idx, column=1, padx=10, pady=5)

        power_source_label = tk.Label(form_container, text="Подключен к источнику питания:",
                                      font=("Arial", 12), bg="#ffffff")
        power_source_label.grid(row=len(field_data), column=0, padx=10, pady=5, sticky="w")

        self.power_status = ttk.Combobox(form_container, font=("Arial", 12), width=20)
        self.power_status['values'] = ["Да", "Нет"]
        self.power_status.set("Yes")
        self.power_status.grid(row=len(field_data), column=1, padx=10, pady=5)

        self.input_vars = [field["var"] for field in field_data]

    def add_action_buttons(self):
        button_panel = tk.Frame(self, bg="#e5e5ea")
        button_panel.pack(pady=(15, 20))

        calc_button = tk.Button(button_panel, text="Вывести результат",
                                command=self.compute_condenser_params,
                                font=("Arial", 14, "bold"), bg="#3498db", fg="#ffffff",
                                activebackground="#2980b9", activeforeground="#ffffff",
                                padx=15, pady=7)
        calc_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(button_panel, text="Очистить",
                                 command=self.reset_fields,
                                 font=("Arial", 14), bg="#e74c3c", fg="#ffffff",
                                 activebackground="#c0392b", activeforeground="#ffffff",
                                 padx=15, pady=7)
        reset_button.pack(side=tk.LEFT, padx=10)

    def display_result_area(self):
        result_box = tk.Frame(self, bg="#ffffff", highlightthickness=1, highlightbackground="#d3d3d3")
        result_box.pack(padx=30, pady=15, fill="both", expand=True)

        self.result_display = tk.Text(result_box, font=("Courier New", 12), bg="#ffffff", wrap=tk.WORD)
        self.result_display.pack(padx=15, pady=15, fill="both", expand=True)

    def compute_condenser_params(self):
        try:
            voltage = float(self.input_vars[0].get())
            plate_distance = float(self.input_vars[1].get())
            dielectric_const = float(self.input_vars[2].get())
            plate_area = float(self.input_vars[3].get())
            connected_to_power = self.power_status.get() == "Yes"

            if plate_distance <= 0 or dielectric_const <= 0 or plate_area <= 0:
                raise ValueError("Введите валидные данные")

            epsilon_zero = 8.85e-12
            electric_field_strength = voltage / plate_distance
            capacitance = dielectric_const * epsilon_zero * plate_area / plate_distance

            charge = capacitance * voltage

            result_text = (
                f"Напряженность электрического поля: {electric_field_strength:.2e} В/м\n"
                f"Емкость: {capacitance:.2e} F\n"
                f"Заряд: {charge:.2e} C"
            )
            self.result_display.delete('1.0', tk.END)
            self.result_display.insert(tk.END, result_text)
        except ValueError as e:
            messagebox.showwarning("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def reset_fields(self):
        for var in self.input_vars:
            var.set("")
        self.power_status.set("Yes")
        self.result_display.delete('1.0', tk.END)

if __name__ == "__main__":
    app = CondenserParametersApp()
    app.mainloop()