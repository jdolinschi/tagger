# tagger
Script for AUTOMATIC1111/stable-diffusion-webui to provide a way to quickly add tags from a list to your prompt

## What it does
The script will add the ability to add tags to a separate textbox. These will be added to the end of your prompt automatically. You can add the tags manually, or via checking any checkboxes that appear below. You can also check "Add with attention brackets" to add the terms with the AUTOMATIC1111's new attention brackets: (term:1.1), with 1.1 being the default and thus added with it. You can edit these manually. Check the [docs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#attentionemphasis) for an explanation of this. You can type in anything into this textbox, and it's contents will be added to the end of your prompt when you click 'Generate'.

## Installation
1. Clone or download the files in the `scripts` folder to the `scripts` folder from https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Select "tagger" in the "Scripts" dropdown in the webui.


## Features
- Customizable tag files. Define your own favorite tags and get rid of ones you don't like.
- You can add/remove tags with attention brackets (e.g. `(greg rutkowski:1.1)`) by checking the "Add with attention brackets" checkbox. Any tags now added will have them.
- Exclude certain tags from showing up in the list by adding a `#` as the first character in the line.
- Tags in the `favorites.txt` file show up at the top of the list always
- Files in the `unused_tags` folder will not be added


## Customize
I have added some text files with tags already. These are added in from the folder `/scripts/tagger/`, which contains the text files with the tags. You can organize your tags any way you want by creating a new text file and adding your custom tags in it or modifying the text files provided. Changes or new files will be loaded on a reload of the web ui. Each line will be a new tag. The tags are organized under the file name you use. Some I have included:

| file | description |
| :---- | :-----|
| artists.txt | A list of all artists recognized by SD. Taken from Manav Mashruwala's great google sheet: https://docs.google.com/spreadsheets/d/1SRqJ7F_6yHVSOeCi3U82aA448TqEGrUlRrLLZ51abLg |
| cameras.txt | Terms relating to cameras, e.g. focal length, depth of field, etc.|
| lighting.txt | Terms relating to the lighting of the scene, e.g. harsh lighting, dramatic lighting, shadows, etc. |
| styles.txt | Terms for the style of image, e.g. oil painting, anime, black and white, etc. |
| websites.txt | Website names, e.g. artstation or pixiv. |

I will update these regularly as I come up with them or find them out there being used. Might want to cut down on the artists list though if you'd like since there's a lot of them! Could organize it, for example, by type of artist:
>fantasy-artists.txt
>sci-fi-artists.txt

![what it looks like in the web ui](https://user-images.githubusercontent.com/25022792/194760728-52641034-bb48-476b-9f18-88e555c5662a.jpg)

## Dependencies
None!
