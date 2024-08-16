import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image

class SliderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Slider App")
        self.geometry("500x900")
        
        # ウィンドウを閉じる際に呼ばれる関数をバインド
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
       

        # スライダーの名前、デフォルト値、整数フラグを保持するリスト
        self.sliders_info = [
            ("points_per_side", 64, True),
            ("points_per_batch", 128, True),
            ("pred_iou_thresh", 0.7, False),
            ("stability_score_thresh", 0.92, False),
            ("stability_score_offset", 0.7, False),
            ("crop_n_layers", 1, True),
            ("box_nms_thresh", 0.7, False),
            ("crop_n_points_downscale_factor", 2, True),
            ("min_mask_region_area", 25.0, False),
        ]
        # スライダーセットを作成
        for i, (name, default_value, is_integer) in enumerate(self.sliders_info):
            self.create_slider_set(i, name, default_value, is_integer)
            
         # ボタンを追加して、画像を選択する機能を提供
        self.button = tk.Button(self, text="画像を選択", command=self.open_image)
        self.button.pack()


    def create_slider_set(self, index, name, default_value, is_integer):
        # フレームを作成して、ラベルとスライダーを含める
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # ラベルを作成
        if is_integer:
            self.value_label = tk.Label(frame, text=f"{name}: {int(default_value)}")
        else:
            self.value_label = tk.Label(frame, text=f"{name}: {default_value:.1f}")
        self.value_label.pack()

        # スライダーを作成
        slider = ttk.Scale(frame, from_=0.0, to=200.0, orient='horizontal', length=400,
                           command=lambda val, idx=index: self.update_label(val, idx))
        slider.set(default_value)
        slider.pack()

        # スライダーの値を確定するためのイベントバインド
        slider.bind("<ButtonRelease-1>", lambda event, s=slider, idx=index: self.on_slider_release(event, s, idx))

    def update_label(self, value, index):
        # ドラッグ中にラベルを更新
        is_integer = self.sliders_info[index][2]
        if is_integer:
            truncated_value = int(float(value))
        else:
            truncated_value = self.truncate_to_one_decimal(value)
        label = self.winfo_children()[index].winfo_children()[0]
        if is_integer:
            label.config(text=f"{self.sliders_info[index][0]}: {truncated_value}")
        else:
            label.config(text=f"{self.sliders_info[index][0]}: {truncated_value:.1f}")

    def on_slider_release(self, event, slider, index):
        # スライダー値を取得し、整数または小数点以下1桁で確定値を表示
        is_integer = self.sliders_info[index][2]
        if is_integer:
            value = int(slider.get())
        else:
            value = self.truncate_to_one_decimal(slider.get())
        
        print(value)

    def truncate_to_one_decimal(self, value):
        # スライダーの値を浮動小数点数に変換し、小数点以下1桁までを抽出
        value = float(value)
        return int(value * 10) / 10.0
        
        
    def open_image(self):
        # ファイルダイアログを開いて画像を選択
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)

            # OpenCVが扱える形式 (NumPy配列) に変換
            self.cv_image = np.array(image)
            self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR)
            
            if self.cv_image is not None:
                # cv2.imshowを使って画像を表示
                cv2.imshow('img', self.cv_image)
                self.update_cv2()
                
    def update_cv2(self):
        cv2.imshow('img', self.cv_image)
        cv2.waitKey(1)  # 1msの待機を行い、GUIを更新
        
        # 10msごとにこのメソッドを呼び出す
        self.after(10, self.update_cv2)

    def on_closing(self):
        # Tkinterのウィンドウが閉じられる前に呼ばれる
        if cv2.getWindowProperty('OpenCV Image', cv2.WND_PROP_VISIBLE) >= 0:
            cv2.destroyAllWindows()  # OpenCVのウィンドウを閉じる
        self.destroy()  # Tkinterのウィンドウを閉じる

if __name__ == "__main__":
    app = SliderApp()
    app.mainloop()
