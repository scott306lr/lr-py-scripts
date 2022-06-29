from argparse import ArgumentParser
from pathlib import Path
import cv2
import os
from time import time
import tqdm

def extract(vid_path, save_dir, skip=10, end_frame=-1, offset=0):
    cap = cv2.VideoCapture(vid_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    todo = (length - offset) // skip
    print(f"Video width: {width}")
    print(f"Video height: {height}")
    print(f"Video fps: {fps}")
    print(f"Video length: {length}")
    print(f"Start to extract from frame {offset}.")
    print(f"Frame skip count = {skip}, so {todo} frames to extract.")
    assert offset < length, "offset should be smaller than video length."
    assert todo > 0, "There should be more than 1 frame to extract."

    # skip frames smaller than offset count
    skipped = 0
    while (cap.isOpened() and skipped < offset):
        cap.read()
        skipped += 1
    
    # Start extracting
    with open(os.path.join(save_dir, 'rgb.txt'), 'w') as f:
        print('Extracting...')
        bar = tqdm.tqdm(total=todo)

        frame_cnt = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret or frame.size == 0 or frame_no == end_frame:
                cap.release()
                break
            
            frame_no = frame_cnt + offset
            if frame_cnt % skip == 0:
                frame_name = f'{frame_no}.png'
                cv2.imwrite(os.path.join(save_dir, frame_name), frame)
                now = time()
                f.write(f"{now} {frame_name}\n")
                bar.update(1)
            frame_cnt += 1

    print(f'\nExtracted files to "{save_dir}" successfully.')
    return

def main():
    parser = ArgumentParser(description="Extract a video into images.")
    parser.add_argument('vid_path', help='Location of the video.')
    parser.add_argument('save_dir', help='location of the directory to save the files.')
    parser.add_argument('--skip', default=10, type=int, help='Amount of frames to ignore after a save.')
    parser.add_argument('--end_frame', default=-1, type=int, help='Early stop on specific frame count.')
    parser.add_argument('--offset', default=0, type=int, help='Start extracting from offset frame count.')

    args = parser.parse_args()
    VIDEO_PATH = args.vid_path
    SAVE_DIR = args.save_dir
    SKIP = args.skip
    END_FRAME = args.end_frame
    OFFSET = args.offset
    
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    extract(VIDEO_PATH, SAVE_DIR, SKIP, END_FRAME, OFFSET)

if __name__ == "__main__":
    main()
