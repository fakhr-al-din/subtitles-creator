# Subtitles Creator
Using [ffmpeg](https://github.com/FFmpeg/FFmpeg) and [OpenAI's Whisper](https://openai.com/blog/whisper).

Tested on Python 3.10.6
## Installation
```bash
git clone https://github.com/vonider/subtitles-creator.git
cd subtitles-creator
python -m pip install -r requirements.txt
```
Download FFMPEG executable along main.py file

## Usage

Create subtitles for videos from folder and add as metadata (can enable/disable)
```python
python main.py -i folder_with_videos/ -o output_folder/
```
Create subtitles for single video (only mp4)
```python
python main.py -i path/to/video.mp4 -o path/to/folder
```
OR
```python
python main.py -i path/to/video.mp4 -o path/to/output.mp4
```
Burn into video (takes longer time; subtitles cannot be disabled)
```python
python main.py -i folder_with_videos/ -o output_folder/ --output-format burn
```
Save subtitles only
```python
python main.py -i folder_with_videos/ -o output_folder/ --output-format srt
```
Add subtitles to videos and also save them
```python
python main.py -i folder_with_videos/ -o output_folder/ --save-srt
```
Burn subtitles to videos and also save them
```python
python main.py -i folder_with_videos/ -o output_folder/ --output-format burn --save-srt
```
Select Whisper model (tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, large-v3-turbo, turbo)  
Default large-v3
```python
python main.py -i folder_with_videos/ -o output_folder/ --model medium
```
Translate subtitles to english
```python
python main.py -i folder_with_videos/ -o output_folder/ --translate
```
Provide input videos language. Otherwise, auto detected
```python
python main.py -i folder_with_videos/ -o output_folder/ --language Serbian
```
Show realtime subtitles generation
```python
python main.py -i folder_with_videos/ -o output_folder/ -v
```