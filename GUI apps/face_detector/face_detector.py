import tkinter as tk
from tkinter import Image, StringVar, ttk
import cv2, os, filetype
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename


class FaceDetector(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Face Detector")
        self.iconbitmap("icon.ico")
        self.screensize = self._get_screen_size()
        self.width = 600
        self.height = 600
        scr_x = round((self.screensize[0] / 2) - (self.width / 2))
        scr_y = round((self.screensize[1] / 2) - (self.height / 2))
        self.geometry(f'{self.width}x{self.height}+{scr_x}+{scr_y}')
        self.resizable(True, True)

        self.img_var = StringVar(value=f"{os.path.dirname(__file__)}\\main.png")
        self.place_image()
        
        open_file_btn = ttk.Button(self, text="Open File", command=self.open_file)
        open_file_btn.place(relheight=0.1, relwidth=0.3, relx=0.01, rely=0.89)
        detect_faces_btn = ttk.Button(self, text="Detect Faces", command=self.detect_face)
        detect_faces_btn.place(relheight=0.1, relwidth=0.3, relx=0.33, rely=0.89)

        self.img_var.trace_add("write", self.trace_img)
    def trace_img(self, name: str, index: str, operation: str):
        self.image_lbl.destroy()
        self.place_image()

    def open_file(self) -> None:
        file = askopenfilename()
        print(file)
        if filetype.is_image(file):
            self.img_var.set(file)
            print("img_var updated.")

    def detect_face(self) -> None:
        """It will save only the last image. Prior to detecting faces it will remove old detection."""
        if os.path.exists(f"{os.path.dirname(__file__)}\\detected_faces.png"):
            os.remove(f"{os.path.dirname(__file__)}\\detected_faces.png")
        face_cascade = cv2.CascadeClassifier("face_detector.xml")
        img = cv2.imread(f"{self.img_var.get()}")
        if(img is not None):
            faces = face_cascade.detectMultiScale(img, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("detected_faces.png", img)
            self.img_var.set(f"{os.path.dirname(__file__)}\\detected_faces.png")
            print("Detecting faces done.")
        else:
            print("Problem with img file.")

    def place_image(self) -> None:
        image = Image.open(f"{self.img_var.get()}")
        label_width =  round((self.width / 100) * 80)
        label_height = round((self.height / 100) * 75)
        # Resize image if x,y are bigger than the label.
        if image.size[0] > label_width or image.size[1] > label_height:
            image = image.resize((label_width, label_height), Image.ANTIALIAS)        
        self.img_prv = ImageTk.PhotoImage(image)
        self.image_lbl = ttk.Label(self, image=self.img_prv, anchor='center')
        self.image_lbl.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.005)

    def _get_screen_size(self) -> tuple[float, float]:
        '''Check for screen size and return tuple[float, float].
        >>> return screen_width, screen_height'''

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height



if __name__ == "__main__":
    FaceDetector().mainloop()
