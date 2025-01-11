import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import main
task_thread = None
is_task_running = False

def import_file():
    file_path = filedialog.askopenfilename(title="Chọn tệp", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        file_label.config(text=f"Tệp đã chọn: {file_path}")


def run_task(channel, subchannel, account, password, file_path, time_step):
    global is_task_running, task_thread
    is_task_running = True
    try:
        while not main.should_stop:
            main.run_discord_bot(channel, subchannel, account, password, file_path, time_step)
            if main.should_stop:
                break
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    finally:
        is_task_running = False
        task_thread = None
        messagebox.showinfo("Thông báo", "Bot đã chạy xong.")
        submit_button.config(state="normal")


def submit():
    channel = channel_entry.get()
    subchannel = subchannel_entry.get()
    account = account_entry.get()
    password = password_entry.get()
    time_step = time_entry.get()
    file_path = file_label.cget('text')[13:]
    file_path = file_path.replace('/','\\')
    main.should_stop = False

    # Kiểm tra các trường đã được điền đầy đủ chưa
    if not (channel and subchannel and account and password and file_path):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ tất cả các trường.")
        return

    if is_task_running:
        messagebox.showwarning("Cảnh báo", "Một tác vụ đã đang chạy. Vui lòng đợi trước khi gửi yêu cầu mới.")
        return

    if time_step.isdigit():
        time_step = int(time_step)
    else:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho time step.")
        return

    task_thread = threading.Thread(target=run_task, args=(channel, subchannel, account, password, file_path, time_step))
    task_thread.start()

    submit_button.config(state="disabled")

    # In thông tin lên console
    print(f"Channel: {channel}")
    print(f"Subchannel: {subchannel}")
    print(f"Account: {account}")
    print(f"Password: {password}")
    print(f"File path: {file_label.cget('text')[13:]}")

    # Thông báo thành công
    messagebox.showinfo("Thông báo", "Dữ liệu đã được nhập thành công.")


def cancel_task():
    global task_thread, is_task_running
    if is_task_running:
        main.should_stop = True
        if task_thread is not None:
            task_thread.join()
        task_thread = None
        messagebox.showinfo("Thông báo", "Tác vụ đã bị hủy.")
    else:
        messagebox.showinfo("Thông báo", "Không có tác vụ nào đang chạy.")

    submit_button.config(state="normal")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("tools discord")

# Tạo các nhãn và trường nhập liệu
tk.Label(root, text="CHANNEL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
channel_entry = tk.Entry(root, width=30)
channel_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="SUBCHANNEL:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
subchannel_entry = tk.Entry(root, width=30)
subchannel_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="ACCOUNT:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
account_entry = tk.Entry(root, width=30)
account_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="PASSWORD:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, width=30, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="time step:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
time_entry = tk.Entry(root, width=30)
time_entry.grid(row=5, column=1, padx=10, pady=5)

# Tạo nút để chọn tệp
file_button = tk.Button(root, text="Import File", command=import_file)
file_button.grid(row=4, column=0, padx=10, pady=5)

# Label để hiển thị tệp đã chọn
file_label = tk.Label(root, text="Tệp chưa chọn")
file_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Tạo nút Submit
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

# Tạo nút Hủy
cancel_button = tk.Button(root, text="Cancel", command=cancel_task)
cancel_button.grid(row=6, column=1, columnspan=2, pady=10)

# Chạy ứng dụng
root.mainloop()
