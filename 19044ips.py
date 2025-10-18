from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

root = Tk()
root.title("Smart Image Rotator")
root.geometry("850x720")

img = None
display_img = None
img_label = None
angle = 0
zoom_level = 1.0
dark_mode = True
file_path = None

style = ttk.Style()

def apply_theme():
    if dark_mode:
        root.config(bg="#121212")
        controls_frame.config(bg="#121212")
        bottom_frame.config(bg="#121212")
        angle_label.config(bg="#121212", fg="white")
        style.theme_use("clam")
        style.configure("TScale", background="#121212", troughcolor="#333", bordercolor="#444")
        style.configure("TButton", background="#333", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#555")])
        theme_btn.config(text="☀ Light Mode")
    else:
        root.config(bg="white")
        controls_frame.config(bg="white")
        bottom_frame.config(bg="white")
        angle_label.config(bg="white", fg="black")
        style.theme_use("clam")
        style.configure("TScale", background="white", troughcolor="#ddd", bordercolor="#ccc")
        style.configure("TButton", background="#f0f0f0", foreground="black", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#ddd")])
        theme_btn.config(text="🌙 Dark Mode")

def upload_image():
    global img, file_path, zoom_level, angle
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        zoom_level = 1.0
        angle = 0
        display_image(img)

def display_image(image):
    global display_img, img_label
    width, height = image.size
    image = image.resize((int(width * zoom_level), int(height * zoom_level)))
    display_img = ImageTk.PhotoImage(image)
    if img_label is None:
        img_label = Label(root, image=display_img, bg=root["bg"])
        img_label.pack(pady=20)
    else:
        img_label.config(image=display_img)
        img_label.image = display_img

def rotate_90():
    global img, angle
    if img:
        angle = (angle + 90) % 360
        rotated = img.rotate(-angle, expand=True)
        display_image(rotated)
        angle_slider.set(angle)
        update_angle_label(angle)

def custom_rotate(value):
    global img
    if img:
        rotated = img.rotate(-float(value), expand=True)
        display_image(rotated)
        update_angle_label(float(value))

def update_angle_label(value):
    angle_label.config(text=f"Angle: {int(float(value))}°")

def save_image():
    global img, angle
    if img:
        rotated = img.rotate(-angle, expand=True)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
        )
        if save_path:
            rotated.save(save_path)
            messagebox.showinfo("Saved", f"Image saved successfully at:\n{save_path}")

def zoom_in():
    global zoom_level
    if img and zoom_level < 3:
        zoom_level += 0.1
        rotated = img.rotate(-angle, expand=True)
        display_image(rotated)

def zoom_out():
    global zoom_level
    if img and zoom_level > 0.3:
        zoom_level -= 0.1
        rotated = img.rotate(-angle, expand=True)
        display_image(rotated)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

controls_frame = Frame(root, bg="#121212")
controls_frame.pack(pady=10)

upload_btn = ttk.Button(controls_frame, text="📂 Upload", command=upload_image, width=14)
rotate_btn = ttk.Button(controls_frame, text="🔄 Rotate 90°", command=rotate_90, width=14)
save_btn = ttk.Button(controls_frame, text="💾 Save", command=save_image, width=14)
zoom_in_btn = ttk.Button(controls_frame, text="🔍 Zoom In", command=zoom_in, width=14)
zoom_out_btn = ttk.Button(controls_frame, text="🔎 Zoom Out", command=zoom_out, width=14)
theme_btn = ttk.Button(controls_frame, text="☀ Light Mode", command=toggle_theme, width=14)

upload_btn.grid(row=0, column=0, padx=6, pady=5)
rotate_btn.grid(row=0, column=1, padx=6, pady=5)
save_btn.grid(row=0, column=2, padx=6, pady=5)
zoom_in_btn.grid(row=0, column=3, padx=6, pady=5)
zoom_out_btn.grid(row=0, column=4, padx=6, pady=5)
theme_btn.grid(row=0, column=5, padx=6, pady=5)


bottom_frame = Frame(root, bg="#121212")
bottom_frame.pack(fill="x", padx=50, pady=10)

angle_label = Label(bottom_frame, text="Angle: 0°", font=("Segoe UI", 11, "bold"), bg="#121212", fg="white")
angle_label.pack(pady=5)

angle_slider = ttk.Scale(bottom_frame, from_=0, to=360, orient=HORIZONTAL, command=custom_rotate)
angle_slider.pack(fill="x", pady=5)

apply_theme()

root.mainloop()
