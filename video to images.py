import cv2
from tkinter import *
from tkinter.filedialog import *
import pafy
import vlc 

class Vidtoimage(Tk):
    
    def __init__(self, max_width=900, max_height=500, windowbg="white", title="Video To Image"):
        
        # ================================== Setting up the Screen =====================================================
        #Calling window        
        super().__init__()
        super().title(title)
        
        #Resizing Window
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.center_width = int((self.screen_width/2) - (max_width/2))
        self.center_height = int((self.screen_height/2) - (max_height/2))
        super().geometry(f"{max_width}x{max_height}+{self.center_width}+{self.center_height}")
        
        # Configuring Window
        super().maxsize(width=max_width, height=max_height)
        super().minsize(width=max_width, height=max_height)
        super().config(background=(windowbg))

        # =========================== vid to image head ===============================
        
        self.head_lab = Label(self, text="Video to Image Converter", font=("Times", 25, "bold"), bg=windowbg).pack(pady=20)
        
        # ============================ variables ===================================
        
        self.path_str = StringVar()
        self.path_str.set("")
        
        # ================================== Vid Frame ===================================
        
        self.canvas_frame = Frame(self, bg=windowbg)
        
        self.canva_vid = Canvas(self, width = 600, height= 300, bg=windowbg)
        self.canva_vid.pack()
        self.canva_vid.create_rectangle(3,5,600,300)
        
        self.canvas_frame.pack(pady=20)
        
        self.path_frame = Frame(self, bg=windowbg)
        
        self.show_vid_path = Entry(self.path_frame, textvariable=self.path_str, font=("lucida", 12), width=70, state=DISABLED, disabledbackground="white", disabledforeground="black").grid(row=0, column=0, padx=20)
        self.select_vid_button = Button(self.path_frame, text="Select video", font=("lucida", 14), command=self.select_vid, bg='lightgreen').grid(row=0, column=1, padx=20)
        
        self.path_frame.pack(pady=20)
        
        self.convert_button = Button(self, text="Convert Video", font=("lucida", 14), bg="lightblue", command=self.convert_vid).pack(pady=10)
        
        
        
    def select_vid(self):
        
        self.select_vid_path = askopenfilename(parent=self, title='Choose a Video', initialdir='/',
                                        filetypes=(("MPEG File (*.,mp4)", "*.mp4"), ("WebM File (*.webm)", "*.webm"), ("All Files", "*.*")))

        if self.select_vid_path.endswith(".mp4" or ".webm"):
            self.path_str.set(self.select_vid_path)
            self.Instance = vlc.Instance()
            self.player = self.Instance.media_player_new()
            self.player.set_hwnd(self.canva_vid.winfo_id()) #tkinter label or frame

            self.media = self.Instance.media_new(self.select_vid_path)
            self.player.set_media(self.media)
            self.player.play()
        
    
    def convert_vid(self):

        self.select_image_path = askdirectory(parent=self, initialdir="/", title="Select Directory")
        self.image_counter = 1
        
        if self.path_str.get() != "" and self.path_str.get()!=" " and self.select_image_path != "" and self.select_image_path != " ":
            
            self.vid = cv2.VideoCapture(self.path_str.get())
            while self.vid.isOpened():
                ret, frame = self.vid.read()
                if not ret:
                    print("unable to read frame")
                    break
                
                self.save_pics = cv2.imwrite(self.select_image_path+f"\image{self.image_counter}.jpeg", frame)
                self.image_counter += 1
        
                       
        
a = Vidtoimage(max_width=900, max_height=580)
a.mainloop()