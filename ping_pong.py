import tkinter as tk


class PingPongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brillaint Unigib Ping Pong")
        self.root.resizable(False, False)

        self.width = 800
        self.height = 600
        self.paddle_width = 12
        self.paddle_height = 100
        self.ball_radius = 10
        self.ball_speed_x = 5
        self.ball_speed_y = 5

        self.left_score = 0
        self.right_score = 0

        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.left_paddle = self.canvas.create_rectangle(
            20,
            self.height // 2 - self.paddle_height // 2,
            20 + self.paddle_width,
            self.height // 2 + self.paddle_height // 2,
            fill="#60a5fa",
        )
        self.right_paddle = self.canvas.create_rectangle(
            self.width - 20 - self.paddle_width,
            self.height // 2 - self.paddle_height // 2,
            self.width - 20,
            self.height // 2 + self.paddle_height // 2,
            fill="#fbbf24",
        )

        self.ball = self.canvas.create_oval(
            self.width // 2 - self.ball_radius,
            self.height // 2 - self.ball_radius,
            self.width // 2 + self.ball_radius,
            self.height // 2 + self.ball_radius,
            fill="#f87171",
        )

        self.score_text = self.canvas.create_text(
            self.width // 2,
            30,
            text="0 : 0",
            fill="white",
            font=("Arial", 24, "bold"),
        )

        self.left_pressed = False
        self.right_pressed = False

        self.root.bind("<KeyPress-w>", self.on_key_press)
        self.root.bind("<KeyPress-s>", self.on_key_press)
        self.root.bind("<KeyPress-Up>", self.on_key_press)
        self.root.bind("<KeyPress-Down>", self.on_key_press)
        self.root.bind("<KeyRelease-w>", self.on_key_release)
        self.root.bind("<KeyRelease-s>", self.on_key_release)
        self.root.bind("<KeyRelease-Up>", self.on_key_release)
        self.root.bind("<KeyRelease-Down>", self.on_key_release)

        self.reset_ball()
        self.game_loop()

    def on_key_press(self, event):
        if event.keysym == "w":
            self.left_pressed = True
        elif event.keysym == "s":
            self.left_pressed = False
            self.left_paddle_move("down")
        elif event.keysym == "Up":
            self.right_pressed = True
        elif event.keysym == "Down":
            self.right_pressed = False
            self.right_paddle_move("down")

    def on_key_release(self, event):
        if event.keysym == "w":
            self.left_pressed = False
        elif event.keysym == "s":
            self.left_pressed = False
        elif event.keysym == "Up":
            self.right_pressed = False
        elif event.keysym == "Down":
            self.right_pressed = False

    def move_paddle(self, paddle, direction, distance=20):
        coords = self.canvas.coords(paddle)
        top_y = coords[1]
        bottom_y = coords[3]

        if direction == "up":
            new_top = max(0, top_y - distance)
            new_bottom = new_top + self.paddle_height
        elif direction == "down":
            new_bottom = min(self.height, bottom_y + distance)
            new_top = new_bottom - self.paddle_height
        else:
            return

        self.canvas.coords(paddle, coords[0], new_top, coords[2], new_bottom)

    def left_paddle_move(self, direction):
        self.move_paddle(self.left_paddle, direction)

    def right_paddle_move(self, direction):
        self.move_paddle(self.right_paddle, direction)

    def reset_ball(self):
        self.canvas.coords(
            self.ball,
            self.width // 2 - self.ball_radius,
            self.height // 2 - self.ball_radius,
            self.width // 2 + self.ball_radius,
            self.height // 2 + self.ball_radius,
        )
        self.ball_speed_x = 5 if self.ball_speed_x > 0 else -5
        self.ball_speed_y = 5 if self.ball_speed_y > 0 else -5

    def update_ball(self):
        ball_coords = self.canvas.coords(self.ball)
        x1, y1, x2, y2 = ball_coords
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        if center_y - self.ball_radius <= 0 or center_y + self.ball_radius >= self.height:
            self.ball_speed_y *= -1

        if x1 <= 0:
            self.right_score += 1
            self.canvas.itemconfig(self.score_text, text=f"{self.left_score} : {self.right_score}")
            self.reset_ball()
            return

        if x2 >= self.width:
            self.left_score += 1
            self.canvas.itemconfig(self.score_text, text=f"{self.left_score} : {self.right_score}")
            self.reset_ball()
            return

        left_paddle_coords = self.canvas.coords(self.left_paddle)
        right_paddle_coords = self.canvas.coords(self.right_paddle)

        if x1 <= left_paddle_coords[2] and y1 <= left_paddle_coords[3] and y2 >= left_paddle_coords[1]:
            self.ball_speed_x = abs(self.ball_speed_x) + 0.5
            self.ball_speed_y = (center_y - (left_paddle_coords[1] + self.paddle_height / 2)) / 5
            self.ball_speed_x *= -1

        if x2 >= right_paddle_coords[0] and y1 <= right_paddle_coords[3] and y2 >= right_paddle_coords[1]:
            self.ball_speed_x = -abs(self.ball_speed_x) - 0.5
            self.ball_speed_y = (center_y - (right_paddle_coords[1] + self.paddle_height / 2)) / 5

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

    def move_paddles(self):
        if self.left_pressed:
            print("Left paddle moving up")
            self.move_paddle(self.left_paddle, "up")

        if self.right_pressed:
            self.move_paddle(self.right_paddle, "up")

    def game_loop(self):
        self.move_paddles()
        self.update_ball()
        self.root.after(16, self.game_loop)


def main():
    root = tk.Tk()
    game = PingPongGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
