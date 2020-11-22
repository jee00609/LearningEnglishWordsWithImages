from tkinter import *
# from tkinter import ttk
from tkinter import filedialog
import os, shutil
import os.path

# ///////////////////////////
from typing import Dict

#내가 만든 파일들
#발음 평가
from pkg.procor import proCorrect
#이미지 객체 추출
from pkg.obdtc import objectDetect
#api가 인식한 나의 말
from pkg.vrecog import voiceRecognition
# ////////////////////////
from PIL import Image, ImageTk
# ///////////////////////////
import tkinter as tk

# /////////////////////////
#pcm 녹음 coding: utf-8 
import sounddevice as sd

class Root(Tk):
    def __init__(self):
        
        global qImage_name #Quest 이미지
        global imgLabel #Quest 이미지에 대한 라벨
        global questionText #Quest 설명에 대한 라벨
        global pronunciationText #발음 평가 점수에 대한 라벨
        global quesiton_list #이미지를 객체 검출하고 나온 단어들 모음
        global questionText_list #Quest 이미지에서 검출된 객체의 개수 설명
        global voiceRecogText #컴퓨터가 인식하는 사용자의 말이 들어가는 텍스트 라벨
        global questionNumber
        
        global desc_button #설명 버튼 (on / off  때문에 global)
        global descWindow # 새 윈도우 창 (설명)
        global descimgLabel # 프로그램 설명 윈도우 창 이미지 라벨
        global descFileNum #프로그램 설명 윈도우 창 이미지 파일 명
        descFileNum =0
        
        questionNumber = 0
        originfileName = "./image/noimage.jpg"
        

        
        #Result 이미지
        rImage_name = "base"
        rImageLevel = "./image/"
        rImageDir = rImageLevel+str(rImage_name)+".jpg"
        
        
        pronunciation = 0
        strPronunciation = "Your pronunciation score is "+str(pronunciation)
        
        super(Root,self).__init__()
        self.title("Learning English Words with Images")
        self.config(background="MistyRose")
        self.minsize(800,500)

        self.labelFrame = tk.LabelFrame(self,text="Open A File")
        self.labelFrame.grid(column=0,row=1,padx= 20, pady= 20)
        self.btton()
        
        # 설명 버튼
        desc_button = tk.Button(self, text="Description",background="LightGoldenrod1",command=self.createNewWindow)
        desc_button.place(x=700, y=0, width=100, height=50)
        
#         ////////////////////

        #기본 이미지 No image available
        img = Image.open(originfileName)
        img = img.resize((350, 200))
        photo = ImageTk.PhotoImage(img)

        self.photolabel = Label(image=photo)
        self.photolabel.image = photo 
        self.photolabel.place(x=25,y=75)

        #이미지에서 검출된 객체의 개수 설명
        questionText_list=tk.Text(self)
        questionText_list.insert(tk.CURRENT, "Nothing is being detected in image")
        ##아래 두줄 모두 중앙 정렬을 위해 필요하다.
        questionText_list.tag_configure("center", justify='center')
        questionText_list.tag_add("center", "1.0", "end")
        questionText_list.place(x=27, y=300, width=350, height=30)
        
        #이미지 설명
        questionText=tk.Text(self)
        questionText.insert(tk.CURRENT, "Please browse your image file")
        ##아래 두줄 모두 중앙 정렬을 위해 필요하다.
        questionText.tag_configure("center", justify='center')
        questionText.tag_add("center", "1.0", "end")
        questionText.place(x=27, y=350, width=350, height=30)
        
#         /////////////////////////
        #객체 검출 버튼
        objDetect_button=tk.Button(self, text="Object Detect",background="LightGoldenrod1",command=self.objectD)
        objDetect_button.place(x=50, y=400, width=100, height=50)

        #Record 녹음 버튼
        record_button = tk.Button(self, text='Speaking',background="LightGoldenrod1",command=self.startrecording)
        record_button.place(x=500, y=400, width=75, height=50)
        #발음 평가 버튼
        proCor_button = tk.Button(self, text='Evaluation',background="LightGoldenrod1",command=self.pronunciationC)
        proCor_button.place(x=625, y=400, width=75, height=50)
#         ///////////////////////////

        #Result 이미지
        rLoad = Image.open(rImageDir)
        rLoad = rLoad.resize((350, 200))
        rRender = ImageTk.PhotoImage(rLoad)
        rlmg = tk.Label(self, image=rRender)
        rlmg.image = rRender
        rlmg.place(x=425, y=75)
        
        #발음 평가 점수 Text 창
        pronunciationText = tk.Text(self)
        pronunciationText.insert(tk.CURRENT, strPronunciation)
        ##아래 두줄 모두 중앙 정렬을 위해 필요하다.
        pronunciationText.tag_configure("center", justify='center')
        pronunciationText.tag_add("center", "1.0", "end")
        pronunciationText.place(x=427, y=300, width=350, height=30)
        
        #컴퓨터가 인식한 사용자의 발음
        voiceRecogText = tk.Text(self)
        voiceRecogText.insert(tk.CURRENT, "My sentences recognized by the computer")
        ##아래 두줄 모두 중앙 정렬을 위해 필요하다.
        voiceRecogText.tag_configure("center", justify='center')
        voiceRecogText.tag_add("center", "1.0", "end")
        voiceRecogText.place(x=427, y=350, width=350, height=30)
        
        #이전 버튼
        prev_button = tk.Button(self, text='Prev',background="LightGoldenrod1",command=self.prevB)
        prev_button.place(x=150, y=400, width=100, height=50)
        #다음 버튼
        next_button = tk.Button(self, text='Next',background="LightGoldenrod1",command=self.nextB)
        next_button.place(x=250, y=400, width=100, height=50)

        
