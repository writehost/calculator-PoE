import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ipaddress import ip_network
import random
import string
from datetime import datetime

def poe_distance_calculator(voltage, current, cable_type):
    max_power = 15.4
    power = voltage * current
    distance = ((power / max_power) ** 0.5) * 100
    return distance

def calculate_distance():
    try:
        voltage = float(entry_voltage.get())
        current = float(entry_current.get())
        cable_type = combo_cable_type.get().lower()
        poe_distance = poe_distance_calculator(voltage, current, cable_type)
        result_label.config(text=f"Расстояние работы PoE: {poe_distance:.2f} метров")
    except ValueError:
        result_label.config(text="Введите корректные значения.")

def calculator_button_click(value):
    current_expression = entry_calculator.get()
    current_expression += str(value)
    entry_calculator.delete(0, tk.END)
    entry_calculator.insert(0, current_expression)

def clear_calculator():
    entry_calculator.delete(0, tk.END)

def evaluate_expression():
    try:
        expression = entry_calculator.get()
        result = eval(expression)
        entry_calculator.delete(0, tk.END)
        entry_calculator.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Ошибка", "Некорректное выражение")

def calculate_bandwidth():
    try:
        voltage = float(entry_voltage_bandwidth.get())
        resistance = float(entry_resistance_bandwidth.get())
        bandwidth = voltage / resistance
        result_label_bandwidth.config(text=f"Пропускная способность витой пары: {bandwidth:.2f} Ампер")
    except ValueError:
        result_label_bandwidth.config(text="Введите корректные значения.")

def calculate_internet_speed():
    try:
        current_speed = float(entry_current_speed.get())
        computers = int(entry_computers.get())
        average_speed = current_speed / computers
        result_label_speed.config(text=f"Средняя скорость на пользователя: {average_speed:.2f} Мбит/с")
    except ValueError:
        result_label_speed.config(text="Введите корректные значения.")

def calculate_subnet_ips():
    try:
        network_address = entry_network_address.get()
        subnet_mask = entry_subnet_mask.get()
        network = ip_network(f"{network_address}/{subnet_mask}", strict=False)
        hosts = list(network.hosts())[:1000]  # Ограничение до первых 1000 хостов
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"IP-адреса подсети: {', '.join(map(str, hosts))}")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Введите корректные значения.")

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_passwords(num_passwords, length):
    passwords = [(generate_password(length), datetime.now().strftime("%Y-%m-%d %H:%M:%S")) for _ in range(num_passwords)]
    return passwords

def update_password_list():
    password_length = int(entry_password_length.get())
    num_passwords = int(entry_num_passwords.get())
    passwords = generate_passwords(num_passwords, password_length)

    result_text_passwords.config(state=tk.NORMAL)
    result_text_passwords.delete(1.0, tk.END)

    for password, creation_date in passwords:
        result_text_passwords.insert(tk.END, f"{creation_date}: {password}\n")

    result_text_passwords.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Network Calculators")

# Frame for PoE Distance Calculator
frame_poe = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_poe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
label_voltage = ttk.Label(frame_poe, text="Напряжение источника питания (в вольтах):")
label_voltage.grid(column=0, row=0, sticky=tk.W)
entry_voltage = ttk.Entry(frame_poe)
entry_voltage.grid(column=1, row=0, sticky=tk.W)
label_current = ttk.Label(frame_poe, text="Ток (в амперах):")
label_current.grid(column=0, row=1, sticky=tk.W)
entry_current = ttk.Entry(frame_poe)
entry_current.grid(column=1, row=1, sticky=tk.W)
label_cable_type = ttk.Label(frame_poe, text="Тип кабеля:")
label_cable_type.grid(column=0, row=2, sticky=tk.W)
combo_cable_type = ttk.Combobox(frame_poe, values=["Витая пара"])
combo_cable_type.grid(column=1, row=2, sticky=tk.W)
combo_cable_type.set("Витая пара")
calculate_button = ttk.Button(frame_poe, text="Рассчитать", command=calculate_distance)
calculate_button.grid(column=0, row=3, columnspan=2, pady=10)
result_label = ttk.Label(frame_poe, text="")
result_label.grid(column=0, row=4, columnspan=2)

