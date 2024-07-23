import pygame
import tkinter as tk
from tkinter import filedialog

from snes_emulator.brain.cartridge import Cartridge
from snes_emulator.hands.controller import Controller
from snes_emulator.eyes.display import Display
from snes_emulator.memory.brain import Memory
from snes_emulator.apu.ears import APU
from snes_emulator.cpu.brain import CPU
from snes_emulator.eyes.ppu import PPU

def load_rom():
    """Öffnet einen Dateidialog zur Auswahl einer ROM-Datei und lädt sie."""
    global cartridge, running
    filepath = filedialog.askopenfilename(
        initialdir=".",
        title="ROM auswählen",
        filetypes=(("SNES ROMs", "*.sfc"), ("alle Dateien", "*.*"))
    )
    if filepath:
        cartridge = Cartridge(filepath)
        cartridge.load_rom(memory)
        running = False # Emulation stoppen, wenn neue ROM geladen wird

def start_emulation():
    """Startet die Emulation."""
    global running
    running = True

def stop_emulation():
    """Stoppt die Emulation."""
    global running
    running = False

# Emulator-Komponenten erstellen (außerhalb der main-Funktion)
memory = Memory()
ppu = PPU(memory)
apu = APU(memory)
cpu = CPU(memory, ppu, apu)
display = Display()
controller = Controller()
running = False  # Variable zur Steuerung der Emulation
cartridge = None

def main():
    global running

    pygame.init()

    # GUI erstellen
    root = tk.Tk()
    root.title("SNES Emulator")

    load_button = tk.Button(root, text="ROM laden", command=load_rom)
    load_button.pack()

    start_button = tk.Button(root, text="Start", command=start_emulation)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop", command=stop_emulation)
    stop_button.pack()

    # Emulator-Hauptschleife
    while True:
        if running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    controller.handle_event(event)

            cpu.set_controller_state(controller.get_button_state())
            cpu.execute_instruction()
            ppu.render()
            apu.step()
            display.update(ppu.get_frame())

        # GUI-Events verarbeiten
        root.update()
        root.update_idletasks()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()
