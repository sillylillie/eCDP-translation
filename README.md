# eCDP Translation
This is a repo that aims to help translating McDonald Japan's eCDP training game on the Nintendo DS.

# Json files
Json files in this repo are strings found in the game's files, converted from binary to utf-8 using the scripts in the scripts folder.

One file may contain multiple pieces of text. Here is an example of the json structure: 

```
{
  "name": "filename",
  "strings": [
    {
      "original_japanese": "こんにちは',
      "original_pointer": 4,
      "translations": {
        "EN": {
          "translation": "Hello",
          "verification": 2,
        },
        "ES": {
          "translation": "Hola",
          "verification": 1,
        },
      },
    },
    {
      "original_japanese": "マックフライポテト",
      "original_pointer": 17,
      "translations": {
        "EN": {
          "translation": "French Fries",
          "verification": 1,
        },
        "ES": {
          "translation": "",
          "verification": 0,
        },
      },
    },
  ],
}
```

This data will be used to power a simple UI that translators can use to simply edit individual lines. 

# Scripts
There are two Python 3 scripts in the scripts folder.

parser.py reads binary files, converts the binary to strings, and outputs the result in a json structure

builder.py is not yet edited from the original version by user670. This is a high priority new feature to allow users to modify their rom copy and generate a new patch. 

# Contributing
At this time, I am not accepting contributions. If you're interested in contributing in the future, give this repo a star or send me a message. 
