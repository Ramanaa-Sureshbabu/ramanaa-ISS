"""
NBL Trainer — IDLE/Python (Tkinter)

A lightweight, single-file 2D prototype of the Neutral Buoyancy Laboratory training game
that runs in standard Python IDLE (no external libraries required).

Features:
- 2D top/side hybrid view showing a diver inside the pool
- Simple buoyancy (vertical float when underwater) and damping
- WASD / arrows movement, Q/E controls buoyancy up/down
- Tasks (collectibles) placed in the pool; touching them scores points
- Tasks now float freely like objects in a vacuum room (constant velocity, slight random drift, bounce off walls)
- Timer, Start / Pause / Reset buttons, Score display
- All in a single file — run with: python nbl_trainer.py or open in IDLE and Run Module

Notes for hackathon teams:
- This is a minimal, accessible prototype to test game mechanics and to run offline.
- Replace or extend with images, sound, network scoreboard, or a Pygame/three.js port for richer graphics.

"""

import tkinter as tk
import time
import random
import math

# --- Config ---
POOL_WIDTH = 900      # pixels (left-right)
POOL_HEIGHT = 450     # pixels (top-bottom)
POOL_DEPTH_METERS = 40.0  # visual depth mapping (not strictly used)
DIVER_RADIUS = 16     # pixels
TASK_RADIUS = 12      # pixels
FPS = 60
TIME_LIMIT = 120      # seconds

class Diver:
    def __init__(self, x, y):
        # x,y are canvas coords (0,0 top-left)
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 160.0  # pixels per second (horizontal)
        self.buoyancy_force = 0.0  # positive = up
        self.on_surface = False

    def update(self, dt, controls, water_level_y):
        # Horizontal movement from controls
        if controls['left']:
            self.vx = -self.speed
        elif controls['right']:
            self.vx = self.speed
        else:
            self.vx = 0

        if controls['up']:
            # forward/backwards in this 2D view -> move up visually
            self.vy -= 60 * dt
        if controls['down']:
            self.vy += 60 * dt

        # buoyancy controls adjust a constant upward acceleration
        if controls['buoy_up']:
            self.buoyancy_force += 40 * dt
        if controls['buoy_down']:
            self.buoyancy_force -= 40 * dt

        # Clamp buoyancy
        self.buoyancy_force = max(-120.0, min(120.0, self.buoyancy_force))

        # If below water (y > water_level_y) apply upward buoyancy proportional to depth
        depth = self.y - water_level_y
        if depth > 0:
            # up acceleration proportional to depth (simple model)
            self.vy -= (depth * 0.8) * dt

        # Apply buoyancy_force as vertical velocity influence
        self.vy -= self.buoyancy_force * dt * 0.1

        # Damping
        self.vx *= 0.9
        self.vy *= 0.98

        # Integrate
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Keep inside pool bounds
        margin = DIVER_RADIUS + 4
        self.x = max(margin, min(POOL_WIDTH - margin, self.x))
        self.y = max(margin, min(POOL_HEIGHT - margin, self.y))


class Task:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.collected = False
        # velocity in pixels/second — initialize with small random velocity to simulate floating in vacuum
        self.vx = random.uniform(-30.0, 30.0)
        self.vy = random.uniform(-30.0, 30.0)

    def distance_to(self, dx, dy):
        return math.hypot(self.x - dx, self.y - dy)

    def update(self, dt):
        # In a vacuum-like room: near-zero damping so the ball continues moving
        # Add tiny random drift to simulate micro-impulses
        impulse = 6.0  # magnitude of tiny random impulses
        self.vx += random.uniform(-impulse, impulse) * dt * 0.1
        self.vy += random.uniform(-impulse, impulse) * dt * 0.1

        # Integrate position
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Bounce off pool walls (simple elastic reflection)
        left = TASK_RADIUS + 4
        right = POOL_WIDTH - TASK_RADIUS - 4
        top = TASK_RADIUS + 4
        bottom = POOL_HEIGHT - TASK_RADIUS - 4

        bounced = False
        if self.x < left:
            self.x = left + (left - self.x)
            self.vx = abs(self.vx)
            bounced = True
        elif self.x > right:
            self.x = right - (self.x - right)
            self.vx = -abs(self.vx)
            bounced = True

        if self.y < top:
            self.y = top + (top - self.y)
            self.vy = abs(self.vy)
            bounced = True
        elif self.y > bottom:
            self.y = bottom - (self.y - bottom)
            self.vy = -abs(self.vy)
            bounced = True

        # optionally apply tiny damping to avoid runaway speeds
        if bounced:
            # small loss on bounce
            self.vx *= 0.98
            self.vy *= 0.98


class NBLTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('NBL Trainer — IDLE Python')

        self.frame = tk.Frame(root)
        self.frame.pack(padx=8, pady=8)

        topbar = tk.Frame(self.frame)
        topbar.pack(fill='x', pady=(0,8))

        self.time_var = tk.StringVar(value='Time: 02:00')
        self.score_var = tk.StringVar(value='Score: 0')

        tk.Label(topbar, textvariable=self.time_var, font=('Consolas', 12)).pack(side='left', padx=6)
        tk.Label(topbar, textvariable=self.score_var, font=('Consolas', 12)).pack(side='left', padx=12)

        btnframe = tk.Frame(topbar)
        btnframe.pack(side='right')
        self.start_btn = tk.Button(btnframe, text='Start', command=self.start)
        self.start_btn.pack(side='left')
        self.pause_btn = tk.Button(btnframe, text='Pause', command=self.pause, state='disabled')
        self.pause_btn.pack(side='left', padx=6)
        self.reset_btn = tk.Button(btnframe, text='Reset', command=self.reset)
        self.reset_btn.pack(side='left')

        # Canvas: draw pool and diver
        self.canvas = tk.Canvas(self.frame, width=POOL_WIDTH, height=POOL_HEIGHT, bg='#bfe9ff', highlightthickness=1, highlightbackground='#234')
        self.canvas.pack()

        # Draw water surface line
        self.water_level_y = POOL_HEIGHT * 0.35  # water surface from top
        self.canvas.create_rectangle(0, self.water_level_y, POOL_WIDTH, POOL_HEIGHT, fill='#6fb6ff', outline='')
        self.canvas.create_text(10, 12, anchor='w', text='Neutral Buoyancy Laboratory — 2D Prototype', font=('Helvetica', 10, 'bold'))

        # Diver start position
        self.diver = Diver(POOL_WIDTH/2, self.water_level_y + 30)

        # Tasks
        self.tasks = []
        self.place_tasks(5)

        # Visual elements
        self.diver_id = None
        self.task_ids = {}

        # Game state
        self.running = False
        self.time_left = TIME_LIMIT
        self.score = 0

        # Controls map
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False, 'buoy_up': False, 'buoy_down': False}

        # Bind keys
        self.root.bind('<KeyPress>', self.on_keydown)
        self.root.bind('<KeyRelease>', self.on_keyup)

        # Start mainloop via after
        self.last_time = time.time()
        self.loop()

    def place_tasks(self, n):
        self.tasks = []
        margin = 60
        for i in range(n):
            x = random.uniform(margin, POOL_WIDTH - margin)
            y = random.uniform(self.water_level_y + 20, POOL_HEIGHT - 30)
            self.tasks.append(Task(i+1, x, y))

    def start(self):
        if not self.running:
            self.running = True
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            # if starting fresh ensure timer if at zero
            if self.time_left <= 0:
                self.time_left = TIME_LIMIT
                self.score = 0
                self.update_score_time()

    def pause(self):
        self.running = False
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')

    def reset(self):
        self.running = False
        self.time_left = TIME_LIMIT
        self.score = 0
        self.diver = Diver(POOL_WIDTH/2, self.water_level_y + 30)
        self.place_tasks(5)
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
        self.update_score_time()

    def on_keydown(self, e):
        k = e.keysym.lower()
        if k in ('left','a'):
            self.controls['left'] = True
        if k in ('right','d'):
            self.controls['right'] = True
        if k in ('up','w'):
            self.controls['up'] = True
        if k in ('down','s'):
            self.controls['down'] = True
        if k == 'q':
            self.controls['buoy_up'] = True
        if k == 'e':
            self.controls['buoy_down'] = True
        if k == 'space':
            # toggle start/pause
            if self.running:
                self.pause()
            else:
                self.start()

    def on_keyup(self, e):
        k = e.keysym.lower()
        if k in ('left','a'):
            self.controls['left'] = False
        if k in ('right','d'):
            self.controls['right'] = False
        if k in ('up','w'):
            self.controls['up'] = False
        if k in ('down','s'):
            self.controls['down'] = False
        if k == 'q':
            self.controls['buoy_up'] = False
        if k == 'e':
            self.controls['buoy_down'] = False

    def check_collisions(self):
        for t in self.tasks:
            if not t.collected:
                dist = t.distance_to(self.diver.x, self.diver.y)
                if dist < (DIVER_RADIUS + TASK_RADIUS + 4):
                    t.collected = True
                    self.score += 100
                    print(f'Collected task {t.id} — score {self.score}')

    def update_score_time(self):
        mm = int(self.time_left // 60)
        ss = int(self.time_left % 60)
        self.time_var.set(f'Time: {mm:02d}:{ss:02d}')
        self.score_var.set(f'Score: {self.score}')

    def draw(self):
        # clear dynamic items
        if self.diver_id:
            self.canvas.delete(self.diver_id)
        for tid in self.task_ids.values():
            self.canvas.delete(tid)
        self.task_ids = {}

        # draw tasks
        for t in self.tasks:
            if not t.collected:
                tid = self.canvas.create_oval(t.x - TASK_RADIUS, t.y - TASK_RADIUS, t.x + TASK_RADIUS, t.y + TASK_RADIUS, fill='#ff9900', outline='')
                self.task_ids[t.id] = tid
                # label
                self.canvas.create_text(t.x, t.y, text=str(t.id), font=('Helvetica', 9, 'bold'))

        # draw diver (simple circle + helmet)
        x,y = self.diver.x, self.diver.y
        self.diver_id = self.canvas.create_oval(x - DIVER_RADIUS, y - DIVER_RADIUS, x + DIVER_RADIUS, y + DIVER_RADIUS, fill='#ffffff', outline='#333')
        # helmet visor
        self.canvas.create_oval(x - 8, y - 6, x + 8, y + 6, fill='#8fb9ff', outline='')

        # overlay small HUD
        remaining_tasks = len([t for t in self.tasks if not t.collected])
        self.canvas.delete('hud')
        self.canvas.create_text(POOL_WIDTH - 10, 12, anchor='ne', text=f'Tasks left: {remaining_tasks}', font=('Consolas', 11), tags='hud')

    def loop(self):
        now = time.time()
        dt = now - self.last_time
        # cap dt
        dt = min(1.0 / 30.0, dt)
        self.last_time = now

        # update tasks regardless of running state so they appear to float continuously
        for t in self.tasks:
            if not t.collected:
                t.update(dt)

        if self.running:
            # update timer
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.running = False
                self.start_btn.config(state='normal')
                self.pause_btn.config(state='disabled')
            # update diver physics and controls
            self.diver.update(dt, self.controls, self.water_level_y)
            # collision check
            self.check_collisions()

        # Draw the scene
        self.canvas.delete('all')
        # redraw static background: water rect and title
        self.canvas.create_rectangle(0, self.water_level_y, POOL_WIDTH, POOL_HEIGHT, fill='#6fb6ff', outline='')
        self.canvas.create_text(10, 12, anchor='w', text='Neutral Buoyancy Laboratory — 2D Prototype', font=('Helvetica', 10, 'bold'))
        # water surface line
        self.canvas.create_line(0, self.water_level_y, POOL_WIDTH, self.water_level_y, fill='#123', width=2)

        self.draw()

        # update HUD
        self.update_score_time()

        # schedule next frame
        self.root.after(int(1000/FPS), self.loop)


if __name__ == '__main__':
    root = tk.Tk()
    app = NBLTrainerApp(root)
    root.mainloop()
