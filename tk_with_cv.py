import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class SliderParam:
    def __init__(self, name, min_val, max_val, default):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.default = default

class SliderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("スライダーとラベルのセット")

        # ウィンドウを閉じる際に呼ばれる関数をバインド
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # メインフレームを作成してgridを使用する
        main_frame = ttk.Frame(root, padding="3 3 12 12")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # ボタンを追加して、画像を選択する機能を提供
        self.button = tk.Button(main_frame, text="画像を選択", command=self.open_image)
        self.button.grid(column=0, row=0, columnspan=3, pady=10)

        # OpenCVで表示する画像の変数を初期化
        self.cv_image = None

        # afterメソッドでOpenCVの表示を定期的に更新
        self.update_cv2()

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
            name_label = ttk.Label(main_frame, text=param.name)
            name_label.grid(column=0, row=i+1, sticky=(tk.W, tk.E))

            slider = tk.Scale(
                main_frame,
                from_=param.min_val,
                to=param.max_val,
                orient=tk.HORIZONTAL,
                length=200,
                command=lambda value, index=i: self.update_label(value, index)
            )
            slider.set(param.default)
            slider.grid(column=1, row=i+1, sticky=(tk.W, tk.E))
            self.sliders.append(slider)

            value_label = ttk.Label(main_frame, text=f"{param.default:.1f}")
            value_label.grid(column=2, row=i+1, sticky=(tk.W, tk.E))
            self.labels.append(value_label)

    def update_label(self, value, index):
        self.labels[index].config(text=f"{float(value):.1f}")
        
    def on_slider_release(self, event):
        slider_index = self.sliders.index(event.widget)
        value = event.widget.get()
        print(f"スライダー {slider_index + 1} の値が {value:.1f} に設定されました")


    def open_image(self):
        # ファイルダイアログを開いて画像を選択
        file_path = filedialog.askopenfilename()
        if file_path:
            # OpenCVで画像を読み込む
            self.cv_image = cv2.imread(file_path)
            if self.cv_image is not None:
                # cv2.imshowを使って画像を表示
                cv2.imshow('OpenCV Image', self.cv_image)

    def update_cv2(self):
        # OpenCVのGUIが動作しているかチェック
        if cv2.getWindowProperty('OpenCV Image', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.waitKey(1)  # 1msの待機を行い、GUIを更新

        # 10msごとにこのメソッドを呼び出す
        self.root.after(10, self.update_cv2)

    def on_closing(self):
        # Tkinterのウィンドウが閉じられる前に呼ばれる
        if cv2.getWindowProperty('OpenCV Image', cv2.WND_PROP_VISIBLE) >= 0:
            cv2.destroyAllWindows()  # OpenCVのウィンドウを閉じる
        self.root.destroy()  # Tkinterのウィンドウを閉じる

if __name__ == "__main__":
    root = tk.Tk()
    app = SliderApp(root)
    
    for slider in app.sliders:
        slider.bind("<ButtonRelease-1>", app.on_slider_release)


    root.mainloop()