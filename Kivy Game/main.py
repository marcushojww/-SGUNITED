import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import random


class Mask(Widget):

     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask_x = Window.width + 100 + Window.width/10
        self.mask_y = Window.height / 2

class Pipe(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipe_texture = Image(source = "covid.png").texture
        self.pipe_texture.wrap = 'repeat'
        self.pipe_texture.uvsize = (1, -3)

        self.gap_size = 120 
        #standardize the gap_size for all pipe widgets

        self.bottom_pipe_height = random.randrange(30, 300, 60) 
        #randomize the bottom pipe height from 30 - 300 with step 60



class Background(Widget):
    singapore_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    #for textures, need to use an object property
    #initializing these attributes in the Background class which will automatically create instance attributes
    #assign it to a property so I can dispatch it and redraw the textures
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Create textures
        self.floor_texture = Image(source="woodfloor.png").texture
        #takes away the texture from the image
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)
        #uvsize basically allows u to choose how many times you want it to be repeated in the x-direction, y-direction
        #-1 inverts the image because its uploaded upside down

        self.singapore_texture = Image(source="sin.png").texture 
        self.singapore_texture.wrap = 'repeat'
        self.singapore_texture.uvsize = (Window.width / self.singapore_texture.width, -1)

    def scroll_textures(self, time_passed):
        #make a texture scroll by updating its uvpos attribute, then telling the textures parent widget that it should be redrawn

        #update uvpos of textures
        self.floor_texture.uvpos = (self.floor_texture.uvpos[0] + time_passed/4,self.floor_texture.uvpos[1])

        self.singapore_texture.uvpos = (self.singapore_texture.uvpos[0] + time_passed/4,self.singapore_texture.uvpos[1])
        #updating the x-coordinate of the uvpos with the argument time_passed
        #can change the speed of scrolling by manipulating the time_passed increment 

        #redraw the texture
        drawfloor = self.property("floor_texture")
        drawfloor.dispatch(self)
        
        drawsg = self.property("singapore_texture")
        drawsg.dispatch(self) 
        
    

class Merlion(Image):
    def on_touch_down(self,touch):
        self.velocity = 150
        

class Covid(Image):
    pass


