from moviepy import VideoFileClip
import os
import glob

VIDEO_FOLDER_PATH = 'C:/Users/sfind/Downloads/Photos-1-001/'
VIDEO_OUTPUT_PATH = 'C:/Users/sfind/Downloads/PersonalProjects/outputs/MP4Outputs/'

def convert_mov_to_mp4(input_path, output_folder):
    mov_files_path = os.path.join(input_path, '*.mov')
    for mov_file in glob.glob(mov_files_path):
        # print(mov_file)
        try:
            video_clip = VideoFileClip(mov_file)

            # Construct the output MP4 filename
            base_name = os.path.basename(mov_file)
            mp4_filename = os.path.splitext(base_name)[0] + '.mp4'
            output_path = os.path.join(output_folder, mp4_filename)

            video_clip.write_videofile(
                        output_path,
                        codec='libx264',
                        audio_codec='aac',
                        ffmpeg_params=['-preset', 'fast', '-crf', '23', '-threads', '4']
                )
            video_clip.close()
            print(f"Converted {mov_file} to {output_path}")
        except Exception as e:
            print(f"Error converting {mov_file}: {e}")

convert_mov_to_mp4(VIDEO_FOLDER_PATH, VIDEO_OUTPUT_PATH)
