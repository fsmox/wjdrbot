Create_new_config  = False

if Create_new_config:

    Capture_width = 506
    Capture_height = 900

    New_width = 540
    New_height = 960

    New_picture = None
    original_size = False
else:
    Capture_width = 540
    Capture_height = 960

    New_width = 540
    New_height = 960

    New_picture = None
    original_size = True
# 操作间隔
Operation_interval = 10  # 操作间隔
save_images = True  # 是否保存图片