class MainApp(App):
    #no build() method as it is not needed
    #if build() is not manually called already, the app will load its config, call load_kv() 
    #and finally call self.build and set the root widget to the return value of self.build()
    #so what load_kv() does is it calls Builder.load_file()
    #Builder.load_file() parses the kv file and if there is a root widget in the kv file,
    #Builder.load_file() will instantiate and construct that widget and return it as the return value of Builder.load_file
    #in this case FloatLayout is the root attribute of the MainApp class

    #assign these class variables as False
    #I let them be class variables as 
    #these variables will be used below to update the score for the application
    was_colliding = False
    was_collide = False

    def on_start(self): #when the application starts running


        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60) 
        #this was a mistake assigning it to the attribute self.nextframe
        #whenever app starts, call the function once every 1/60 seconds and provides the time passed as the argument for the function
        #makes the scrolling of textures smoother

        pipe1 = self.root.ids.pipe1
        pipe2 = self.root.ids.pipe2
        pipe3 = self.root.ids.pipe3
        pipe4 = self.root.ids.pipe4
        pipe5 = self.root.ids.pipe5
        #define pipe list
        self.pipe_list = [pipe1, pipe2, pipe3,pipe4,pipe5] 
        #remove pipe widget
        for pipe in self.pipe_list: 
            self.root.remove_widget(pipe)
        #remove mask widget
        self.mask = self.root.ids.mask
        self.root.remove_widget(self.mask)

        #removing of widgets is redundant as the x coordinate pos of the widgets is >= Window.width
        #should have created pipe attributes to the instance by using eg self.pipe1 = self.root.ids.pipe1
    

    def start_game(self): #after button is pressed
        #reset score to 0 when button is pressed
        self.root.ids.score.text = "0"

        #use of kivy clock module to call a method and give time passed as an argument
        self.nextframe = Clock.schedule_interval(self.next_frame, 1/60)

        pipe1 = self.root.ids.pipe1
        pipe2 = self.root.ids.pipe2
        pipe3 = self.root.ids.pipe3
        pipe4 = self.root.ids.pipe4
        pipe5 = self.root.ids.pipe5

        #reupdate the x-coordinate pos of the pipes when game starts
        pipe1.x = Window.width
        pipe2.x = Window.width + self.root.ids.pipe1.size[0] + Window.width / 5
        pipe3.x = Window.width + 2* self.root.ids.pipe1.size[0] + 2* Window.width / 5
        pipe4.x = Window.width + 3* self.root.ids.pipe1.size[0] + 3* Window.width / 5
        pipe5.x = Window.width + 4* self.root.ids.pipe1.size[0] + 4* Window.width / 5
        for pipe in self.pipe_list: #add pipe widgets after button is pressed
            self.root.add_widget(pipe)

        #reupdate pos of mask
        self.mask = self.root.ids.mask
        self.root.add_widget(self.mask)
        self.mask.x = Window.width + 100 + Window.width/10


    def next_frame(self, time_passed):
        #Clock.schedule_interval basically calls this function 60 times per second to check update the pos of the pipes (allowing it to move)
        # and changing the x coordinate pos of the left most pipe once the right most pipe is at a certain x coordinate position

        #move pipes
        for pipe in self.pipe_list:
            pipe.x -= time_passed * 100

        #to enable the pipe widgets to come back onto the screen to allow an infinite cycle of pipe widgets, equal distance apart
        #create a list of pipe.x so I may compare the values of pipe.x
        #list is continuously renewed every time the function is called so it may check the current pipe.x value of each pipe
        pipex_list = []

        for pipe in self.pipe_list:
            pipex_list.append(pipe.x)

        right_most_x = max(pipex_list) #right_most_x = the highest value of pipe.x within the pipex_list
        if right_most_x <= Window.width - self.root.ids.pipe5.size[0] - Window.width/5:
            most_left_pipe = self.pipe_list[pipex_list.index(min(pipex_list))] #get the index of the lowest pipe.x and using that index, get the pipe with the lowest pipe.x and assign it to most_left_pipe
            most_left_pipe.x = Window.width #manually change the x-coordinate pos of the most_left_pipe to the width of the Window to ensure continuous flow of pipes

        #move merlion
        GRAVITY = 300
        merlion = self.root.ids.merlion
        merlion.y = merlion.y + merlion.velocity * time_passed
        merlion.velocity = merlion.velocity - GRAVITY * time_passed 
        #as time passes and screen is not touched, the velocity will decrease until it becomes negative
        #negative velocity would then decrease y coordinate pos of merlion
        #when button is pressed, merlion.velocity = 150
        

        #move mask
        mask = self.root.ids.mask
        mask.x -= time_passed * 100
        if mask.x <= -mask.size[0]:
            mask.x = Window.width/10 - 70 + 4*self.root.ids.pipe1.size[0] + 3* Window.width/5 + Window.width/10
            mask.opacity = 1 #need to change the opacity to 1 since mask opacity becomes 0 when mask widget collides with merlion widget

        self.check_collision()
        #call this function as well to check for collisions


    def check_collision(self):
        #initialize the variables as False
        #these variables are bolean values to determine if the merlion widget collides with the Pipe/Mask widget
        is_colliding = False
        is_collide = False

        #redundant code if I created the instance attributes using self.___ at the on_start(self) method
        merlion = self.root.ids.merlion
        self.mask = self.root.ids.mask

        for pipe in self.pipe_list: #need to create for loop as we have 5 pipe widgets in the pipe_list
            if pipe.collide_widget(merlion): 
                #is_colliding = True #this is WRONG, should use an else statement such that when the merlion is between the top&btm pipe, is_colliding = True
                if merlion.y < pipe.bottom_pipe_height + 70 : 
                    self.game_over()
                elif merlion.top > pipe.bottom_pipe_height + self.root.ids.pipe1.gap_size + 70: #y coordinate of the top of merlion instead of bottom left of merlion
                    self.game_over()
                else:
                    is_colliding = True
            else: #if merlion widget DOES NOT collide with pipe widget, check if the merlion collides with the ground or the ceiling 
                if merlion.y < 70:
                    self.game_over()
                elif merlion.top > Window.height:
                    self.game_over()
            #should have put this code outside of the for loop because it does not belong here
            #eitherways if the merlion collides with the ground / ceiling, the game would be over, hence making a condition where it does not collide with the pipe is not necessary

        #update the score whenever the merlion collides with the pipe 
        if not self.was_colliding and is_colliding: #if was_colliding = False & is_colliding = True, score + 1, hence as when it first collides w the widget, score increases by 1
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1) 
        self.was_colliding = is_colliding 
        #set was_colliding to the same bolean value as is_colliding so the score does not continually increase
        #hence was_colliding = True while merlion is colliding with the pipe widget
        #when the merlion stops colliding with the pipe widget, is_colliding = False as assigned in this method and hence was_colliding also = False

        #check if merlion collides with mask, if yes, update is_collide variable and change opacity of mask to 0
        if merlion.collide_widget(self.mask):
            is_collide = True
            self.root.ids.mask.opacity = 0

        #update score when merlion collides with mask
        if not self.was_collide and is_collide:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 10)
        self.was_collide = is_collide
            
           

    def game_over(self):
        #reupdate pos of merlion
        self.root.ids.merlion.pos = (100, Window.height / 2)

        #remove pipe widgets
        for pipe in self.pipe_list:
            self.root.remove_widget(pipe)

        #remove mask widget
        self.root.remove_widget(self.mask)

        #stop clock interval
        self.nextframe.cancel()
        
        #enable button
        self.root.ids.button.disabled = False
        self.root.ids.button.opacity = 1
        
    

MainApp().run()