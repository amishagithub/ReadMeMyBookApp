import os
import time
import img2pdf
from PIL import Image
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path

request_permissions([
    Permission.CAMERA,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.READ_EXTERNAL_STORAGE
])

class IntroScreen(Screen):
    pass

class SecondScreen(Screen):
    count = 0
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("/storage/emulated/0/DCIM/IMG_{}.jpg".format(SecondScreen.count))
        SecondScreen.count=SecondScreen.count+1
	
class ThirdScreen(Screen):
    def createpdf(self):                                    
        path="/storage/emulated/0/DCIM/"
        list=os.listdir(path)
        newList=[path+x for x in list if x.endswith('.jpg')]
        pdf=img2pdf.convert(newList)
        file=open("/storage/emulated/0/DCIM/TestPdf.pdf","wb")
        file.write(pdf)
        file.close()

class FourthScreen(Screen):
    pass

class FifthScreen(Screen):
    def delete(self):                                   
        path="/storage/emulated/0/DCIM/"
        list=os.listdir(path)
        newList=[path+x for x in list if x.endswith('.jpg')]
        num = self.ids.input.text
        os.remove(newList[int(num)-1])
        newList.pop(int(num)-1)
        pdf=img2pdf.convert(newList)
        file=open("/storage/emulated/0/DCIM/TestPdf.pdf","wb")
        file.write(pdf)
        file.close()

class SixthScreen(Screen):
    pass

class SeventhScreen(Screen):
    def on_enter(self, *args):
        read = 0
        read = self.manager.get_screen("sixth").ids.my_text.text
        path="/storage/emulated/0/DCIM/"
        list=os.listdir(path)
        newList=[path+x for x in list if x.endswith('.jpg')]
        self.ids.imageView.source = newList[int(read)-1]
	
class MyManager(ScreenManager):
    pass