#///////////////////////////////////////

    def createNewWindow(self):
        global desc_button
        
        global descWindow
        global descimgLabel
        self.descFileNum = 0
        descPath = "description/"
        descFile = str(descFileNum)+".png"
        fullDesc = descPath+descFile
        
        #메인 창에서 중복해서 설명창을 키지 못하도록 상태 변경
        desc_button['state'] = tk.DISABLED
        
        descWindow = tk.Toplevel(self)
        descWindow.title("Description")
        descWindow.minsize(800,500)
        descWindow.config(background="ghost white")
        # State Bar X key function change
        descWindow.protocol("WM_DELETE_WINDOW", self.descWindowDestroy)
        
        load = Image.open(fullDesc)
        load = load.resize((700, 450))
        render = ImageTk.PhotoImage(load)
        descimgLabel = tk.Label(descWindow, image=render)
        descimgLabel.image = render
        descimgLabel.place(x=50, y=0)
        
        #이전 버튼
        desc_prev_button = tk.Button(descWindow, text='Prev',background="LightSkyBlue1",command = self.descPrev)
        desc_prev_button.place(x=325, y=450, width=75, height=50)
        #다음 버튼
        desc_next_button = tk.Button(descWindow, text='Next',background="LightSkyBlue1",command = self.descNext)
        desc_next_button.place(x=400, y=450, width=75, height=50)
        
        
        descWindow.bind("<Escape>", lambda e:self.changeButtonState(e))
        
    #설명창을  ESC 키로 닫을 경우
    #닫으면 다시 메인창에서 설명창을 킬 수 있도록 바꿈
    def changeButtonState(self,e):
        global descWindow
        global desc_button
        desc_button['state'] = tk.NORMAL
        descWindow.destroy()
    
    #설명창을 state bar 의 X 키로 로 껐을 경우
    #닫으면 다시 메인창에서 설명창을 킬 수 있도록 바꿈
    def descWindowDestroy(self):
        global descWindow
        global desc_button
        desc_button['state'] = tk.NORMAL
        descWindow.destroy()
        
    #설명 이전 장    
    def descPrev(self):
        global descWindow
        global descimgLabel
        global descFileNum
        descPath = "description/"
        
        descFileNum = descFileNum - 1
        if descFileNum < 0:
            descFileNum = 0
        
        descFile = str(descFileNum)+".png"
        fullDesc = descPath+descFile
        
        load = Image.open(fullDesc)
        load = load.resize((700, 450))
        render = ImageTk.PhotoImage(load)
        descimgLabel = tk.Label(descWindow, image=render)
        descimgLabel.image = render
        descimgLabel.place(x=50, y=0)

        
    #설명 다음 장
    def descNext(self):
        global descWindow
        global descimgLabel
        global descFileNum
        descPath = "description/"
        
        descFileNum = descFileNum + 1
        if descFileNum > 10:
            descFileNum = 10
        
        descFile = str(descFileNum)+".png"
        fullDesc = descPath+descFile
        
        load = Image.open(fullDesc)
        load = load.resize((700, 450))
        render = ImageTk.PhotoImage(load)
        descimgLabel = tk.Label(descWindow, image=render)
        descimgLabel.image = render
        descimgLabel.place(x=50, y=0)

        

    # 파잉 열기
    def btton(self):
        self.button = tk.Button(self.labelFrame, text="Browse Afile", command=self.fileDailog)
        self.button.grid(column=1,row=1)
        
    def fileDailog(self):
        try :
            self.fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File",filetype=(("jpeg","*.jpg"),("png","*.png")))
            shutil.copy(self.fileName,"./image/myPhoto.jpg")

            img = Image.open(self.fileName)
            img = img.resize((350, 200))
            photo = ImageTk.PhotoImage(img)

            self.photolabel = Label(image=photo)
            self.photolabel.image = photo 
            self.photolabel.place(x=25,y=70)
        except:
            print("Forced termination of image file browse dialog")

    #녹음
    def startrecording(self):
        #녹음
        duration = 5
        fs = 16000
        rec = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        pcm = rec.tostring()
        with open('./audio/test.raw', 'wb') as w:
            w.write(pcm)
   
    #Etri 발음 교정 API
    def pronunciationC(self):
        #내가 녹음한 파일
        myaudioFile = "./audio/test.raw"
        #발음교정
        getText = questionText.get("1.0", "end")
        script = str(getText)
        script = script.replace("(an)","")
        
        # \n 안 지워주면 result -500 에러
        script = script.rstrip("\n")

        #이미지 경로
        winImg = "./image/win.jpg"
        loseImg = "./image/lose.jpg"
        imgDir = "./image/win.jpg"
        
        if os.path.isfile(myaudioFile):
            result = proCorrect(script)
            pronunciationText.delete(1.0,"end")
            pronunciationText.insert(1.0, "Your pronunciation score is "+ str(result))
            pronunciationText.tag_configure("center", justify='center')
            pronunciationText.tag_add("center", "1.0", "end")

            if result > 3:
                imgDir = "./image/win.jpg"
            else:
                imgDir = "./image/lose.jpg"

            self.rLoad = Image.open(imgDir)
            self.rLoad = self.rLoad.resize((350, 200))
            self.rRender = ImageTk.PhotoImage(self.rLoad)
            rlmg = tk.Label(self, image=self.rRender)
            rlmg.image = self.rRender
            rlmg.place(x=425, y=75)

            self.voiceRecog()
        else :
            questionText.delete(1.0,"end")
            questionText.insert(1.0, "The recording file does not exist")
            questionText.tag_configure("center", justify='center')
            questionText.tag_add("center", "1.0", "end")
        
    #ETRI 컴퓨터가 인식한 사용자의 발음 함수    
    def voiceRecog(self):
        myaudioFile = "./audio/test.raw"
        
        computerSentence = voiceRecognition(myaudioFile)
        fullSentence = "The computer recognized that you said\n "+computerSentence
        voiceRecogText.delete(1.0,"end")
        voiceRecogText.insert(1.0, fullSentence)
        voiceRecogText.tag_configure("center", justify='center')
        voiceRecogText.tag_add("center", "1.0", "end")
        

