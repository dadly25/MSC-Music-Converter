import os
import subprocess

rawfiles = []
sortedfiles = []

# Converts source files into track[index].ogg in selected CD folder.
def convert_to_CD(source, destination, CD_num):
	counter = 1
	for file in sortedfiles:
		#Converts source files into selected CD folder.
		print(f'Converting "{file}" to track{counter}.ogg... ')
		command = f'ffmpeg -i "{source}{file}" -vn -ar 44100 -ac 2 -b:a 192k "{destination}CD{CD_num}/track{counter}.ogg" -loglevel warning -stats'
		subprocess.call(command, shell=True)
		counter = counter + 1

# Converts source files into track[index].ogg into Radio folder.
def convert_to_Radio(source, destination):
	# Reads all .ogg files in Radio folder.
	radiofiles = []
	for (dirpath, dirnames, filenames) in os.walk(f'{destination}/Radio'):
		rawfiles.extend(filenames)
		break
	for file in rawfiles:
		if '.ogg' in file:
			radiofiles.append(file)
	# Creates counter based on how many .ogg files were found, in order to convert new files in chronological order.
	counter = len(radiofiles) + 1
	for file in sortedfiles:
		# Converts source files into the Radio folder.
		print(f'Converting "{file}" to track{counter}.ogg... ')
		command = f'ffmpeg -i "{source}{file}" -vn -ar 44100 -ac 2 -b:a 192k "{destination}Radio/track{counter}.ogg" -loglevel warning -stats'
		subprocess.call(command, shell=True)
		counter = counter + 1

# Takes user input for source files, checks if directory exists and checks if input has "/" at the end, if not, adds it.
source_directory = input("Source music file directory: ")
if not os.path.isdir(source_directory):
	source_directory = input(("Directory does not exist. Try again: "))
if source_directory[-1] != "/" or source_directory[-1] != "\\":
	source_directory = source_directory + "/"

# Takes user input for game directory, checks if directory exists and checks if input has "/" at the end, if not, adds it.
msc_directory = input("Full MSC Directory: (i.e. 'steamapps/common/My Summer Car') ")
if not os.path.isdir(msc_directory):
	msc_directory = input(("Directory does not exist. Try again: "))
if msc_directory[-1] != "/" or msc_directory[-1] != "\\":
	msc_directory = msc_directory + "/"

# Ask user if converting to a CD folder or to Radio.
mode = int(input("Select mode: (1 - CD, 2 - Radio) "))
while not 1 <= mode <= 2:
	mode = int(input("Invalid input, try again: "))


# Reads all files in source directory.
for (dirpath, dirnames, filenames) in os.walk(source_directory):
	rawfiles.extend(filenames)
	break

# Append all supported audio files into an array.
for file in rawfiles:
	supported_formats = ['.mp3', '.flac', '.ogg', '.wav', '.aiff']
	for format in supported_formats:
		if format in file:
			sortedfiles.append(file)

# If CD mode selected, ask for specific CD folder, and check that input is valid.
if mode == 1:
	CD_input = int(input("CD folder number: "))
	while not 1 <= CD_input <= 3:
		CD_input = int(input("Invalid input, try again: "))
	convert_to_CD(source_directory, msc_directory, CD_input)
elif mode == 2:
	convert_to_Radio(source_directory, msc_directory)
