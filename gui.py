import tkinter as tk
from tkinter import messagebox
from converter import Converter

ct = Converter()


class Interface:
    def __init__(self):
        self.root = tk.Tk()  # Create an instance of the tkinter (Initialize tkinter)
        # ---------- Create the title of the window ---------- #
        self.title = self.root.title('Text to Morse Code Converter')
        self.root.config(padx=50, pady=50)  # Adds padding to each side of the window

        # ---------- Create the heading of the interface ---------- #
        self.heading_label = tk.Label(master=self.root, text='Text to Morse Code Converter', font=('Arial', 16))
        self.heading_label.grid(row=0, column=1, columnspan=2)

        # ---------- Create a variable for conversion direction ---------- #
        self.conversion_var = tk.IntVar(value=1)  # Default: Text to Morse

        # ---------- Create radio buttons for conversion choices ---------- #
        self.radio_text_to_morse = tk.Radiobutton(self.root, text="Text to Morse", variable=self.conversion_var,
                                                  value=1,
                                                  command=self.update_label_text)
        self.radio_text_to_morse.grid(row=1, column=1, padx=10, pady=10)

        self.radio_morse_to_text = tk.Radiobutton(self.root, text="Morse to Text", variable=self.conversion_var,
                                                  value=2,
                                                  command=self.update_label_text)
        self.radio_morse_to_text.grid(row=1, column=2, padx=10, pady=10)

        # ---------- Create the input section ---------- #
        # Define label text options based on conversion direction
        self.text_label_text = tk.StringVar(value="Enter Text:")
        self.morse_label_text = tk.StringVar(value="Morse Code:")
        # create the entry field and label
        self.entry_label = tk.Label(self.root, textvariable=self.text_label_text, font=("Arial", 12))
        self.entry_label.grid(row=2, column=0, pady=10)
        self.entry_field = tk.Text(master=self.root, width=40, height=5)
        self.entry_field.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        # ---------- Create the output section ---------- #
        self.output_label = tk.Label(master=self.root, textvariable=self.morse_label_text, font=("Arial", 12))
        self.output_label.grid(row=4, column=0, pady=10)
        self.output_field = tk.Text(master=self.root, width=40, height=5, state="disabled")  # Read-only output
        self.output_field.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        # ---------- Create the play audio checkbox ---------- #
        self.play_audio_var = tk.BooleanVar()  # Default: No audio (False)
        self.play_audio_checkbox = tk.Checkbutton(master=self.root, text="Play Audio", variable=self.play_audio_var)
        self.play_audio_checkbox.grid(row=5, column=1, pady=5)

        # ---------- Create the convert button ---------- #
        self.convert_button = tk.Button(master=self.root, text="Convert", command=self.convert)
        self.convert_button.grid(row=3, column=1,  padx=10, pady=10)

        # ---------- Create the clear buttons ---------- #
        self.clear_button1 = tk.Button(master=self.root, text='Clear', command=self.clear_input)  # Clears entry field
        self.clear_button1.grid(row=3, column=2, padx=10, pady=10)
        self.clear_button2 = tk.Button(master=self.root, text='Clear', command=self.clear_output)  # Clears output field
        self.clear_button2.grid(row=5, column=2, padx=10, pady=10)

        # Call the update label text function to show label
        self.update_label_text()

        # ---------- Run the GUI ---------- #
        self.root.mainloop()

    def convert(self):
        """Converts the user's input and plays audio if ticked by user"""
        input_value = self.entry_field.get(1.0, tk.END).strip()  # Get user's input
        output = ''  # Empty string to fill output in
        self.output_field.config(state='normal')  # Change the state of the output field to normal to write into it
        if self.conversion_var.get() == 1:  # Text to morse
            output = ct.text_to_morse(input_value)  # Use the converter instance to change the text to morse code
            if self.play_audio_var.get():
                ct.play_morse_audio(output)  # Plays morse sequence sound if checkbox it ticked
        elif self.conversion_var.get() == 2:  # Morse to text
            if ct.is_morse_code(input_value):  # Check if the input is a morse code
                output = ct.morse_to_text(input_value)  # Use the converter instance to change the morse code to text
            else:
                messagebox.askokcancel(title='Invalid Input', message='Make sure input is in morse code sequence')
            if self.play_audio_var.get():
                ct.play_text_audio(output)  # Reads out the text if checkbox it ticked
        self.output_field.delete(0.0, tk.END)  # Clear output (if any)
        self.output_field.insert(tk.END, output)  # Write the translated output in the output field
        self.output_field.config(state='disabled')  # Return the state of the output field to disabled.

    def clear_input(self):
        """Clears the the content of the entry_field"""
        self.entry_field.delete(0.0, tk.END)  # Clears the content in the entry field

    def clear_output(self):
        """Clears the content of the output_field"""
        self.output_field.config(state='normal')  # Change the state of the output field to normal to edit it
        self.output_field.delete(0.0, tk.END)  # Clears the content in the output field
        self.output_field.config(state='disabled')  # Return the state of the output field to disabled

    def update_label_text(self):
        """Changes the label texts based on conversion direction"""
        if self.conversion_var.get() == 1:
            self.text_label_text.set("Enter Text:")
            self.morse_label_text.set("Morse Code:")
        else:
            self.text_label_text.set("Enter Morse Code:")
            self.morse_label_text.set("Text:")
        self.clear_input()  # Clear the input in the entry field (if any)
        self.clear_output()  # Clear the output in the output field (if any)
