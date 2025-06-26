import os
import ffmpeg


def format_timestamp(seconds: float, always_include_hours: bool = True):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def burn_subtitles(input_path, srt_path, output_path):
    video = ffmpeg.input(input_path)
    audio = video.audio
    ffmpeg.concat(
        video.filter(
            "subtitles", srt_path, force_style="OutlineColour=&H40000000,BorderStyle=3"
        ),
        audio,
        v=1,
        a=1,
    ).output(output_path).run(overwrite_output=True)


def add_subtitles(input_path, srt_path, output_path, language):
    ff_input = ffmpeg.input(input_path)
    video = ff_input["v"]
    audio = ff_input["a"]
    ff_sub = ffmpeg.input(srt_path)
    sub = ff_sub["s"]
    output_ff = ffmpeg.output(
        video,
        audio,
        sub,
        output_path,
        vcodec="copy",
        acodec="copy",
        scodec="mov_text",
        **{"metadata:s:s:0": f"title={language} - Whisper"},
    )
    command = ffmpeg.overwrite_output(output_ff)
    ffmpeg.run(command)
