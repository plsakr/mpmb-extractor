# MPMB PDF Data Extractor

This tool extracts the fields from an MPMB D&D Character Sheet to be used with other applications including
[this bot](https://github.com/plsakr/dnd-bot).

The following sub-sections explain using the program to extract your data, in addition to building the program if you
do not have a Windows or Linux machine.

## For Normal Users
Use this section if you have a Windows or Linux machine (not a mac) and you need to only use the program to extract your
data from an MPMB PDF.

There are a few things you need to know before continuing:

* The program is still in very early stages of development. Bugs will happen
* This tool is only intended to be used temporarily until another solution to export the PDF data is created
* Since the tool is still very young, it may not work as expected, but if you follow the steps below _carefully_,
everything _should_ work correctly.
  
Now, to use the program, follow the following steps as closely as possible:

1. Download the tool from the [releases](https://github.com/plsakr/mpmb-extractor/releases) page. Make sure you choose the version corresponding to your operating system.
2. Run the tool. A UI with a lot of empty fields should pop up. Don't worry, if the tool is able to extract the PDF data
correctly, you shouldn't need to fill out any information by hand.
3. Click the browse button at the top and select your Character Sheet's PDF file.
4. Click the Import Data button. Make sure to **NOT DO ANYTHING** for a few seconds. The extraction is a little bit
   slow because of the complexity of the PDFs. After a few seconds (not more than 20) the fields should populate with
   your character's information. If your character's information did not automatically fill in the fields, don't panic,
   you can just fill it all in manually. Some notes on this are in step 6.
5. Double check all the information. The only field with any text characters should be the name. Every other field should
be filled with a number corresponding to the field name.
6. If you found mistakes in the extracted information, or they did not automatically fill. Make sure to take the following
into consideration:
   * You can edit any of the fields, to correct any incorrect information or fill in missing ones.
   * All fields need to be filled. If you have a zero bonus, just put a 0.
   * The fields represent the final values, as-in after all bonuses and proficiencies, and these are the final bonuses that
     will be added to dice rolls. For example, if you have a magic item that adds 2 to your initiative, the value here
     must already include that bonus.
   * Positive numbers should **not** have a `+` before them
   * Fields should not have extra spaces. **ESPECIALLY** if they are fields that should be numbers. If they are number
    fields, they should also not have any characters other than digits or a `-` for negative numbers. A `-` should be
     immediately before the digit, **NO SPACES**.
   * Auto-exracted fields _should_ already follow all the above rules, you do not need to double check them.
7. When you are done, click the Export Character button at the bottom. It will ask you where you want to save the newly
created file. This is the file containing all of your character's information in a machine-readable format. If you want
   to open it yourself, make sure it has a `.json` extension and you can open it with notepad (NOT A WORD-PROCESSOR).
   
## Running From Source
Use this section if you need to run the tool directly from source, or if you have a mac. Note that this area is intended
for developers who know what they are doing. There won't be a lot of hand holding.

You need to have Python 3 installed. The app was developed with Python 3.8.6, and I recommend using that same version to
avoid any problems.

After downloading the source code or cloning this repository, use pip to install the requirements (found in 
`requirements.txt`). I also suggest using a virtual environment to avoid any dependency clashes.

Finally, run the program by typing `python pdfextractor.py` from a terminal.

