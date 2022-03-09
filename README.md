# Streamlit Gif Converter

Hack Version.
No Customizing Output.

Feel free to take and hack further.

Convert a Video file into optimized gif with ffmpeg and gifsicle.

Provides for download a gif with:

- half the pixel width and height of input movie
- 20 fps frame rate
- rgb8 color space
- level 3 gifsicle optimization
- 10 ms delay between frames
- default loop setting

Allow bigger files and different destination for local with `.streamlit/config.toml` and `.streamlit/secrets.toml`

Made with :heart: from [Gar's Bar](https://tech.gerardbentley.com/)

## Basic File Drop

```py
import streamlit as st
from pathlib import Path

files = st.file_uploader("uploads", accept_multiple_files=True)
destination = Path('downloads')
destination.mkdir(exist_ok=True)

for f in files:
    bytes_data = f.read()
    st.write("filename:", f.name)
    st.write(f"{len(bytes_data) = }")
    new_file = destination / f.name
    new_file.write_bytes(bytes_data)
```

## ffmpeg convert to gif

```py
stream = ffmpeg.input(str(video_path))
stream = ffmpeg.output(
    stream,
    str(gif_path),
    pix_fmt="rgb8",
    s=f"{width//2}x{height//2}",
    r="20",
    f="gif",
)
stream = stream.overwrite_output()
ffmpeg.run(stream)
```

## gifsicle optimize

```py
subprocess.call(
    f"gifsicle --optimize=3 --delay=10 {str(gif_path)} --output {str(optimized_path)}".split()
)
```
