import argparse
import whisper
import os
from logger import logger

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-i", "--input", type=str, help="path to mp4 or folder")
parser.add_argument("-o", "--output", type=str, help="output file (mp4) or dir path")
parser.add_argument(
    "--save-srt",
    action="store_true",
    default=False,
    help="do not delete .srt file",
)
parser.add_argument(
    "--output-format",
    default="add",
    choices=("add", "burn", "srt"),
    help="ADD subtitles without re-encode whole video, BURN subtitles right into video or save only SRT file",
    metavar="",
)
parser.add_argument(
    "--model",
    default="large-v3",
    choices=whisper.available_models(),
    help="name of the Whisper model to use: " + ", ".join(whisper.available_models()),
    metavar="",
)
parser.add_argument("--language", type=str, default=None, help="input video language")
parser.add_argument(
    "--translate", action="store_true", default=False, help="translate to English"
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="show realtime transcript",
)
args = parser.parse_args().__dict__

to_process = []

is_input_dir = os.path.isdir(args["input"])
is_output_dir = os.path.isdir(args["output"])
if is_input_dir and not is_output_dir:
    logger.error("Input folder provided while output is file")
    exit()
if not is_input_dir:
    if not args["input"].endswith("mp4"):
        logger.error("Only mp4 type input is allowed")
        exit()
    to_process.append(args["input"])
else:
    files = list(map(str.strip, os.listdir(args["input"])))
    for file in files:
        if not file.endswith("mp4"):
            logger.warning(f"Only mp4 type input is allowed. Skip {file}")
        else:
            to_process.append(os.path.join(args["input"], file))

# Check parameters
if args["save_srt"] == False and args["output_format"] == "srt":
    args["save_srt"] = True


if args["model"].endswith(".en"):
    logger.warning("You're using English only model. Input language set to English")
    args["language"] = "en"


if args["language"] == "en" and args["translate"] == True:
    logger.warning("Parameter --translate ignored, since input language is English")
    args["translate"] = False
