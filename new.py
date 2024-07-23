import shutil
import os

# 1. Create a new folder called "snes_emulator_updated"
new_folder = "snes_emulator_updated"
os.makedirs(new_folder, exist_ok=True)

# 2. Copy all files and folders from the folder "snes_emulator" into the new folder "snes_emulator_updated"
for item in os.listdir("snes_emulator"):
    source = os.path.join("snes_emulator", item)
    destination = os.path.join(new_folder, item)
    if os.path.isfile(source):
        shutil.copy2(source, destination)
    else:
        shutil.copytree(source, destination)

# 3. Read the contents of files "brain/cpu.py" and "brain/opcodes.py" from the new folder
with open(f"{new_folder}/brain/cpu.py", "r") as cpu_file, open(f"{new_folder}/brain/opcodes.py", "r") as opcodes_file:
    cpu_code = cpu_file.read()
    opcodes_code = opcodes_file.read()

# 4. Combine the contents of "brain/cpu.py" and "brain/opcodes.py"
combined_code = cpu_code + "\n" + opcodes_code

# 5. Write the combined code into the file "snes_emulator_updated/brain/cpu.py"
with open(f"{new_folder}/brain/cpu.py", "w") as cpu_file:
    cpu_file.write(combined_code)

# 6. Delete the file "snes_emulator_updated/brain/opcodes.py"
os.remove(f"{new_folder}/brain/opcodes.py")

