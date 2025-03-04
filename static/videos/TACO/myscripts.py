import cv2
import imageio
import os
import numpy as np

def split_and_resize_video_to_gif(video_path, output_dir, num_parts=12, scale_factor=4, num_splits=3):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取视频
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    frames_per_part = total_frames // num_parts  # 每部分的帧数

    for i in range(num_parts):
        start_frame = i * frames_per_part
        end_frame = start_frame + frames_per_part
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # 定位到起始帧

        # 处理每一段
        all_frames = []
        for j in range(frames_per_part):
            ret, frame = cap.read()
            h, w = frame.shape[:2]
            for k in range(num_splits):
                frame[:60, 0+(w//num_splits*k):400+(w//num_splits*k), :] = [244, 249, 247]
            
            frame[-80:, -500-(w//num_splits*(num_splits-1)):-1-(w//num_splits*(num_splits-1)), :] = [244, 249, 247]
            if not ret:
                break

            # 将帧缩小 4 倍（16倍面积压缩）
            resized_frame = cv2.resize(frame, (w // scale_factor, h // scale_factor), interpolation=cv2.INTER_AREA)

            # 横向分割为 num_splits 份
            split_width = resized_frame.shape[1] // num_splits
            split_frames = [resized_frame[:, k * split_width:(k + 1) * split_width] for k in range(num_splits)]

            # 转换 BGR 到 RGB 并存储
            all_frames.append([cv2.cvtColor(split, cv2.COLOR_BGR2RGB) for split in split_frames])

        # 遍历保存每个横向分割的 GIF
        for k in range(num_splits):
            gif_frames = [frames[k] for frames in all_frames]
            gif_path = os.path.join(output_dir, f'part_{i + 1}_split_{k + 1}.gif')
            imageio.mimsave(gif_path, gif_frames, fps=fps, loop=100)  # 维持原始帧率
            print(f"Saved: {gif_path}")

    cap.release()
    print("All GIFs saved successfully!")

# 使用示例
video_path = "TACO_expimp.mp4"  # 替换为你的视频路径
output_dir = "output_gifs3"     # 替换为你的输出目录
split_and_resize_video_to_gif(video_path, output_dir)