TEXT_BLOCKS = [
    {
        "start": 9.2,
        "end": 41.0,
        "number": 1,
        "text": "EP-133 K.O. II isn't built\nfor anacrusis or rhythmic displacement —\nwhen parts of some instruments\nare shifted relative to others.\n\nWorking on the track, I wanted to create\na musical-engineered solution\nthat bypasses the instrument's limitations —\nto make a track its architecture doesn't allow.\n\nI've never made electronic music before.\nThis is my first experience,\nand throughout the process,\nI was learning the EP-133 K.O. II itself.",
        "typing_effect": True,
        "typing_duration": 25.0
    },
    {
        "start": 41.0,
        "end": 72.0,
        "number": 2,
        "text": "I made this track over 6 months,\non weekends, in my free time, in the evenings —\n1-2 hours every 2-3 weeks.\n\nThe solution was\nto write scenes from the middle.\nThe end of a scene contains\nthe rhythmic displacement\nthat begins the next bar.\n\nIts beginning contains either\nthe main part of the phrase\nthat follows the displacement,\nor the phrase that preceded it.",
        "typing_effect": True,
        "typing_duration": 25.0
    },
    {
        "start": 72.0,
        "end": 103.0,
        "number": 3,
        "text": "In the second case, at the end of the scene,\nwhat has already been played will play again —\nso performing the track requires\nswitching scenes one after another.\n\nFrom a scene where the beginning\nprecedes the rhythmic displacement —\nto a scene where the beginning\ncontinues the displacement that ends it.\n\nTo make scene transitions smooth,\nthe bars at the transition point\nare duplicated in both scenes.",
        "typing_effect": True,
        "typing_duration": 25.0
    },
    {
        "start": 103.0,
        "end": 134.0,
        "number": 4,
        "text": "8 scenes are switched\nevery 2-4 bars.\n\nThe scene structure in the sequencer,\nscene switching, duplicated bars,\nand the current bar position\nare all shown in the diagram below.\n\nThis diagram is my 6 months of evenings —\nturned into 2 minutes of music.",
        "typing_effect": True,
        "typing_duration": 20.0
    }
]

ASCII_TEXT = ["███████╗██████╗       ██╗██████╗ ██████╗      ██╗  ██╗      ██████╗      ██╗ ██╗",
              "██╔════╝██╔══██╗      ██║╚════██╗╚════██╗     ██║ ██╔╝     ██╔═══██╗     ██║ ██║",
              "█████╗  ██████╔╝█████╗██║ █████╔╝ █████╔╝     █████╔╝      ██║   ██║     ██║ ██║",
              "██╔══╝  ██╔═══╝ ╚════╝██║ ╚═══██╗ ╚═══██╗     ██╔═██╗      ██║   ██║     ██║ ██║",
              "███████╗██║           ██║██████╔╝██████╔╝     ██║  ██╗ ██╗ ╚██████╔╝ ██╗ ██║ ██║",
              "╚══════╝╚═╝           ╚═╝╚═════╝ ╚═════╝      ╚═╝  ╚═╝ ╚═╝  ╚═════╝  ╚═╝ ╚═╝ ╚═╝"]

INFO_LINES = [
    "ARTIST       : Pasha Iden",
    "TRACK        : From the Ruins",
    "INSTRUMENT   : EP-133 K.O. II",
    "BPM          : 86",
    "SCENES       : 8",
    "ENGINE       : Python / data-driven",
    "LOCATION     : Krasnodar",
    "DATE         : June 2026",
    "STATUS       : processing...",
]

START_LOGS = [
    "> 256 samples, latency: 5.8 ms",
    "> 5 sounds, 3 groups, 8 scenes",
    "> Track lenth: 2:05 minutes",
    "> 21.4 Mb .wav compilled",
    "> Bit depth: 16-bit, sample rate: 44.1 kHz",
    "> Ableton processing: eq, reverb",
    "> Overlay render: scenes processing...",
    "> Render mode: True",
    "> Render time: ~137.6 sec, output: 1920x1080",
    "> Scenes render: completed",
    "> Status: Ready."
]

FINAL_LOGS = [
    "+-------------------------------------------------------+",
    "|                                                       |",
    "|  > Overlay source: github.com/pashaIden/ep133-overlay |",
    "|  > Built with Python / data-driven                    |",
    "|  > Vibecoded with DeepSeek                            |",
    "|                                                       |",
    "|         Session closed. Thanks for listening.         |",
    "|                                                       |",
    "+-------------------------------------------------------+"
]