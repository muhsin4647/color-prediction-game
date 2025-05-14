import tkinter as tk
import random

# Color dictionary (color name: hex code)
COLORS = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Cyan": "#00FFFF",
    "Magenta": "#FF00FF",
    "Orange": "#FFA500",
    "Purple": "#800080",
    "Pink": "#FFC0CB",
    "Brown": "#A52A2A"
}

THEMES = {
    "Classic Red": {
        "main_bg": "#FF0000",
        "text_fg": "white",
        "button_bg": "white",
        "button_fg": "black",
        "start_bg": "#4CAF50",
        "start_fg": "white"
    },
    "Dark Mode": {
        "main_bg": "#2d2d2d",
        "text_fg": "white",
        "button_bg": "#4a4a4a",
        "button_fg": "white",
        "start_bg": "#5cb85c",
        "start_fg": "white"
    },
    "Ocean Blue": {
        "main_bg": "#006994",
        "text_fg": "white",
        "button_bg": "#afeeee",
        "button_fg": "black",
        "start_bg": "#7fffd4",
        "start_fg": "black"
    }
}

class ColorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Prediction Game")
        self.root.geometry("500x600")
        self.current_theme = "Classic Red"
        
        # Game variables
        self.score = 0
        self.time_left = 60
        self.current_color = ""

        # GUI elements
        self.theme_menu = tk.OptionMenu(root, tk.StringVar(value=self.current_theme), 
                              *THEMES.keys(), command=self.change_theme)
        self.theme_menu.pack(pady=5)

        self.time_label = tk.Label(root, text=f"Time Left: {self.time_left}", 
                                font=("Arial", 12), bg=THEMES[self.current_theme]["main_bg"], 
                                fg=THEMES[self.current_theme]["text_fg"])
        self.time_label.pack(pady=5)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", 
                                 font=("Arial", 12), bg=THEMES[self.current_theme]["main_bg"], 
                                 fg=THEMES[self.current_theme]["text_fg"])
        self.score_label.pack()

        self.color_display = tk.Label(root, width=20, height=3, bg="white", 
                                    relief="solid", borderwidth=2)
        self.color_display.pack(pady=20)

        self.feedback = tk.Label(root, text="", font=("Arial", 24), 
                       bg=THEMES[self.current_theme]["main_bg"])
        self.feedback.pack()

        self.option_buttons = []
        for _ in range(4):
            btn = tk.Button(root, text="", width=15, state=tk.DISABLED,
                          relief="raised", borderwidth=3)
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.start_btn = tk.Button(root, text="Start Game", command=self.start_game,
                                 relief="raised", borderwidth=3)
        self.start_btn.pack(pady=10)

        # Apply the theme after all widgets are created
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name):
        theme = THEMES[theme_name]
        self.root.config(bg=theme["main_bg"])
        self.time_label.config(bg=theme["main_bg"], fg=theme["text_fg"])
        self.score_label.config(bg=theme["main_bg"], fg=theme["text_fg"])
        self.feedback.config(bg=theme["main_bg"])
        
        for btn in self.option_buttons:
            btn.config(bg=theme["button_bg"], fg=theme["button_fg"],
                     activebackground=theme["button_bg"], 
                     activeforeground=theme["button_fg"])
            
        self.start_btn.config(bg=theme["start_bg"], fg=theme["start_fg"],
                           activebackground=theme["start_bg"],
                           activeforeground=theme["start_fg"])
        
        self.theme_menu.config(bg=theme["button_bg"], fg=theme["button_fg"],
                             activebackground=theme["button_bg"],
                             activeforeground=theme["button_fg"])

    def change_theme(self, selected_theme):
        self.current_theme = selected_theme
        self.apply_theme(selected_theme)

    def start_game(self):
        self.score = 0
        self.time_left = 60
        self.update_score()
        self.time_label.config(text=f"Time Left: {self.time_left}")
        self.start_btn.config(state=tk.DISABLED)
        for btn in self.option_buttons:
            btn.config(state=tk.NORMAL)
        self.next_question()
        self.countdown()

    def next_question(self):
        color_names = list(COLORS.keys())
        self.current_color = random.choice(color_names)
        self.color_display.config(bg=COLORS[self.current_color])

        # Generate answer options
        options = [self.current_color] + random.sample(
            [c for c in color_names if c != self.current_color], 3
        )
        random.shuffle(options)

        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i], command=lambda opt=options[i]: self.check_answer(opt))

    def check_answer(self, selected):
        if selected == self.current_color:
            self.score += 1
            self.feedback.config(text="✓", fg="green")
        else:
            self.score -= 1
            self.feedback.config(text="✗", fg="red")
        self.update_score()
        self.root.after(1000, lambda: self.feedback.config(text=""))
        self.next_question()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}")
            self.root.after(1000, self.countdown)
        else:
            self.end_game()

    def end_game(self):
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        self.feedback.config(text=f"Game Over! Score: {self.score}", 
                           fg=THEMES[self.current_theme]["text_fg"])

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorGame(root)
    root.mainloop()