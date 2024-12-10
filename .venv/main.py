import tkinter as tk
import random
import time


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        self.load_samples()

        self.title_label = tk.Label(root, text="Typing Speed Test", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.sample_text = tk.Text(root, height=10, width=60, wrap="word")
        self.sample_text.pack(pady=10)

        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=5)

        self.accuracy_label = tk.Label(self.score_frame, text="Accuracy: 0%", font=("Helvetica", 12))
        self.accuracy_label.pack(side="left", padx=5)

        self.timer_label = tk.Label(self.score_frame, text="Time: 0s", font=("Helvetica", 12))
        self.timer_label.pack(side="left", padx=5)

        self.wpm_label = tk.Label(self.score_frame, text="WPM: 0", font=("Helvetica", 12))
        self.wpm_label.pack(side="left", padx=5)

        self.input_text = tk.Text(root, height=10, width=60, wrap="word")
        self.input_text.pack(pady=10)
        self.input_text.bind("<KeyPress>", self.start_timer)
        self.input_text.bind("<space>", self.check_word)
        self.input_text.bind("<BackSpace>", self.check_word)
        self.input_text.bind("<Control-v>", lambda e: "break")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_test)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_test)
        self.clear_button.pack(side="left", padx=10)

        self.show_scores_button = tk.Button(self.button_frame, text="Show Best Scores", command=self.show_best_scores)
        self.show_scores_button.pack(side="left", padx=10)

        self.reset()

    def load_samples(self):
        with open("samples.txt", "r") as file:
            self.samples = file.read().split("\n\n")

    def start_test(self):
        self.sample_text.delete(1.0, "end")
        self.input_text.delete(1.0, "end")
        self.reset()
        sample_index = random.randint(0, len(self.samples) - 1)
        self.current_sample = self.samples[sample_index]
        self.sample_text.insert("end", self.current_sample)

    def start_timer(self, event):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False
        elapsed_time = int(time.time() - self.start_time)
        input_text = self.input_text.get(1.0, "end").strip()
        sample_words = self.current_sample.split()
        input_words = input_text.split()
        if len(input_words) >= len(sample_words):
            self.evaluate_accuracy()
            self.calculate_wpm(elapsed_time)

    def clear_test(self):
        self.reset()
        self.sample_text.delete(1.0, "end")
        self.input_text.delete(1.0, "end")

    def reset(self):
        self.start_time = None
        self.timer_running = False
        self.accuracy_label.config(text="Accuracy: 0%")
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")

    def check_word(self, event):
        if event.keysym == 'BackSpace':
            self.recalculate_accuracy()
            return

        input_text = self.input_text.get(1.0, "end").strip()
        sample_words = self.current_sample.split()
        input_words = input_text.split()
        correct_words = sum(1 for i in range(len(input_words)) if input_words[i] == sample_words[i])
        accuracy = correct_words / len(input_words) if input_words else 0
        self.accuracy_label.config(text=f"Accuracy: {accuracy * 100:.2f}%")
        self.calculate_wpm(int(time.time() - self.start_time))

    def recalculate_accuracy(self):
        input_text = self.input_text.get(1.0, "end").strip()
        sample_words = self.current_sample.split()
        input_words = input_text.split()
        correct_words = sum(1 for i in range(len(input_words)) if input_words[i] == sample_words[i])
        accuracy = correct_words / len(input_words) if input_words else 0
        self.accuracy_label.config(text=f"Accuracy: {accuracy * 100:.2f}%")
        self.calculate_wpm(int(time.time() - self.start_time))

    def evaluate_accuracy(self):
        input_text = self.input_text.get(1.0, "end").strip()
        sample_words = self.current_sample.split()
        input_words = input_text.split()
        correct_words = sum(1 for i in range(len(input_words)) if input_words[i] == sample_words[i])
        accuracy = correct_words / len(input_words) if input_words else 0
        if accuracy >= 0.9:
            elapsed_time = int(time.time() - self.start_time)
            wpm = self.calculate_wpm(elapsed_time)
            self.save_score(elapsed_time, accuracy, wpm)

    def calculate_wpm(self, elapsed_time):
        input_text = self.input_text.get(1.0, "end").strip()
        input_words = input_text.split()
        minutes = elapsed_time / 60
        wpm = len(input_words) / minutes if minutes > 0 else 0
        wpm = int(wpm)  # Truncate to nearest integer
        self.wpm_label.config(text=f"WPM: {wpm}")
        return wpm

    def save_score(self, time, accuracy, wpm):
        with open("scores.txt", "a") as file:
            file.write(f"{time},{accuracy},{wpm}\n")

    def show_best_scores(self):
        self.clear_test()
        self.sample_text.insert("end", "Best Scores:\n")
        with open("scores.txt", "r") as file:
            scores = [line.strip().split(",") for line in file.readlines()]
        # Convert time, accuracy, and wpm to the correct types
        scores = [(int(time), float(accuracy), int(wpm)) for time, accuracy, wpm in scores]
        # Sort by WPM in descending order, then by accuracy in descending order
        scores = sorted(scores, key=lambda x: (-x[2], -x[1]))
        for i, (time, accuracy, wpm) in enumerate(scores[:10]):
            self.sample_text.insert("end", f"{i + 1}. WPM: {wpm}, Accuracy: {accuracy * 100:.2f}%, Time: {time}s\n")


root = tk.Tk()
app = TypingSpeedTest(root)
root.mainloop()
