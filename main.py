


import kivy
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color

import random
import os


class tiles_lay(FloatLayout):
    def __init__(self, **kwargs):
        super(tiles_lay, self).__init__(**kwargs)
        #self.audios = os.listdir('audio')
        self.score_num =1

        self.score =Button(size_hint=(None, None), size= (80, 50), text='Score: 0',
                           pos=(0, Window.height-50))
        with self.canvas:
            Color(.8, .8, .8, 1)    
            self.rect = Rectangle(pos=(self.pos), size=(Window.size))

        global all_tiles
        all_tiles = self.children
        self.back_btn= Button(background_normal='', background_down='') 
        self.back_btn.bind(on_press=self.game_over)

        self.start_tiles()
    
    def start_tiles(self):
        self.add_widget(self.back_btn)
        self.tile_list = []

        self.btn_y = 0
        self.btn_width = Window.width/4
        self.btn_x = [self.btn_width*0, self.btn_width*1, self.btn_width*2, self.btn_width*3]
        
        global box_slide
        box_slide = BoxLayout(orientation='vertical', pos=(-Window.width, 0))
        
        with box_slide.canvas:
            Color(.2, .5, 1, .7)
            box_slide.rect1 = Rectangle(pos=(box_slide.pos), size=(Window.size))

        self.restart_btn = Button(text='Restart', size_hint=(None, None),
                                  pos_hint={'center_x': .5, 'center_y':.4})
        self.restart_btn.bind(on_press=self.game_over1)
        box_slide.add_widget(Label(text='Game Over', font_size=40,
                                  pos_hint={'center_x': .5, 'center_y':.7}))
        box_slide.add_widget(self.restart_btn)

        global slide_anim
        slide_anim = Animation(pos=(0, 0), d=1)
        
        for i in range(50):

            self.btn = btn(size_hint=(None, None), size=(self.btn_width, Window.height/4),
                                    pos=(random.choice(self.btn_x), Window.height+self.btn_y))

            self.btn_y += self.btn.height
##            self.btn.bind(on_press=self.play_sound)
            self.add_widget(self.btn)
            self.btn.bind(on_press=self._state)

        self.add_widget(box_slide)
        self.add_widget(self.score)

        for child in self.children:

            if child != box_slide and child != self.back_btn and child != self.score:
                self.time = (child.y + Window.height/4) / 200
                global anim
                anim = Animation(y=-(Window.height/4), d=self.time)

                self.tile_list.append(child)
                
                anim.start(child)
                anim.fbind('on_complete', self.delete_btn)
            else:
                pass        

    def play_sound(self, btn):
        if btn.state == 'down':
            pass
            #self.sound = SoundLoader.load(random.choice(self.audios))
            if self.sound.status != 'stop':
                self.sound.stop()
            self.sound.play()
            
    
    def delete_btn(self, anim, btn):
        self.remove_widget(btn)
        if self.tile_list.index(btn) == 0:
            #means the last tile has finish animation
            self.clear_widgets()
            self.start_tiles()

    def game_over1(self, *args):
        self.score.text = 'Score: 0'
        self.score_num = 1
        self.clear_widgets()
        self.start_tiles()

    def game_over(self, *args):
        for child in all_tiles:
            anim.cancel_all(child)
            
        #play a sound
#        self.sound = SoundLoader.load('12914_sweet_trip_mm_kick_lo.wav')
#        if self.sound.status != 'stop':
#            self.sound.stop()
#        self.sound.play()
        slide_anim.start(box_slide)
        slide_anim.start(box_slide.rect1)

    def _state(self, btn):
        if btn.state == 'down':
            self.score.text = 'Score: ' + str(self.score_num)
            self.score_num += 1
                

        
class btn(ToggleButton):
    def __init__(self, **kwargs):
        super(btn, self).__init__(**kwargs)
        global game_over
        game_over = False
        self.allow_no_selection = False


        self.btn_width = Window.width/4
        self.btn_x = [self.btn_width*0, self.btn_width*1, self.btn_width*2, self.btn_width*3]
                      
        self.size_hint=(None, None)
        size=(self.btn_width, Window.height/4)

    def on_pos(self, btn, pos):
        if btn.y <= 0 and btn.state == 'normal':
            for child in all_tiles:
                anim.cancel_all(child)
            
            #play a sound
            self.sound = SoundLoader.load('12914_sweet_trip_mm_kick_lo.wav')
            if self.sound.status != 'stop':
                self.sound.stop()
            self.sound.play()
            slide_anim.start(box_slide)
            slide_anim.start(box_slide.rect1)
            
        else:
            pass



class Piano_Tiles(App):
    def build(self):
        return tiles_lay()

Piano_Tiles().run()