# /////////////////////
    #Etri 객체 검출 API
    def objectD(self):
        global questionText_list
        global question_list
        global questionNumber
        questionNumber = 0
        
        file = './image/myPhoto.jpg'
        
        #이미지 파일이 존재하는지
        if os.path.isfile(file):
            question_list = objectDetect(file)
            #이미지 파일에서 객체가 검출됬는가
            if not question_list:
                objectlistNum = "Detected 0 object"
                questionText_list.delete(1.0,"end")
                questionText_list.insert(1.0, objectlistNum)
                questionText_list.tag_configure("center", justify='center')
                questionText_list.tag_add("center", "1.0", "end")

                questionSentence = "Sorry I can't detect anything"
                questionText.delete(1.0,"end")
                questionText.insert(1.0, questionSentence)
                questionText.tag_configure("center", justify='center')
                questionText.tag_add("center", "1.0", "end")
            else:
                listLen = len(question_list)

                objectlistNum = "Detected " + str(listLen) + " objects"
                questionText_list.delete(1.0,"end")
                questionText_list.insert(1.0, objectlistNum)
                questionText_list.tag_configure("center", justify='center')
                questionText_list.tag_add("center", "1.0", "end")

                questionSentence = "I can see a(an) "+ str(question_list[questionNumber])
                questionText.delete(1.0,"end")
                questionText.insert(1.0, questionSentence)
                questionText.tag_configure("center", justify='center')
                questionText.tag_add("center", "1.0", "end")
            
        else:
            questionText.delete(1.0,"end")
            questionText.insert(1.0, "There is no Image")
            questionText.tag_configure("center", justify='center')
            questionText.tag_add("center", "1.0", "end")
    
    def prevB(self):
        global question_list
        global questionNumber
#         question_list = objectDetect()

        try:
            listLen = len(question_list)-1
            questionNumber = questionNumber - 1
            
            if questionNumber < 0:
                questionNumber = 0
                
            questionSentence = "I can see a(an) "+str(question_list[questionNumber])

            questionText.delete(1.0,"end")
            questionText.insert(1.0, questionSentence)
            questionText.tag_configure("center", justify='center')
            questionText.tag_add("center", "1.0", "end")

        except:
            print('no question_list')
        
    def nextB(self):
        global question_list
        global questionNumber
#         question_list = objectDetect()
        
        try :
            listLen = len(question_list)-1
            questionNumber = questionNumber +1

            if questionNumber > listLen:
                questionNumber = listLen
            
            questionSentence = "I can see a(an) "+str(question_list[questionNumber])

            questionText.delete(1.0,"end")
            questionText.insert(1.0, questionSentence)
            questionText.tag_configure("center", justify='center')
            questionText.tag_add("center", "1.0", "end")

        except:
            print("no question_list")



if __name__ == '__main__':
    
    #프로그램을 다시 실행할 때 이전에 사용하고 남은 이미지 삭제
    imagefile = './image/myPhoto.jpg'
    audiofile = './audio/test.raw'

    try:
        os.remove(imagefile)
        print("Remove!")
    except:
        pass
        
    try:
        os.remove(audiofile)
        print("Remove!")
    except:
        pass
    
    
    root = Root()
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()