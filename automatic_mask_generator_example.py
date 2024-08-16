import os
# if using Apple MPS, fall back to CPU for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image

def draw_masks_and_get_contours(image, masks):
    result = image.copy()
    colors = np.random.randint(0, 256, size=(len(masks), 3), dtype=np.uint8)
    
    for i, (mask_data, color) in enumerate(zip(masks, colors)):
        mask = mask_data['segmentation']
        
        # マスク領域を半透明で塗りつぶし
        result[mask] = result[mask] * 0.5 + np.array(color) * 0.5
        
        # 2値マスク画像の作成
        current_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        current_mask[mask] = 255
        # findContoursの実行と結果の保存
        
        # cv2.RETR_EXTERNAL: 一番外側の輪郭のみ抽出する
        # cv2.RETR_LIST: すべての輪郭を抽出するが、階層構造は作成しない
        # cv2.RETR_CCOMP: すべての輪郭を抽出し、2 階層の階層構造を作成する
        # cv2.RETR_TREE: すべての輪郭を抽出し、ツリーで階層構造を作成する
        contours, _ = cv2.findContours(current_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mask_data['contours'] = contours
    
    return result
    

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(f"using device: {device}")

if device.type == "cuda":
    # use bfloat16 for the entire notebook
    torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
    # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
    if torch.cuda.get_device_properties(0).major >= 8:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
elif device.type == "mps":
    print(
        "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
        "give numerically different outputs and sometimes degraded performance on MPS. "
        "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
    )

from sam2.build_sam import build_sam2
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

sam2_checkpoint = "C:\\Users\\morea\\Documents\\pg\\python\\sam2\\segment-anything-2\\checkpoints\\sam2_hiera_large.pt"
model_cfg =       "C:\\Users\\morea\\Documents\\pg\\python\\sam2\\segment-anything-2\\sam2_configs\\sam2_hiera_l.yaml"

sam2 = build_sam2(model_cfg, sam2_checkpoint, device=device, apply_postprocessing=False)
mask_generator = SAM2AutomaticMaskGenerator(sam2)

# 画像の読み込み
src_image = cv2.imread("input_image.jpg")
image = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)

# セグメンテーション実行
masks = mask_generator.generate(image)

# 結果を元にマスク分割やfindcontoursで輪郭取得
result = draw_masks_and_get_contours(image, masks)

# 結果の表示
cv2.imshow("Segmented Image", result)
cv2.imshow("SRC Image", src_image)

while True:
    # 1ミリ秒待ってキーイベントをチェック
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()






