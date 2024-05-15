import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import primer3


# 检查引物序列中是否存在连续三次的二碱基重复
def has_three_repeated_dinucleotides(sequence):
    for i in range(len(sequence) - 5):
        dinucleotide = sequence[i:i + 2]
        if sequence[i + 2:i + 4] == dinucleotide and sequence[i + 4:i + 6] == dinucleotide:
            return True
    return False


def design_primers(sequence, primer_max_poly_x, primer_opt_size, product_size_min, product_size_max):
    seq_args = {
        'SEQUENCE_ID': 'example',
        'SEQUENCE_TEMPLATE': sequence
    }

    global_args = {
        'PRIMER_OPT_SIZE': primer_opt_size,
        'PRIMER_PICK_INTERNAL_OLIGO': 0,
        'PRIMER_INTERNAL_OPT_SIZE': 20,
        'PRIMER_INTERNAL_MIN_SIZE': 18,
        'PRIMER_INTERNAL_MAX_SIZE': 25,
        'PRIMER_INTERNAL_OPT_TM': 60.0,
        'PRIMER_INTERNAL_MIN_TM': 57.0,
        'PRIMER_INTERNAL_MAX_TM': 63.0,
        'PRIMER_INTERNAL_MAX_SELF_END': 8,
        'PRIMER_MIN_SIZE': 18,
        'PRIMER_MAX_SIZE': 25,
        'PRIMER_OPT_TM': 60.0,
        'PRIMER_MIN_TM': 57.0,
        'PRIMER_MAX_TM': 63.0,
        'PRIMER_MAX_POLY_X': primer_max_poly_x,
        'PRIMER_SALT_MONOVALENT': 50.0,
        'PRIMER_DNA_CONC': 50.0,
        'PRIMER_PRODUCT_SIZE_RANGE': [[product_size_min, product_size_max]]
    }

    primer_results = primer3.bindings.design_primers(seq_args, global_args)

    if primer_results['PRIMER_PAIR_NUM_RETURNED'] > 0:
        valid_primers = []
        for i in range(primer_results['PRIMER_PAIR_NUM_RETURNED']):
            left_primer = primer_results[f'PRIMER_LEFT_{i}_SEQUENCE']
            right_primer = primer_results[f'PRIMER_RIGHT_{i}_SEQUENCE']
            internal_oligo = primer_results.get(f'PRIMER_INTERNAL_{i}_SEQUENCE', None)
            left_primer_tm = primer_results[f'PRIMER_LEFT_{i}_TM']
            right_primer_tm = primer_results[f'PRIMER_RIGHT_{i}_TM']
            internal_oligo_tm = primer_results.get(f'PRIMER_INTERNAL_{i}_TM', None)
            product_size = primer_results[f'PRIMER_PAIR_{i}_PRODUCT_SIZE']

            if (not has_three_repeated_dinucleotides(left_primer) and
                    not has_three_repeated_dinucleotides(right_primer) and
                    (internal_oligo is None or not has_three_repeated_dinucleotides(internal_oligo))):
                valid_primers.append({
                    'left_primer': left_primer,
                    'right_primer': right_primer,
                    'internal_oligo': internal_oligo,
                    'left_primer_tm': left_primer_tm,
                    'right_primer_tm': right_primer_tm,
                    'internal_oligo_tm': internal_oligo_tm,
                    'product_size': product_size
                })

        return valid_primers
    else:
        return None


