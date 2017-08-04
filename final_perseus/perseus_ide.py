import Tkinter as tk
from my_language import Interpretor
class PerseusIDLE:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.wm_title("Perseus 0.2 IDLE")
        self.the_button = tk.Button(self.main_window, text = "Run Code", width=10, command=self.show_code_output)
        self.the_button.pack()
        self.the_canvas = tk.Canvas(height = 200, width = 60)
        self.code_box = tk.Text(height = 300, width = 60)
        self.code_box.place(x=0, y=0)
        self.the_canvas.pack()
        self.code_box.pack()
        tk.mainloop()

    def show_code_output(self):
        toplevel = tk.Toplevel()

        self.the_text = self.code_box.get("1.0", "end-1c").splitlines()


        code = Interpretor(self.the_text)
        code.determine_variables()
        final_output = code.show_output()

        #print final_output
        output_box = tk.Text(toplevel, height = 50, width=50)
        output_box.pack()
        for i in final_output:
            output_box.insert("insert", str(i)+"\n")



        #label1 = tk.Label(toplevel, text="Hi, how are you", height = 50, width = 100)
        #label1.pack()



ide = PerseusIDLE()
