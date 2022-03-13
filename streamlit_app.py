from pathlib import Path
import subprocess

import streamlit as st
import ffmpeg

with st.expander("What is this?"):
    st.write(Path('README.md').read_text())

DELETE_MODE = st.secrets.get("delete_mode", True)
DOWNLOAD_DIR = st.secrets.get("download_dir", "downloads")
MOVIE_FORMATS = "WEBM MPG MP2 MPEG MPE MPV OGG MP4 M4P M4V AVI MOV QT WMV FLV SWF AVCHD".split()

if 'is_downloaded' not in st.session_state:
    st.session_state.is_downloaded = False

def set_state(key, value):
    st.session_state[key] = value

downloads = Path(DOWNLOAD_DIR)
downloads.mkdir(exist_ok=True, parents=True)

video_file = st.file_uploader(
    label="Upload a video file to make into a GIF", type=MOVIE_FORMATS
)

if st.session_state.is_downloaded:
    st.warning("Already downloaded, click below to re-run")
    st.button("Re-run on same file", on_click=set_state, args=('is_downloaded', False))
    st.stop()

if video_file is None:
    st.warning("Upload a video to convert to gif")
    st.stop()

st.success(f"Uploaded {video_file.name}! Awesome! :movie_camera:")
st.video(video_file)
with st.spinner("Saving Video"):
    new_name = "".join(ch for ch in video_file.name if ch.isalnum() or ch in "._-")
    video_path = downloads / new_name
    video_path.write_bytes(video_file.read())

gif_path = video_path.with_suffix(".gif")
st.success(f"Saved video {str(video_path)}. Converting to gif")

probe = ffmpeg.probe(video_path)
video_stream = next(
    (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
)
if video_stream is None:
    st.error("No video stream found")
    st.stop()

with st.expander("Video Info"):
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    st.write(f"Width (px): {width}")
    st.write(f"Height (px): {height}")
    st.write(f"Duration (seconds): {video_stream['duration']}")
    st.write(f"Number of Frames: {video_stream['nb_frames']}")
    st.write(video_stream)

with st.spinner("Converting with ffmpeg"):
    stream = ffmpeg.input(str(video_path))
    stream = ffmpeg.output(
        stream,
        str(gif_path),
        pix_fmt="rgb8",
        s=f"{width//2}x{height//2}",
        r="17",
        f="gif",
    )
    stream = stream.overwrite_output()
    ffmpeg.run(stream)

st.success(f"Saved converted gif {str(gif_path)}!")
optimized_path = gif_path.with_name("opt_" + gif_path.name)
with st.spinner(f"Compressing with gifsicle to file {optimized_path}"):
    subprocess.call(
        f"gifsicle --optimize=3 --delay=10 {str(gif_path)} --output {str(optimized_path)}".split()
    )
st.success(f"Optimized to file {optimized_path}")

gif = optimized_path.read_bytes()
st.image(gif)

did_download = st.download_button(
    "Download your gif!",
    data=gif,
    file_name=gif_path.name,
    mime="image/gif",
    help="Download your gif to your local computer",
    on_click=set_state, args=('is_downloaded', True)
)


if DELETE_MODE:
    with st.spinner("Cleaning up files"):
        video_path.unlink()
        gif_path.unlink()
        optimized_path.unlink()
