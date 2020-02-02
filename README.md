# Jazz2Converter
> [Jazz Jackrabbit 2](https://pl.wikipedia.org/wiki/Jazz_Jackrabbit_2) game assets converter written in **Python**
>
**NOTE**: You need legal version of Jazz Jackrabbit 2 to use that tool. You can buy it on [GOG](https://www.gog.com/game/jazz_jackrabbit_2_collection)

## Table of Contents
* [General Information](#general-information)
* [Technologies](#technologies)
* [Dependencies](#dependencies)
* [Setup](#setup)
* [Running](#running)
* [Usage](#usage)
* [Features](#features)
* [Status](#status)
* [License](#license)
* [Contact](#contact)
* [Special Thanks](#special-thanks)

## General Information
This project converts/extracts game assets files from Jazz Jackrabbit 2: The Secret Files to *normal widely-used* formats (like png, wav, ogg).

Main goal of this project is to extract assets in formats used in my ***Unity** *remake** of this game with source code available [here](https://github.com/GrzybDev/Jazz2).

## Technologies
* Written in *Python 3* (target version is: **Python 3.7**)
* Uses Pillow for sprite processing
* External tools used:
    * [FFmpeg](https://www.ffmpeg.org/)
    * [openmpt123](https://lib.openmpt.org/libopenmpt/)

## Dependencies

| Name        | Version                                           |
|-------------|---------------------------------------------------|
| colorama    | [0.4.3](https://pypi.org/project/colorama/0.4.3/) |
| Pillow      | [7.0.0](https://pypi.org/project/Pillow/7.0.0/)   |

## Setup

After cloning this repository:
- Run `pip install -r requirements.txt` in order to install required dependencies
- Download `FFmpeg` and move `ffmpeg` executable to root folder of this repository (or install it system-wise)
- Download `openmpt123` and move `openmpt123` executable to root folder of this repository (or install it system-wise)

## Running
To run this project simply launch `run.py` (this will launch interactive mode).

You can also launch this project by specifying input and output arguments (this won't launch interactive mode) 

## Usage

Usage: `Usage: run.py [-h|--help] -i|--input "GAME FOLDER" -o|--output "OUTPUT FOLDER" (arguments)`

| Argument            | Description                                                                      |
|---------------------|----------------------------------------------------------------------------------|
| `-h` or `--help`    | Shows help message                                                               |
| `-v` or `--verbose` | Shows additional debug information                                               |
| `-i` or `--input`   | Sets Jazz Jackrabbit 2 game folder                                               |
| `-o` or `--output`  | Sets converted file path (Converter output folder)                               |
| `-c` or `--clear`   | Clears output folder before conversion (to prevent *folder is not empty* errors) |
|                     |                                                                                  |
| `--skip-languages`  | Skips language files (**\*.j2s**)                                                |
| `--skip-data`       | Skip data files (**\*.j2d**)                                                     |
| `--skip-animations` | Skip animation files (**\*.j2a**)                                                |
| `--skip-episodes`   | Skip episode files (**\*.j2e**)                                                  |
| `--skip-music`      | Skip music files (**\*.j2b, \*.mod, \*.it, \*.s3m**)                             |
| `--skip-videos`     | Skip video files (**\*.j2v**)                                                    |
| `--skip-tilesets`   | Skip tileset files (**\*.j2t**)                                                  |
| `--skip-levels`     | Skip level files (**\*.j2l**)                                                    |

## Features
- Extract and convert Jazz Jackrabbit 2: The Secret Files game assets to usable formats
    - Extract it in ready-to-use format for [Jazz2](https://github.com/GrzybDev/Jazz2)
- Extract all anims (with mapping data)
- Extract data archives
    - Extract palette files
    - Extract pictures files
    - Extract sound fx list files
    - Extract texture files
- Extract episodes data
- Convert language files to JSON
- Convert level files
- Convert music to `.ogg`
- Extract tilesets
- Convert video files to `.mp4`

## License
> You can check out the full license [here](./LICENSE.md)

This project is licensed under the terms of the **GNU General Public License v3** license.

## Contact
Created by [@GrzybDev](https://grzybdev.github.io) - feel free to contact me!

## Special Thanks
- To [@deathkiller](https://github.com/deathkiller) for [inspiration](https://github.com/deathkiller/jazz2) to making this project (also for some converters and mappings code that I rewritten in Python)
