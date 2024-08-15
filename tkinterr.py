import tkinter as tk
from tkinter import ttk

class SliderParam:
    def __init__(self, name, min_val, max_val, default):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.default = default

class SliderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("スライダーとラベルのセット")
        
        self.sliders = []
        self.labels = []
     
        self.params = [
            SliderParam("明るさ", 0, 100, 50),
            SliderParam("コントラスト", 0, 100, 50),
            SliderParam("彩度", 0, 100, 50),
            SliderParam("色相", 0, 180, 90),
            SliderParam("ぼかし", 0, 20, 0)
        ]
        
        for i, param in enumerate(self.params):
            frame = ttk.Frame(self.master, padding="3 3 12 12")
            frame.grid(row=i, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            name_label = ttk.Label(frame, text=param.name)
            name_label.grid(column=0, row=0, sticky=(tk.W, tk.E))

            value_label = ttk.Label(frame, text=f"{param.default:.1f}")
            value_label.grid(column=2, row=0, sticky=(tk.W, tk.E))
            self.labels.append(value_label)

            slider = ttk.Scale(
                frame, 
                from_=param.min_val, 
                to=param.max_val, 
                orient=tk.HORIZONTAL, 
                length=200, 
                command=lambda value, index=i: self.update_label(value, index)
            )
            slider.set(param.default)
            slider.grid(column=1, row=0, sticky=(tk.W, tk.E))
            self.sliders.append(slider)

    def update_label(self, value, index):
        self.labels[index].config(text=f"{float(value):.1f}")
    
    def on_slider_release(self, event):
        slider_index = self.sliders.index(event.widget)
        value = event.widget.get()
        print(f"スライダー {slider_index + 1} の値が {value:.1f} に設定されました")

def main():
    root = tk.Tk()
    app = SliderApp(root)
    
    for slider in app.sliders:
        slider.bind("<ButtonRelease-1>", app.on_slider_release)
    
    root.mainloop()

if __name__ == "__main__":
    main()