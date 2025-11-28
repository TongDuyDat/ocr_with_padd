# Initialize PaddleOCR instance
from paddleocr import PaddleOCR, PaddleOCRVL
# ocr = PaddleOCR(
#     use_doc_orientation_classify=True,  # Phát hiện hướng văn bản
#     use_doc_unwarping=False,            # Làm phẳng tài liệu
#     # text_recognition_model_name = "latin_PP-OCRv5_mobile_rec",
#     use_textline_orientation=True,      # Phát hiện hướng dòng text
#     text_recognition_model_dir = "/mnt/d/ThucTap/OCR_Labs/models/tdd_ocr",
#     # doc_parser=True,                    # Bật chế độ phân tích tài liệu
#     # use_angle_cls=True,                 # Phát hiện góc xoay
#     # lang='vi'
#     )

# pipeline = PaddleOCRVL(
#     use_doc_orientation_classify=True,
#     use_doc_unwarping=True,
#     use_layout_detection=True,
#     vl_rec_model_dir = "/home/tongdat/.paddlex/official_models/PaddleOCR-VL"
#     # show_log=True  # Bật log để xem model nào đang tải
# )
# # pipeline = PaddleOCRVL(use_doc_orientation_classify=True) # Use use_doc_orientation_classify to enable/disable document orientation classification model
# # pipeline = PaddleOCRVL(use_doc_unwarping=True) # Use use_doc_unwarping to enable/disable document unwarping module
# # pipeline = PaddleOCRVL(use_layout_detection=False) # Use use_layout_detection to enable/disable layout detection module
# output = pipeline.predict("images/image9.png")
# for res in output:
#     res.print() ## Print the structured prediction output
#     res.save_to_json(save_path="output") ## Save the current image's structured result in JSON format
#     res.save_to_markdown(save_path="output") ## Save the current image's result in Markdown format
# exit()
# Run OCR inference on a sample image 
# result = ocr.predict(
#     input="images/image9.png",
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
#     text_det_unclip_ratio=None,
#     text_rec_score_thresh=None,
#     # return_word_box=True,
#     text_det_limit_side_len=256
#     )

# # Visualize the results and save the JSON results
# for res in result:
#     res.print()
#     res.save_to_img("output")
#     res.save_to_json("output")
    
# from paddleocr import PaddleOCRVL

# pipeline = PaddleOCRVL()
# output = pipeline.predict("images/image6.png")
# for res in output:
#     res.print()
#     res.save_to_json(save_path="output")
#     res.save_to_markdown(save_path="output")

from paddleocr import PPStructureV3
# pipeline = PPStructureV3()
pipeline = PPStructureV3(lang="vi", device="gpu") # Set the lang parameter to use the English text recognition model. For other supported languages, see Section 5: Appendix. By default, both Chinese and English text recognition models are enabled.
output = pipeline.predict("images/image4.png")
for res in output:
    res.print() ## Print the structured prediction output
    res.save_to_json(save_path="output") ## Save the current image's structured result in JSON format
    res.save_to_markdown(save_path="output") ## Save the current image's result in Markdown format