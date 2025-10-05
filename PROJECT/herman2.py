import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance
import requests
from io import BytesIO
import math
import threading
import os
from datetime import datetime
import time

class ISS_Cupola_Viewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ISS Cupola Earth Viewer - Enhanced Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0a0a")
        self.root.minsize(800, 600)

        # Enhanced window data with ALL properly formatted Google Drive URLs
        self.cupola_windows = {
            "Window 0": [
                "https://drive.google.com/uc?export=download&id=1pfF3bDvlDouq0r6pNnLcXHwcU3piPCru",
                "https://drive.google.com/uc?export=download&id=1K8o7djvEmIBdz4at7iv3Sbs5ukN2wi9L",
                "https://drive.google.com/uc?export=download&id=1apFAc1ye7-2nVnS7tPjc57Rd6qMTMKr8",
                "https://drive.google.com/uc?export=download&id=1qe48ivsfLsvGZi5eE3e0PKcSM9Eu5re7",
                "https://drive.google.com/uc?export=download&id=1d1zD3-mF9c5QLAS0yMK_keb6DXxT_BDn",
            ],
            "Window 1": [
                "https://drive.google.com/uc?export=download&id=1aTPf80gcjwutNh-AelhoARhNGDN3QaKg",
                "https://drive.google.com/uc?export=download&id=15g5dNuz7OGlaE--dEeXTGxjS6AdX25Sg",
                "https://drive.google.com/uc?export=download&id=1wZhf-uknETMyPb4_mgOg9reLVXZtSPC5",
                "https://drive.google.com/uc?export=download&id=1I8GenxSDJ-41NRCuENjXD3mt1i6hMEuy",
                "https://drive.google.com/uc?export=download&id=1A1hjEv5MBOd2yD2OqptSzwr-T_7dn63u",
            ],
            "Window 2": [
                "https://drive.google.com/uc?export=download&id=1aTPf80gcjwutNh-AelhoARhNGDN3QaKg",
                "https://drive.google.com/uc?export=download&id=1Kh1sCO0WF6NkhsLeJB55Pp8c6Oax77VJ",
                "https://drive.google.com/uc?export=download&id=1djwHw8aCj6xUNS4RC6zxXPKhko7KiWAZ",
                "https://drive.google.com/uc?export=download&id=106KpUBeYFBVJmLIWnBfTWCgNxP6w7cne",
                "https://drive.google.com/uc?export=download&id=1sOgvQpjOcxQl_zvaowLW3i3amxlgH0Ts",
            ],
            "Window 3": [
                "https://drive.google.com/uc?export=download&id=1K8o7djvEmIBdz4at7iv3Sbs5ukN2wi9L",
                "https://drive.google.com/uc?export=download&id=12zCqc-y_t9zti6Vz0eZu5awYIEmVq3v9",
                "https://drive.google.com/uc?export=download&id=1x3lqnMhlUQDJeHr3hzuOSXkf-qPfgGC3",
                "https://drive.google.com/uc?export=download&id=1KQL7qKNClmg1edGAkGm5m44g4R0gmDBu",
                "https://drive.google.com/uc?export=download&id=1gG-uj42zOsj-G4L7GTztSBumKKWZ_jLR",
            ],
            "Window 4": [
                "https://drive.google.com/uc?export=download&id=1pfF3bDvlDouq0r6pNnLcXHwcU3piPCru",
                "https://drive.google.com/uc?export=download&id=16ckndM4z3iQ6S9f31kel6j4rBz-GFpJC",
                "https://drive.google.com/uc?export=download&id=1UGHEATWSiyfXiWH-s5_0hD4vSn7U4Z0M",
                "https://drive.google.com/uc?export=download&id=1A5SXNiqOwlzRe18e5MZuYMZtkGcsXIB8",
                "https://drive.google.com/uc?export=download&id=1SqRRYREYPAcIL33r9pbBz9S31JAIXfY-",
            ],
            "Window 5": [
                "https://drive.google.com/uc?export=download&id=1SMqMSQR_enzXFp_mA4CHeqKCZlWhDKaN",
                "https://drive.google.com/uc?export=download&id=1_AM4gbGlZtL_j_MjRqrh0qtTkPQ1kna3",
                "https://drive.google.com/uc?export=download&id=1L8-NEsrqRFgQkncoCHCVCaQW7HhAnc8i",
                "https://drive.google.com/uc?export=download&id=15qcxHZ_hXtoMqEFFRRWD37g092SfFRYA",
            ],
            "Window 6": [
                "https://drive.google.com/uc?export=download&id=1E9-ZsqXMtZL3b_rJa_LOWua2aTKrjf3K",
                "https://drive.google.com/uc?export=download&id=10ILjbLn2cZUtTUwWGbN1IG7Srtv1GoVO",
                "https://drive.google.com/uc?export=download&id=1SJttmNLmfZXE7SbtJ8G4-DqRH8X8Bn-f",
                "https://drive.google.com/uc?export=download&id=1AbwhVL7uEUd9zHhlE3GUeqaG7A9ciYUy",
            ],
        }

        self.preloaded_images = {}
        self.current_window = None
        self.current_index = 0
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rotation_angle = 0
        self.brightness = 1.0
        self.contrast = 1.0
        self.fullscreen_mode = False
        self.loading_progress = 0
        self.total_images = sum(len(urls) for urls in self.cupola_windows.values())
        self.failed_images = 0

        self.setup_ui()
        self.bind_events()
        self.start_preloading()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill="both", expand=True)

        self.setup_toolbar()
        self.content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.content_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_frame, bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.image_frame = tk.Frame(self.content_frame, bg="#0a0a0a")
        self.image_label = tk.Label(self.image_frame, bg="#0a0a0a")
        self.image_label.pack()

        self.controls_frame = tk.Frame(self.image_frame, bg="#0a0a0a")
        self.controls_frame.pack(side="bottom", fill="x", pady=10)

        self.setup_image_controls()
        self.setup_status_bar()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var,
                                            maximum=100, length=400, mode='determinate')

        self.loading_label = tk.Label(self.main_frame, text="Loading ISS Cupola imagery from Google Drive...\nThis may take a moment, please be patient.",
                                      bg="#0a0a0a", fg="white", font=("Arial", 12), justify=tk.CENTER)

        self.loading_details = tk.Label(self.main_frame, text="", bg="#0a0a0a", fg="#888888", font=("Arial", 10), justify=tk.CENTER)

    def setup_toolbar(self):
        self.toolbar = tk.Frame(self.main_frame, bg="#1a1a1a", height=40)
        self.toolbar.pack(side="top", fill="x")

        self.back_button = tk.Button(self.toolbar, text="⬅ Cupola View",
                                    font=("Arial", 10, "bold"), bg="#2a2a2a", fg="white",
                                    relief="flat", pady=5, command=self.show_cupola)
        self.window_info = tk.Label(self.toolbar, text="", bg="#1a1a1a", fg="white", font=("Arial", 10))

        self.prev_btn = tk.Button(self.toolbar, text="◀ Previous", font=("Arial", 10, "bold"),
                                  bg="#2a2a2a", fg="white", relief="flat", command=self.prev_image)
        self.next_btn = tk.Button(self.toolbar, text="Next ▶", font=("Arial", 10, "bold"),
                                  bg="#2a2a2a", fg="white", relief="flat", command=self.next_image)
        self.slideshow_btn = tk.Button(self.toolbar, text="▶ Slideshow", font=("Arial", 10),
                                      bg="#2a2a2a", fg="white", relief="flat", command=self.toggle_slideshow)
        self.fullscreen_btn = tk.Button(self.toolbar, text="⛶ Fullscreen", font=("Arial", 10),
                                       bg="#2a2a2a", fg="white", relief="flat", command=self.toggle_fullscreen)
        self.save_btn = tk.Button(self.toolbar, text="💾 Save", font=("Arial", 10),
                                 bg="#2a2a2a", fg="white", relief="flat", command=self.save_image)
        self.refresh_btn = tk.Button(self.toolbar, text="🔄 Reload", font=("Arial", 10),
                                    bg="#2a2a2a", fg="white", relief="flat", command=self.reload_failed_images)
        self.help_btn = tk.Button(self.toolbar, text="❓ Help", font=("Arial", 10),
                                 bg="#2a2a2a", fg="white", relief="flat", command=self.show_help)

        self.slideshow_active = False
        self.slideshow_job = None

        self.hide_toolbar()

    def setup_image_controls(self):
        zoom_frame = tk.Frame(self.controls_frame, bg="#0a0a0a")
        zoom_frame.pack(side="left", padx=20)
        tk.Label(zoom_frame, text="Zoom:", bg="#0a0a0a", fg="white", font=("Arial", 10)).pack(side="left")
        self.zoom_out_btn = tk.Button(zoom_frame, text="-", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                      command=self.zoom_out)
        self.zoom_out_btn.pack(side="left", padx=2)
        self.zoom_label = tk.Label(zoom_frame, text="100%", bg="#0a0a0a", fg="white", font=("Arial", 10), width=8)
        self.zoom_label.pack(side="left", padx=5)
        self.zoom_in_btn = tk.Button(zoom_frame, text="+", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                     command=self.zoom_in)
        self.zoom_in_btn.pack(side="left", padx=2)
        self.reset_zoom_btn = tk.Button(zoom_frame, text="Reset", bg="#2a2a2a", fg="white", relief="flat",
                                       command=self.reset_zoom)
        self.reset_zoom_btn.pack(side="left", padx=5)

        rot_frame = tk.Frame(self.controls_frame, bg="#0a0a0a")
        rot_frame.pack(side="left", padx=20)
        tk.Label(rot_frame, text="Rotate:", bg="#0a0a0a", fg="white", font=("Arial", 10)).pack(side="left")
        self.rotate_left_btn = tk.Button(rot_frame, text="↺", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                        command=self.rotate_left)
        self.rotate_left_btn.pack(side="left", padx=2)
        self.rotate_right_btn = tk.Button(rot_frame, text="↻", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                         command=self.rotate_right)
        self.rotate_right_btn.pack(side="left", padx=2)

        enhance_frame = tk.Frame(self.controls_frame, bg="#0a0a0a")
        enhance_frame.pack(side="left", padx=20)
        tk.Label(enhance_frame, text="Enhance:", bg="#0a0a0a", fg="white", font=("Arial", 10)).pack(side="left")
        self.brightness_btn = tk.Button(enhance_frame, text="☀", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                       command=self.adjust_brightness)
        self.brightness_btn.pack(side="left", padx=2)
        self.contrast_btn = tk.Button(enhance_frame, text="◐", bg="#2a2a2a", fg="white", relief="flat", width=3,
                                     command=self.adjust_contrast)
        self.contrast_btn.pack(side="left", padx=2)
        self.reset_enhance_btn = tk.Button(enhance_frame, text="Reset All", bg="#2a2a2a", fg="white", relief="flat",
                                          command=self.reset_enhancements)
        self.reset_enhance_btn.pack(side="left", padx=5)

    def setup_status_bar(self):
        self.status_bar = tk.Frame(self.main_frame, bg="#1a1a1a", height=25)
        self.status_bar.pack(side="bottom", fill="x")

        self.status_label = tk.Label(self.status_bar, text="Ready", bg="#1a1a1a", fg="white",
                                    font=("Arial", 9), anchor="w")
        self.status_label.pack(side="left", padx=10)

        self.image_info_label = tk.Label(self.status_bar, text="", bg="#1a1a1a", fg="white",
                                        font=("Arial", 9), anchor="e")
        self.image_info_label.pack(side="right", padx=10)

    def bind_events(self):
        self.root.bind("<Right>", lambda e: self.next_image())
        self.root.bind("<Left>", lambda e: self.prev_image())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-r>", lambda e: self.reset_view())
        self.root.bind("<space>", lambda e: self.next_image())
        self.root.bind("<BackSpace>", lambda e: self.show_cupola())
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<F5>", lambda e: self.reload_failed_images())
        self.root.bind("<plus>", lambda e: self.zoom_in())
        self.root.bind("<minus>", lambda e: self.zoom_out())
        self.root.bind("<Key-0>", lambda e: self.reset_zoom())

        self.image_label.bind("<Button-1>", self.start_pan)
        self.image_label.bind("<B1-Motion>", self.do_pan)
        self.image_label.bind("<ButtonRelease-1>", self.end_pan)
        self.image_label.bind("<MouseWheel>", self.mouse_zoom)

        self.root.bind("<Configure>", self.on_window_resize)

    def start_preloading(self):
        self.show_loading_interface()
        self.loading_thread = threading.Thread(target=self.preload_images, daemon=True)
        self.loading_thread.start()

    def show_loading_interface(self):
        self.canvas.pack_forget()
        self.loading_label.pack(expand=True, pady=20)
        self.loading_details.pack(pady=10)
        self.progress_bar.pack(pady=10)
        self.update_status("Loading ISS Cupola images from Google Drive...")

    def preload_images(self):
        loaded_count = 0
        self.failed_images = 0

        for window, urls in self.cupola_windows.items():
            self.preloaded_images[window] = []
            for i, url in enumerate(urls):
                try:
                    self.root.after(0, self.update_loading_details, f"Loading {window} - Image {i+1}/{len(urls)}")

                    retry_key = f"{window}_{i}"
                    max_retries = 3

                    for attempt in range(max_retries):
                        try:
                            response = requests.get(url, timeout=30,
                                                    headers={'User-Agent': 'Mozilla/5.0'})
                            response.raise_for_status()

                            pil_img = Image.open(BytesIO(response.content))

                            self.preloaded_images[window].append({
                                'original': pil_img,
                                'display': None,
                                'info': {
                                    'size': pil_img.size,
                                    'format': pil_img.format,
                                    'mode': pil_img.mode,
                                    'url': url
                                }
                            })
                            break
                        except Exception as retry_error:
                            if attempt == max_retries - 1:
                                raise retry_error
                            else:
                                time.sleep(1)

                    loaded_count += 1
                    progress = (loaded_count / self.total_images) * 100
                    self.root.after(0, self.update_progress, progress)

                except Exception as e:
                    print(f"Error loading {url}: {e}")
                    self.failed_images += 1
                    self.preloaded_images[window].append({
                        'original': None,
                        'display': None,
                        'info': {
                            'error': str(e),
                            'url': url
                        }
                    })

        self.root.after(0, self.loading_complete)

    def update_loading_details(self, details):
        self.loading_details.config(text=details)
        self.root.update_idletasks()

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def loading_complete(self):
        self.loading_label.pack_forget()
        self.loading_details.pack_forget()
        self.progress_bar.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.draw_cupola()

        success_count = self.total_images - self.failed_images
        status_msg = f"Ready - Loaded {success_count}/{self.total_images} images successfully"
        if self.failed_images > 0:
            status_msg += f" ({self.failed_images} failed - press F5 to retry)"

        self.update_status(status_msg)

        if self.failed_images > 0:
            messagebox.showwarning("Loading Complete",
                                   f"Loaded {success_count} out of {self.total_images} images.\n"
                                   f"{self.failed_images} images failed to load.\n\n"
                                   f"You can press F5 or click the Reload button to retry failed images.")
        else:
            messagebox.showinfo("Loading Complete",
                               f"Successfully loaded all {success_count} ISS Earth observation images!\n\n"
                               f"Click on any cupola window to start viewing.")

    def reload_failed_images(self):
        if self.failed_images == 0:
            messagebox.showinfo("No Failed Images", "All images loaded successfully!")
            return

        self.update_status("Retrying failed image downloads...")
        retry_thread = threading.Thread(target=self.retry_failed_loads, daemon=True)
        retry_thread.start()

    def retry_failed_loads(self):
        retried_count = 0
        recovered_count = 0

        for window, images in self.preloaded_images.items():
            for i, image_data in enumerate(images):
                if image_data['original'] is None and 'error' in image_data['info']:
                    retried_count += 1
                    url = image_data['info']['url']
                    self.root.after(0, self.update_status, f"Retrying {window} image {i + 1}...")

                    try:
                        response = requests.get(url, timeout=30,
                                                headers={'User-Agent': 'Mozilla/5.0'})
                        response.raise_for_status()
                        pil_img = Image.open(BytesIO(response.content))

                        images[i] = {
                            'original': pil_img,
                            'display': None,
                            'info': {
                                'size': pil_img.size,
                                'format': pil_img.format,
                                'mode': pil_img.mode,
                                'url': url
                            }
                        }
                        recovered_count += 1
                    except Exception as e:
                        print(f"Retry failed for {url}: {e}")

        self.failed_images -= recovered_count

        self.root.after(0, self.retry_complete, retried_count, recovered_count)

    def retry_complete(self, retried_count, recovered_count):
        self.update_status(f"Retry complete: {recovered_count}/{retried_count} images recovered")
        if recovered_count > 0:
            messagebox.showinfo("Retry Complete",
                               f"Successfully recovered {recovered_count} out of {retried_count} failed images!")
        else:
            messagebox.showwarning("Retry Complete",
                                   f"Unable to recover any of the {retried_count} failed images.\n"
                                   f"This may be due to network issues or invalid URLs.")

    def draw_cupola(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.draw_cupola)
            return

        center_x = canvas_width // 2
        center_y = canvas_height // 2

        scale_factor = min(canvas_width, canvas_height) / 600
        circle_r = int(60 * scale_factor)
        self.canvas.create_text(center_x, 50, text="ISS Cupola Earth Observation Dome",
                                fill="white", font=("Arial", int(16 * scale_factor), "bold"))
        success_count = self.total_images - self.failed_images
        subtitle = f"{success_count} High-Resolution Earth Images from Space"
        self.canvas.create_text(center_x, 75, text=subtitle,
                                fill="#888888", font=("Arial", int(12 * scale_factor)))

        circle = self.canvas.create_oval(center_x - circle_r, center_y - circle_r,
                                         center_x + circle_r, center_y + circle_r,
                                         fill="#2a2a2a", outline="#4a90e2", width=3, tags="window_0")

        self.canvas.tag_bind(circle, "<Button-1>", lambda e: self.show_image("Window 0"))
        self.canvas.tag_bind(circle, "<Enter>", lambda e: self.on_window_hover("Window 0"))
        self.canvas.tag_bind(circle, "<Leave>", lambda e: self.on_window_leave())

        available_count = sum(1 for img in self.preloaded_images.get("Window 0", []) if img['original'] is not None)
        self.canvas.create_text(center_x, center_y - 10, text="Window 0",
                                fill="white", font=("Arial", int(12 * scale_factor), "bold"), tags="window_0_text")
        self.canvas.create_text(center_x, center_y + 8, text=f"({available_count} images)",
                                fill="#888888", font=("Arial", int(9 * scale_factor)), tags="window_0_text")

        trap_w_top = int(50 * scale_factor)
        trap_w_bottom = int(90 * scale_factor)
        trap_h = int(60 * scale_factor)
        radius = int(140 * scale_factor)

        window_names = ["Window 1", "Window 2", "Window 3", "Window 4", "Window 5", "Window 6"]

        for i in range(6):
            angle = math.radians(i * 60 - 90)
            cx = center_x + radius * math.cos(angle)
            cy = center_y + radius * math.sin(angle)

            dx = math.cos(angle)
            dy = math.sin(angle)
            px, py = -dy, dx

            points = [
                cx - trap_w_top / 2 * px - trap_h / 2 * dx, cy - trap_w_top / 2 * py - trap_h / 2 * dy,
                cx + trap_w_top / 2 * px - trap_h / 2 * dx, cy + trap_w_top / 2 * py - trap_h / 2 * dy,
                cx + trap_w_bottom / 2 * px + trap_h / 2 * dx, cy + trap_w_bottom / 2 * py + trap_h / 2 * dy,
                cx - trap_w_bottom / 2 * px + trap_h / 2 * dx, cy - trap_w_bottom / 2 * py + trap_h / 2 * dy
            ]

            win_key = window_names[i]
            window_id = f"window_{i + 1}"

            trap = self.canvas.create_polygon(points, fill="#3a3a3a", outline="#4a90e2", width=2, tags=window_id)

            self.canvas.tag_bind(trap, "<Button-1>", lambda e, w=win_key: self.show_image(w))
            self.canvas.tag_bind(trap, "<Enter>", lambda e, w=win_key: self.on_window_hover(w))
            self.canvas.tag_bind(trap, "<Leave>", lambda e: self.on_window_leave())

            available_count = sum(1 for img in self.preloaded_images.get(win_key, []) if img['original'] is not None)

            self.canvas.create_text(cx, cy - 8, text=win_key.replace("Window ", "W"),
                                    fill="white", font=("Arial", int(10 * scale_factor), "bold"), tags=f"{window_id}_text")
            self.canvas.create_text(cx, cy + 8, text=f"({available_count})",
                                    fill="#888888", font=("Arial", int(8 * scale_factor)), tags=f"{window_id}_text")

        instructions = "Click any window to view Earth imagery • Arrow keys navigate • F1 for help"
        if self.failed_images > 0:
            instructions += f" • F5 to retry {self.failed_images} failed images"

        self.canvas.create_text(center_x, canvas_height - 30, text=instructions,
                                fill="#888888", font=("Arial", int(10 * scale_factor)))

    def on_window_hover(self, window_key):
        self.canvas.config(cursor="hand2")
        available_count = sum(1 for img in self.preloaded_images.get(window_key, []) if img['original'] is not None)
        failed_count = sum(1 for img in self.preloaded_images.get(window_key, []) if img['original'] is None)

        status = f"Hover: {window_key} - {available_count} images available"
        if failed_count > 0:
            status += f" ({failed_count} failed)"

        self.update_status(status)

    def on_window_leave(self):
        self.canvas.config(cursor="")
        success_count = self.total_images - self.failed_images
        self.update_status(f"Ready - {success_count} images loaded successfully")

    def show_image(self, window_key, idx=0):
        if window_key not in self.preloaded_images or not self.preloaded_images[window_key]:
            self.update_status(f"No images available for {window_key}")
            return

        available_images = [(i, img) for i, img in enumerate(self.preloaded_images[window_key])
                            if img['original'] is not None]

        if not available_images:
            messagebox.showwarning("No Images", f"All images for {window_key} failed to load.\n\nPress F5 to retry loading.")
            return

        if idx >= len(available_images) or self.preloaded_images[window_key][idx]['original'] is None:
            idx = available_images[0][0]

        image_data = self.preloaded_images[window_key][idx]
        if image_data['original'] is None:
            self.update_status(f"Failed to load image {idx + 1} for {window_key}")
            return

        self.current_window = window_key
        self.current_index = idx

        if self.slideshow_active:
            self.toggle_slideshow()

        self.reset_view(False)
        self.update_image_display()

        self.canvas.pack_forget()
        self.image_frame.pack(fill="both", expand=True)
        self.show_toolbar()

        available_images_count = sum(1 for img in self.preloaded_images[window_key] if img['original'] is not None)
        current_available_index = sum(1 for i, img in enumerate(self.preloaded_images[window_key][:idx + 1]) if img['original'] is not None)

        self.window_info.config(text=f"{window_key} - Image {current_available_index}/{available_images_count}")

        img_info = image_data['info']
        self.image_info_label.config(
            text=f"Size: {img_info['size'][0]}x{img_info['size'][1]} | "
                 f"Format: {img_info.get('format', 'Unknown')} | Mode: {img_info.get('mode', 'Unknown')}"
        )

        self.update_status(f"Viewing {window_key} - Use arrow keys or buttons to navigate")

    def update_image_display(self):
        if not self.current_window:
            return

        image_data = self.preloaded_images[self.current_window][self.current_index]
        if image_data['original'] is None:
            return

        pil_img = image_data['original'].copy()

        if self.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(self.brightness)

        if self.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(self.contrast)

        if self.rotation_angle != 0:
            pil_img = pil_img.rotate(-self.rotation_angle, expand=True)

        canvas_width = self.image_frame.winfo_width()
        canvas_height = self.image_frame.winfo_height() - 100

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.update_image_display)
            return

        img_width, img_height = pil_img.size
        scale_x = (canvas_width - 100) / img_width
        scale_y = (canvas_height - 100) / img_height
        base_scale = min(scale_x, scale_y) * self.zoom_factor

        new_width = int(img_width * base_scale)
        new_height = int(img_height * base_scale)

        if new_width > 0 and new_height > 0:
            display_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(display_img)

            self.image_label.config(image=tk_img)
            self.image_label.image = tk_img
            zoom_percent = int(self.zoom_factor * 100)
            self.zoom_label.config(text=f"{zoom_percent}%")
            image_data['display'] = display_img

    def show_cupola(self):
        if self.slideshow_active:
            self.toggle_slideshow()

        self.current_window = None
        self.image_frame.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.hide_toolbar()
        self.draw_cupola()

        success_count = self.total_images - self.failed_images
        self.update_status(f"Ready - {success_count} images loaded successfully")
        self.image_info_label.config(text="")

    def show_toolbar(self):
        self.back_button.pack(side="left", padx=10, pady=5)
        self.window_info.pack(side="left", padx=20)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.slideshow_btn.pack(side="left", padx=10)
        self.fullscreen_btn.pack(side="right", padx=5)
        self.save_btn.pack(side="right", padx=5)
        self.refresh_btn.pack(side="right", padx=5)
        self.help_btn.pack(side="right", padx=5)

    def hide_toolbar(self):
        for widget in [self.back_button, self.window_info, self.prev_btn, self.next_btn,
                       self.slideshow_btn, self.fullscreen_btn, self.save_btn, self.refresh_btn, self.help_btn]:
            widget.pack_forget()

    def next_image(self):
        if not self.current_window:
            return

        available_indices = [i for i, img in enumerate(self.preloaded_images[self.current_window]) if img['original'] is not None]
        if len(available_indices) <= 1:
            return

        current_pos = available_indices.index(self.current_index) if self.current_index in available_indices else 0
        next_pos = (current_pos + 1) % len(available_indices)
        next_index = available_indices[next_pos]
        self.show_image(self.current_window, next_index)

    def prev_image(self):
        if not self.current_window:
            return

        available_indices = [i for i, img in enumerate(self.preloaded_images[self.current_window]) if img['original'] is not None]
        if len(available_indices) <= 1:
            return

        current_pos = available_indices.index(self.current_index) if self.current_index in available_indices else 0
        prev_pos = (current_pos - 1) % len(available_indices)
        prev_index = available_indices[prev_pos]
        self.show_image(self.current_window, prev_index)

    def toggle_slideshow(self):
        if not self.current_window:
            return

        if self.slideshow_active:
            self.slideshow_active = False
            if self.slideshow_job:
                self.root.after_cancel(self.slideshow_job)
                self.slideshow_job = None
            self.slideshow_btn.config(text="▶ Slideshow")
            self.update_status("Slideshow stopped")
        else:
            self.slideshow_active = True
            self.slideshow_btn.config(text="⏸ Stop")
            self.update_status("Slideshow active - 3 second intervals")
            self.schedule_next_slide()

    def schedule_next_slide(self):
        if self.slideshow_active:
            self.slideshow_job = self.root.after(3000, self.slideshow_next)

    def slideshow_next(self):
        if self.slideshow_active:
            self.next_image()
            self.schedule_next_slide()

    def zoom_in(self):
        if self.current_window:
            self.zoom_factor = min(self.zoom_factor * 1.2, 5.0)
            self.update_image_display()

    def zoom_out(self):
        if self.current_window:
            self.zoom_factor = max(self.zoom_factor / 1.2, 0.1)
            self.update_image_display()

    def reset_zoom(self):
        if self.current_window:
            self.zoom_factor = 1.0
            self.pan_x = 0
            self.pan_y = 0
            self.update_image_display()

    def rotate_left(self):
        if self.current_window:
            self.rotation_angle = (self.rotation_angle - 90) % 360
            self.update_image_display()

    def rotate_right(self):
        if self.current_window:
            self.rotation_angle = (self.rotation_angle + 90) % 360
            self.update_image_display()

    def adjust_brightness(self):
        if self.current_window:
            self.brightness = 1.5 if self.brightness == 1.0 else 1.0
            self.update_image_display()

    def adjust_contrast(self):
        if self.current_window:
            self.contrast = 1.5 if self.contrast == 1.0 else 1.0
            self.update_image_display()

    def reset_enhancements(self):
        if self.current_window:
            self.brightness = 1.0
            self.contrast = 1.0
            self.rotation_angle = 0
            self.zoom_factor = 1.0
            self.update_image_display()

    def reset_view(self, update_display=True):
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rotation_angle = 0
        self.brightness = 1.0
        self.contrast = 1.0
        if update_display:
            self.update_image_display()

    def start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def do_pan(self, event):
        if hasattr(self, 'pan_start_x'):
            self.pan_x += event.x - self.pan_start_x
            self.pan_y += event.y - self.pan_start_y
            self.pan_start_x = event.x
            self.pan_start_y = event.y

    def end_pan(self, event):
        if hasattr(self, 'pan_start_x'):
            del self.pan_start_x
            del self.pan_start_y

    def mouse_zoom(self, event):
        if self.current_window:
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def toggle_fullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        self.root.attributes('-fullscreen', self.fullscreen_mode)
        if self.fullscreen_mode:
            self.update_status("Fullscreen mode - Press F11 or Escape to exit")
            self.fullscreen_btn.config(text="⛶ Exit FS")
        else:
            self.update_status("Windowed mode")
            self.fullscreen_btn.config(text="⛶ Fullscreen")

    def exit_fullscreen(self):
        if self.fullscreen_mode:
            self.fullscreen_mode = False
            self.root.attributes('-fullscreen', False)
            self.fullscreen_btn.config(text="⛶ Fullscreen")
            self.update_status("Windowed mode")

    def save_image(self):
        if not self.current_window:
            messagebox.showwarning("No Image", "No image currently displayed to save.")
            return

        image_data = self.preloaded_images[self.current_window][self.current_index]
        if image_data['original'] is None:
            messagebox.showerror("Error", "Current image could not be saved.")
            return

        img_to_save = image_data.get('display') or image_data['original']

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"ISS_Cupola_{self.current_window.replace(' ', '_')}_img{self.current_index+1}_{timestamp}.png"

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfilename=default_filename,
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if filename:
            try:
                img_to_save.save(filename)
                self.update_status(f"Image saved as {os.path.basename(filename)}")
                messagebox.showinfo("Saved", f"Image saved successfully as\n{os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")

    def show_help(self):
        help_text = """🚀 ISS Cupola Earth Viewer - Enhanced Edition 🌍

OVERVIEW:
View high-resolution Earth imagery captured from the International Space Station's 
cupola observation dome. The cupola has 7 windows providing stunning views of Earth.

KEYBOARD SHORTCUTS:
• Arrow Keys / Space: Navigate between images
• Backspace: Return to cupola overview  
• F11: Toggle fullscreen mode
• Escape: Exit fullscreen
• Ctrl+S: Save current image
• Ctrl+R: Reset all view settings
• F1: Show this help dialog
• F5: Retry loading failed images
• +/- Keys: Zoom in/out
• 0 Key: Reset zoom to 100%

MOUSE CONTROLS:
• Click & Drag: Pan image when zoomed in
• Mouse Wheel: Zoom in and out
• Click Windows: Select viewing window

IMAGE CONTROLS:
• Zoom: +/- buttons or mouse wheel (10% to 500%)
• Rotate: 90° increments left/right
• Enhance: Toggle brightness and contrast
• Reset All: Restore original settings

CUPOLA WINDOWS:
• Window 0: Nadir (directly downward) Earth view
• Windows 1-6: Side observation windows at different angles
• Each window contains multiple high-resolution images

FEATURES:
✓ 30+ high-quality ISS Earth observation images
✓ Advanced image manipulation and enhancement
✓ Automatic slideshow mode (3-second intervals)
✓ Fullscreen immersive viewing
✓ Save images with metadata timestamps
✓ Retry failed downloads automatically
✓ Responsive interface for any screen size
✓ Professional space imagery experience

TROUBLESHOOTING:
• If images fail to load, press F5 to retry
• Check internet connection for Google Drive access
• Use Reload button for individual failed images
• Contact support if persistent issues occur

Enjoy your virtual journey aboard the International Space Station! 🛰️"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - ISS Cupola Viewer")
        help_window.geometry("800x700")
        help_window.configure(bg="#1a1a1a")
        help_window.resizable(True, True)

        help_window.transient(self.root)
        help_window.grab_set()

        text_frame = tk.Frame(help_window, bg="#1a1a1a")
        text_frame.pack(fill="both", expand=True, padx=20, pady=20)

        text_widget = tk.Text(text_frame, bg="#2a2a2a", fg="white", font=("Arial", 11),
                             wrap=tk.WORD, padx=15, pady=15)
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy,
                             bg="#4a90e2", fg="white", font=("Arial", 12, "bold"),
                             padx=30, pady=10)
        close_btn.pack(pady=20)

        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (help_window.winfo_width() // 2)
        y = (help_window.winfo_screenheight() // 2) - (help_window.winfo_height() // 2)
        help_window.geometry(f"+{x}+{y}")

    def on_window_resize(self, event):
        if event.widget == self.root:
            if self.current_window:
                self.root.after_idle(self.update_image_display)
            else:
                self.root.after_idle(self.draw_cupola)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication closed by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An unexpected error occurred:\n{str(e)}")


if __name__ == "__main__":
    print("🚀 Starting ISS Cupola Earth Viewer - Enhanced Edition")
    print("Loading high-resolution Earth imagery from the International Space Station...")
    print("Please wait while images are downloaded from Google Drive...\n")

    try:
        app = ISS_Cupola_Viewer()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        input("Press Enter to exit...")
