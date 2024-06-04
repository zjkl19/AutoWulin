from paddleocr import PaddleOCR, draw_ocr
import cv2
from PIL import Image

# 初始化OCR对象，指定语言为中文，并指定本地模型路径
ocr = PaddleOCR(det_model_dir='./inference/ch_ppocr_server_v2.0_det_infer',
                rec_model_dir='./inference/ch_ppocr_server_v2.0_rec_infer',
                cls_model_dir='./inference/ch_ppocr_mobile_v2.0_cls_infer',
                use_angle_cls=True, lang='ch')

# 读取图像
img_path = "回合终了-全.png"
result = ocr.ocr(img_path, cls=True)

# 输出识别结果
for line in result:
    print(line)

# 可视化识别结果
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]

# 确保scores仅包含浮点数
def clean_score(score):
    if isinstance(score, float):
        return score
    elif isinstance(score, (tuple, list)):
        return score[0] if isinstance(score[0], float) else 0.0
    else:
        return 0.0

scores = [clean_score(line[1][1]) for line in result]

# 使用PaddleOCR提供的绘图工具绘制识别结果
im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.show()
