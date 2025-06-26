import whisper
from logger import logger
from utils import format_timestamp, add_subtitles, burn_subtitles
import os
from cli_parse import args, to_process, is_output_dir

if is_output_dir:
    os.makedirs(args["output"], exist_ok=True)

logger.info("Loading model. Please wait...")
model = whisper.load_model(args["model"], download_root="models/")
logger.info(f"Using device: {model.device}")
task = "translate" if args["translate"] else "transcribe"

for input_file in to_process:
    logger.info(f"Starting to process {input_file}")
    result = model.transcribe(
        input_file,
        verbose=args["verbose"],
        condition_on_previous_text=False,
        language=args["language"],
        task=task,
    )

    logger.info("Creating .srt file")

    if not is_output_dir:
        srt_path = args["output"].rpartition(".")[0] + ".srt"
        output_path = args["output"]
    else:
        output_basename = os.path.basename(input_file).rpartition(".")[0]
        output_path = os.path.join(args["output"], output_basename + ".mp4")
        srt_path = os.path.join(args["output"], output_basename + ".srt")

    with open(srt_path, "w", encoding="utf-8") as srt:
        for i, segment in enumerate(result["segments"], start=1):
            line = f"{i}\n{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n{segment['text'].strip()}\n\n"
            srt.write(line)

    if args["output_format"] == "add":
        logger.info("Adding subtitles to video")
        add_subtitles(input_file, srt_path, output_path, result["language"])
        logger.info(f"Video with subtitles saved to {output_path}")
    elif args["output_format"] == "burn":
        logger.info("Burning subtitles to video")
        burn_subtitles(input_file, srt_path, output_path)
        logger.info(f"Video burned with subtitles saved to {output_path}")

    if args["save_srt"] == False:
        os.remove(srt_path)