kv = Builder.load_string("""
MyManager:
	IntroScreen:
	SecondScreen:
	ThirdScreen:
	FourthScreen:
	FifthScreen: 
	SixthScreen:
	SeventhScreen:   
<IntroScreen>:
	name:"intro"	
	background_color: (72/255, 219/255, 200/255, 1)
	canvas.before:
		Color:
			rgba: root.background_color
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation: "vertical"
		size: root.width, root.height		
		padding: 50
		spacing: 20
		Label:
			markup:True
			text:"[b][i]Welcome To Read Me My Book[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:70
			color:(118/255,56/255,217/255,1)
		Button:
			markup:True
			text:"[i]Start Scanning[/i]"
			font_size:70
			size_hint:(None,None)
			width:900
			height:200
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				app.root.current= "second"
				root.manager.transition.direction = "left"		
		Button:
			markup:True
			text:"[i]Quit[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: app.stop()
<SecondScreen>:
	name:"second"
	BoxLayout:
		orientation:'vertical'
		Camera:
			index:0
			id: camera
			resolution:(640,480)
			play:True
			allow_stretch:True
			canvas.before:
				PushMatrix
				Rotate:
					angle:-90
					origin:self.center
			canvas.after:
				PopMatrix			
		Button:
			text: 'Click to Take Image'
			size_hint_y: None
			height: '48dp'
			on_press: root.capture()
		Button:
			text: 'Next'
			size_hint_y:None
			height: '48dp'
			on_press:    
				app.root.current= "third"
				root.manager.transition.direction = "left"
<ThirdScreen>:
	name:"third"    
	background_color: (72/255, 219/255, 200/255, 1)
	canvas.before:
		Color:
			rgba: root.background_color
		Rectangle:
			size: self.size
			pos: self.pos   
	BoxLayout:
		orientation: "vertical"
		size: root.width, root.height   	
		padding: 50
		spacing: 20   		
		Label:
			markup:True
			text:"[b][i]PDF Generation Tool[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:70
			color:(118/255,56/255,217/255,1)         
		Button:
			markup:True
			text:"[i]Create Pdf[/i]"
			font_size:70
			size_hint:(None,None)
			width:800
			height:200
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				root.createpdf()
				app.root.current= "fourth"
				root.manager.transition.direction = "left"
		Button:
			markup:True
			text:"[i]Back[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100	
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				app.root.current= "second"
				root.manager.transition.direction = "right"
<FourthScreen>:
	name: "fourth"
	background_color: (72/255, 219/255, 200/255, 1)
	canvas.before:
		Color:
			rgba: root.background_color
		Rectangle:
			size: self.size
			pos: self.pos   
	BoxLayout:
		orientation: "vertical"
		size: root.width, root.height   	
		padding: 50
		spacing: 20           
		Label:
			markup:True
			text:"[b][i]PDF Created in DCIM[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:70
			color:(118/255,56/255,217/255,1)   
		Label:
			markup:True
			text:"[b][i]Choose something from here or Quit[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:50
			color:(118/255,56/255,217/255,1)
		Button:
			markup:True
			text:"[i]Update Pdf[/i]"
			font_size:70
			size_hint:(None,None)
			width:800
			height:200
			pos_hint:{'center_x':0.5,'center_y':0.3}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				app.root.current= "second"
				root.manager.transition.direction = "right"          
		Button:
			markup:True
			text:"[i]Delete a page of pdf[/i]"
			font_size:50
			size_hint:(None,None)
			width:800
			height:200
			pos_hint:{'center_x':0.5,'center_y':0.6}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				app.root.current= "fifth"
				root.manager.transition.direction = "left"  
		Button:
			markup:True
			text:"[i]Read a page of pdf[/i]"
			font_size:50
			size_hint:(None,None)
			width:800
			height:200
			pos_hint:{'center_x':0.5,'center_y':0.6}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: 
				app.root.current= "sixth"
				root.manager.transition.direction = "left" 				              
		Button:
			markup:True
			text:"[i]Quit[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press: app.stop()
            
<FifthScreen>:
	name:"fifth"
	background_color: (72/255, 219/255, 200/255, 1)
	canvas.before:
		Color:
			rgba: root.background_color
		Rectangle:
			size: self.size
			pos: self.pos    
	BoxLayout:
		orientation: 'vertical'      
		padding: 50
		spacing: 20                  
		Label:
			markup:True
			text:"[b][i]Enter a page number to delete[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:70
			color:(118/255,56/255,217/255,1)
		TextInput:
			id:input
			size_hint_y:None
			height:150
			size_hint_x:None
			width:600  
			pos_hint:{'center_x':0.5,'center_y':0.5}    
		Button:
			markup:True
			text:"[i]Delete[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press:
				root.delete()
				app.root.current= "fourth"
				root.manager.transition.direction = "right"               
		Button:
			markup:True
			text:"[i]Back[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press:                 
				app.root.current= "fourth"
				root.manager.transition.direction = "right"      
<SixthScreen>:
	id:sixth
	name:"sixth"
	background_color: (72/255, 219/255, 200/255, 1)
	canvas.before:
		Color:
			rgba: root.background_color
		Rectangle:
			size: self.size
			pos: self.pos    
	BoxLayout:
		orientation: 'vertical'      
		padding: 50
		spacing: 20                  
		Label:
			markup:True
			text:"[b][i]Enter a page number to read[/i][/b]"
			background_color: (72/255, 219/255, 200/255, 1)
			canvas.before:
				Color:
					rgba: root.background_color
				Rectangle:
					size: self.size
					pos: self.pos
			pos_hint:{'center_x':0.5}
			font_size:70
			color:(118/255,56/255,217/255,1)
		TextInput:
			id:my_text
			size_hint_y:None
			height:150
			size_hint_x:None
			width:600  
			pos_hint:{'center_x':0.5,'center_y':0.5}    
		Button:
			markup:True
			text:"[i]Read[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press:
				app.root.current="seventh"
				root.manager.transition.direction="left"           
		Button:
			markup:True
			text:"[i]Back[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press:                 
				app.root.current= "fourth"
				root.manager.transition.direction = "right"      
	
<SeventhScreen>:
	name:"seventh"
	BoxLayout:
		orientation: 'vertical'      
		padding: 50
		spacing: 20
		
		Image:
			id:imageView
			source:'<random_name>.jpg'   
			allow_stretch:True
			keep_ratio:True   
			
		Button:
			markup:True
			text:"[i]Back[/i]"
			font_size:70
			size_hint:(None,None)
			width:400
			height:100
			pos_hint:{'center_x':0.5}
			color:(0/255,250/255,0/255)
			background_color:(235/255,79/255,52/255)
			on_press:                 
				app.root.current= "fourth"
				root.manager.transition.direction = "right"      
""")

class AwesomeApp(App):
    def build(self):
        return kv

if __name__=="__main__":
    AwesomeApp().run()
    