def on_submit():
    sequence = sequence_entry.get("1.0", "end-1c")
    try:
        primer_max_poly_x = int(primer_max_poly_x_entry.get())
        primer_opt_size = int(primer_opt_size_entry.get())
        product_size_min = int(product_size_min_entry.get())
        product_size_max = int(product_size_max_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for PRIMER_MAX_POLY_X, PRIMER_OPT_SIZE, PRODUCT_SIZE_MIN, and PRODUCT_SIZE_MAX.")
        return

    if not sequence:
        messagebox.showerror("Error", "Please enter a sequence.")
        return

    valid_primers = design_primers(sequence, primer_max_poly_x, primer_opt_size, product_size_min, product_size_max)
    if valid_primers:
        result_box.config(state=tk.NORMAL)
        result_box.delete("1.0", tk.END)
        for i, primer in enumerate(valid_primers):
            left_primer = primer["left_primer"]
            right_primer = primer["right_primer"]
            product_size = primer["product_size"]

            left_start = sequence.find(left_primer)
            right_start = sequence.find(right_primer)
            left_end = left_start + len(left_primer)
            right_end = right_start + len(right_primer)

            result_text = f'Left Primer {i + 1}: {left_primer} (Tm: {primer["left_primer_tm"]})\n'
            result_text += f'Right Primer {i + 1}: {right_primer} (Tm: {primer["right_primer_tm"]})\n'
            result_text += f'Product Size {i + 1}: {product_size}\n\n'

            result_box.insert(tk.END, result_text)

            create_highlight(result_box, left_start, left_end, right_start, right_end)

        result_box.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("No Primers", "No valid primers found.")


def create_highlight(result_box, left_start, left_end, right_start, right_end):
    def select(event):
        sequence_entry.tag_add("highlight", f"1.0+{left_start}c", f"1.0+{left_end}c")
        sequence_entry.tag_add("highlight", f"1.0+{right_start}c", f"1.0+{right_end}c")
        sequence_entry.tag_config("highlight", background="yellow")

    def unselect(event):
        sequence_entry.tag_remove("highlight", "1.0", "end")

    result_box.bind("<ButtonPress-1>", select)
    result_box.bind("<ButtonRelease-1>", unselect)


def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = tk.Label(tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1)
    label.pack()
    tooltip.withdraw()

    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 30
        y += widget.winfo_rooty() + 30
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


app = tk.Tk()
app.title("Primer Design Tool")

# 设置背景颜色
background_color = "#333333"  # 从你提供的第二张图片中提取的颜色
app.configure(bg=background_color)

# 添加九州大学的logo并调整大小（保持比例）
image_path = "mnt/data/image.png"
image = Image.open(image_path)
# 调整大小但保持比例
basewidth = 300  # 增大宽度以放大图片
wpercent = (basewidth / float(image.size[0]))
hsize = int((float(image.size[1]) * float(wpercent)))
image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(image)
logo_label = tk.Label(app, image=logo, bg=background_color)
logo_label.pack(pady=10)

# 界面布局
frame = tk.Frame(app, bg=background_color)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Enter Sequence:", bg=background_color, fg="white").grid(row=0, column=0, columnspan=2, padx=5,
                                                                              pady=5)

sequence_entry = tk.Text(frame, height=10, width=80)
sequence_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

tk.Label(frame, text="PRIMER_MAX_POLY_X:", bg=background_color, fg="white").grid(row=2, column=0, padx=5, pady=5,
                                                                                 sticky='w')
primer_max_poly_x_entry = tk.Entry(frame)
primer_max_poly_x_entry.insert(0, "2")  # 设置默认值
primer_max_poly_x_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

create_tooltip(primer_max_poly_x_entry, "Maximum allowable poly-x sequence (e.g., AAA) in any primer")

tk.Label(frame, text="PRIMER_OPT_SIZE:", bg=background_color, fg="white").grid(row=3, column=0, padx=5, pady=5,
                                                                               sticky='w')
primer_opt_size_entry = tk.Entry(frame)
primer_opt_size_entry.insert(0, "20")  # 设置默认值
primer_opt_size_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

create_tooltip(primer_opt_size_entry, "Optimum size of the primer")

# 添加输入框用于PRIMER_PRODUCT_SIZE_RANGE的上界和下界
tk.Label(frame, text="PRODUCT_SIZE_MIN:", bg=background_color, fg="white").grid(row=4, column=0, padx=5, pady=5,
                                                                               sticky='w')
product_size_min_entry = tk.Entry(frame)
product_size_min_entry.insert(0, "100")  # 设置默认值
product_size_min_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

create_tooltip(product_size_min_entry, "Minimum product size")

tk.Label(frame, text="PRODUCT_SIZE_MAX:", bg=background_color, fg="white").grid(row=5, column=0, padx=5, pady=5,
                                                                               sticky='w')
product_size_max_entry = tk.Entry(frame)
product_size_max_entry.insert(0, "300")  # 设置默认值
product_size_max_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

create_tooltip(product_size_max_entry, "Maximum product size")

submit_button = tk.Button(frame, text="Submit", command=on_submit, bg="white")
submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

result_box = tk.Text(frame, height=20, width=80, state=tk.DISABLED)
result_box.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# 添加作者名字和版本号
tk.Label(app, text="Author: yxy, Version: 1.0", bg=background_color, fg="white").pack(pady=5)

app.mainloop()