# Frame for Simple Calculator
frame_calculator = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_calculator.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
entry_calculator = ttk.Entry(frame_calculator, width=15, font=("Arial", 14))
entry_calculator.grid(column=0, row=0, columnspan=4)
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]
row_val = 1
col_val = 0
for button in buttons:
    ttk.Button(frame_calculator, text=button, command=lambda b=button: calculator_button_click(b)).grid(row=row_val, column=col_val, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1
ttk.Button(frame_calculator, text='C', command=clear_calculator).grid(row=row_val, column=col_val, pady=5)
ttk.Button(frame_calculator, text='AC', command=lambda: entry_calculator.delete(0, tk.END)).grid(row=row_val, column=col_val+1, pady=5)
ttk.Button(frame_calculator, text='=', command=evaluate_expression).grid(row=row_val, column=col_val+2, pady=5)

# Frame for Bandwidth Calculator
frame_bandwidth = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_bandwidth.grid(column=2, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
label_voltage_bandwidth = ttk.Label(frame_bandwidth, text="Напряжение (в вольтах):")
label_voltage_bandwidth.grid(column=0, row=0, sticky=tk.W)
entry_voltage_bandwidth = ttk.Entry(frame_bandwidth)
entry_voltage_bandwidth.grid(column=1, row=0, sticky=tk.W)
label_resistance_bandwidth = ttk.Label(frame_bandwidth, text="Сопротивление (в омах):")
label_resistance_bandwidth.grid(column=0, row=1, sticky=tk.W)
entry_resistance_bandwidth = ttk.Entry(frame_bandwidth)
entry_resistance_bandwidth.grid(column=1, row=1, sticky=tk.W)
calculate_button_bandwidth = ttk.Button(frame_bandwidth, text="Рассчитать", command=calculate_bandwidth)
calculate_button_bandwidth.grid(column=0, row=2, columnspan=2, pady=10)
result_label_bandwidth = ttk.Label(frame_bandwidth, text="")
result_label_bandwidth.grid(column=0, row=3, columnspan=2)

# Frame for Internet Speed Calculator
frame_speed = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_speed.grid(column=3, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
label_current_speed = ttk.Label(frame_speed, text="Текущая скорость интернета (в Мбит/с):")
label_current_speed.grid(column=0, row=0, sticky=tk.W)
entry_current_speed = ttk.Entry(frame_speed)
entry_current_speed.grid(column=1, row=0, sticky=tk.W)
label_computers = ttk.Label(frame_speed, text="Количество компьютеров:")
label_computers.grid(column=0, row=1, sticky=tk.W)
entry_computers = ttk.Entry(frame_speed)
entry_computers.grid(column=1, row=1, sticky=tk.W)
calculate_button_speed = ttk.Button(frame_speed, text="Рассчитать", command=calculate_internet_speed)
calculate_button_speed.grid(column=0, row=2, columnspan=2, pady=10)
result_label_speed = ttk.Label(frame_speed, text="")
result_label_speed.grid(column=0, row=3, columnspan=2)

# Frame for IP Subnet Calculator
frame_subnet_ips = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_subnet_ips.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
label_network_address = ttk.Label(frame_subnet_ips, text="Сетевой адрес:")
label_network_address.grid(column=0, row=0, sticky=tk.W)
entry_network_address = ttk.Entry(frame_subnet_ips)
entry_network_address.grid(column=1, row=0, sticky=tk.W)
label_subnet_mask = ttk.Label(frame_subnet_ips, text="Маска подсети:")
label_subnet_mask.grid(column=0, row=1, sticky=tk.W)
entry_subnet_mask = ttk.Entry(frame_subnet_ips)
entry_subnet_mask.grid(column=1, row=1, sticky=tk.W)
calculate_button_subnet_ips = ttk.Button(frame_subnet_ips, text="Рассчитать", command=calculate_subnet_ips)
calculate_button_subnet_ips.grid(column=0, row=2, columnspan=2, pady=10)

# Scrollable Text for IP Subnet Results
result_text = scrolledtext.ScrolledText(frame_subnet_ips, width=40, height=5, wrap=tk.WORD)
result_text.grid(column=0, row=3, columnspan=2, pady=10)

# Frame for Password Generator
frame_password_generator = ttk.Frame(root, padding="10", borderwidth=2, relief="ridge")
frame_password_generator.grid(column=1, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
label_password_length = ttk.Label(frame_password_generator, text="Длина пароля:")
label_password_length.grid(column=0, row=0, sticky=tk.W)
entry_password_length = ttk.Entry(frame_password_generator)
entry_password_length.grid(column=1, row=0, sticky=tk.W)
label_num_passwords = ttk.Label(frame_password_generator, text="Количество паролей:")
label_num_passwords.grid(column=0, row=1, sticky=tk.W)
entry_num_passwords = ttk.Entry(frame_password_generator)
entry_num_passwords.grid(column=1, row=1, sticky=tk.W)
calculate_button_passwords = ttk.Button(frame_password_generator, text="Генерировать пароли", command=update_password_list)
calculate_button_passwords.grid(column=0, row=2, columnspan=2, pady=10)

# Scrollable Text for Passwords
result_text_passwords = scrolledtext.ScrolledText(frame_password_generator, width=40, height=5, wrap=tk.WORD)
result_text_passwords.grid(column=0, row=3, columnspan=2, pady=10)
result_text_passwords.config(state=tk.DISABLED)

# Frame для подвала
frame_footer = ttk.Frame(root, padding="10")
frame_footer.grid(column=0, row=2, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

# Надпись в подвале
label_footer = ttk.Label(frame_footer, text="By Nik Sukhotskiy")
label_footer.pack(side=tk.BOTTOM, pady=10)

# Запускаем цикл событий
root.mainloop()
