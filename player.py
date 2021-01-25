from tkinter import *
from ttkthemes import themed_tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import messagebox
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import os
import vlc
import time

# using adapta theme to give a new look to widgets 
root = themed_tk.ThemedTk(theme='adapta')
root.title('Fly-beats')
root.geometry('770x514')
root.maxsize(770,514)
root.minsize(770,514)
root.configure(background='#F0F2F6')

# adding icon
root.iconphoto(False, PhotoImage(file='images/icon final.png').subsample(2,2))

# reading images for play, pause, previous, next
play_image = PhotoImage(file='images/play final.png').subsample(32,32)
pause_image = PhotoImage(file='images/pause final.png').subsample(32,32)
play_prev = PhotoImage(file='images/play previous.png').subsample(7,7)
play_next = PhotoImage(file='images/play next.png').subsample(7,7)



# varibles -------------------------------------------------------------------------------------------------
flag = {'val':0}
default_volume = {'vol':50}
time_dict = {'current':0, 'length':1}
prev_dir = {'val':''}



# functions ------------------------------------------------------------------------------------------------
def play_pause():
    '''
       This function changes the play and pause icon. 
       If song is playing, it shows pause button to pause
       and vice versa. 
    '''
    if p.is_playing():
        play_button.config(image=play_image)
    else:
        play_button.config(image=pause_image)



def play_time():
    '''
       This function show the current running time of song.
       It changes the time every second.
       It also plays next song if the current songs is over.
    '''
    global current_time
    # getting current time in seconds
    current_time = int(p.get_time()/1000)
    time_dict['current'] = current_time

    # converting time in M:S format
    real_time = time.strftime('%M:%S', time.gmtime(current_time)) 

    # updating time status 
    status_time.config(text=real_time)
    status_time.after(1000, play_time)
    slider.config(value=current_time)

    # if current time is equal to song length then play next song
    if time_dict['current'] == time_dict['length']:
        next()   
     
     

def song_length(index):
    '''
       This function takes index of the song and shows the total length.
       Length format is MM:SS
    '''
    # getting song extension
    tag = lb.get(index)[-4:]
    global total_length

    # total length of mp3 song
    if '.mp3' == tag:
        s = directory + '/' + lb.get(index)
        audio = MP3(s)
        total_length = int(audio.info.length)
        time_dict['length'] = total_length
        real_length = time.strftime('%M:%S', time.gmtime(total_length))
        total_time.config(text=real_length)

    # total length of m4a song    
    elif '.m4a' == tag:
        s = directory + '/' + lb.get(index)
        audio = MP4(s)
        total_length = int(audio.info.length)
        time_dict['length'] = total_length
        real_length = time.strftime('%M:%S', time.gmtime(total_length))
        total_time.config(text=real_length)  
    slider.config(to=total_length)   
     


def manipulate(index):
    '''
       This function shows the name of current song.
       Also it handles the play of song.
    '''
    song_name = lb.get(index)[:-4]

    # write full song name if it contains character less than 30
    if len(song_name) < 30:
        lb_item.config(text=song_name)
    else:
        s_name = song_name[:27]+'...'
        lb_item.config(text=s_name)    
    song = directory + '/' + lb.get(index)
    global p

    # playing and stoping
    if flag['val'] == 0:
        p = vlc.MediaPlayer(song)
        p.play()
        flag['val'] += 1
    else:
        p.stop()
        p = vlc.MediaPlayer(song)
        p.play()
    p.audio_set_volume(default_volume['vol'])

    # function call to get the play time of current/choosen song
    play_time()

    # function call to get the current song length
    song_length(index) 



def select_item(event):
    '''
       This function selects song from listbox and
       then it plays it.
    '''
    global index
    try:
        index = lb.curselection()
        manipulate(index)
        
        # function call to change play and pause icon
        play_pause()
    except Exception:
        pass     
   


def add_playlist():
    '''
       This function asks to select playlist folder.
    '''
    global directory
    global last_song_index
    # asking for song directory
    directory = filedialog.askdirectory(title='Choose directory')
    try:
        if directory != '':
            # list down all the content in the choosen directory
            lst = os.listdir(directory)
            lb.delete(0, END)
            lb_item.config(text='Choose song')

            # adding item to listbox
            for i in lst:
                if ('.mp3' in i) or ('.m4a' in i):
                    last_song = i
                    lb.insert(END, i)
            if lb.size() > 0:        
                last_song_index = lb.get(0, END).index(last_song)  
            if lb.size() == 0:
                # show message if the folder does not have any song
                messagebox.showinfo(title='Empty -(Fly beats)', message='This folder is empty!\nPlease select another folder.')  
                add_playlist()  
            prev_dir['val'] = directory       
        else:
            path_error = 'Choose a valid path!'
            messagebox.showerror(title='Path error -(Fly beats)', message=path_error)
            directory = prev_dir['val']
    except Exception:
        pass         


   
def pause():
    '''
       This function pause the current song.
    '''
    try:
        p.pause()
        play_pause()   
    except Exception:
        pass 



def volume_adjust(s):
    '''
       This function helps to adjust volume.
    '''
    try:
        default_volume['vol'] = 100-int(volume_slider.get())
        p.audio_set_volume(default_volume['vol'])        
    except Exception:
        pass 



def next():
    '''
       This function plays the next song.
    '''
    try:
        # getting index of next song
        index = lb.curselection()
        index = index[0]+1
        if (index <= last_song_index):
            # passing index of next song to play 
            manipulate(index)
            lb.select_clear(0, END)
            lb.activate(index)
            lb.selection_set(index, last=None)
            play_pause()

    except Exception:    
        pass



def previous():
    '''
       This function plays the previous song.
    '''
    try:
        # getting index of previous song
        index = lb.curselection()
        index = index[0]-1
        if index >= 0:
            # passing index of previous song to play
            manipulate(index)
            lb.select_clear(0, END)
            lb.activate(index)
            lb.selection_set(index, last=None)  
            play_pause()  

    except Exception:   
        pass


       
def slide(x):
    '''
       This function is used by slider to change the song position.
    '''
    try:
        # getting slider value
        slide_position = slider.get()
        to_set = slide_position / total_length

        # set song to slider value
        p.set_position(to_set)
        slider.config(value=slide_position)
    except Exception:
        pass 


# UI designing ---------------------------------------------------------------------------------------------
# image for left frame
img = PhotoImage(file='images/logo image.png').subsample(2,2)

# creating frames
# left frame
left_frame = Frame(root, width=400, height=500, background='#F0F2F6', bd=0)
left_frame.grid(row=0, column=0)
left_frame.config(highlightthickness=0, borderwidth=0)

# right frame
right_frame = Frame(root, width=500, height=500, background='#F0F2F6', bd=0)
right_frame.grid(row=0, column=1)

Label(left_frame, image=img, bg='#F0F2F6').pack()

first_frame = Frame(right_frame, width=500, height=50, background='#F0F2F6')
first_frame.pack(anchor='nw', pady=8)

second_frame = Frame(right_frame, width=500, height=400, background='#F0F2F6')
second_frame.pack(anchor='nw')

third_frame = Frame(right_frame, width=500, height=400, background='#F0F2F6', pady=15)
third_frame.pack(anchor='nw')


# creating add playlist button
Button(first_frame, text='+ Add folder', background='#5E17EB', borderwidth=0,foreground='white', pady=8, font='ubuntu 10 bold',
       command=add_playlist, activebackground='#5E17EB', activeforeground='white').grid(row=0,column=0)

# volume slider
volume_slider = ttk.Scale(first_frame, from_=0, to=100, length=80, command=volume_adjust,
                          value=default_volume['vol'], orient=VERTICAL)
volume_slider.grid(row=0, column=2, sticky='ne')
Label(first_frame, text='', bg='#F0F2F6', padx=100).grid(row=0, column=1)

Label(second_frame, text = 'Songs', bg='#F0F2F6', fg='#545454', pady=15, font='ubuntu 10 bold').pack(anchor='nw', side=TOP)       


# creating listbox and scrollbar 
sb = Scrollbar(second_frame, orient=VERTICAL, borderwidth=0, width=8, troughcolor='white', bg='#ffafd7',
               activebackground='#ffafd7')
lb = Listbox(second_frame,height=12, font='ubuntu 10', fg='#545454', width=40,
             selectbackground='#ffafd7', activestyle=NONE, yscrollcommand=sb.set)
lb.config(highlightthickness=0, highlightbackground='grey', foreground='#545454', bd=0)             

sb.config(command=lb.yview)
sb.pack(side=RIGHT, fill=Y)

# show item when release button
lb.bind('<ButtonRelease-1>', select_item)         
lb.pack()

# displaying choosen song name
lb_item = Label(third_frame, text='Fly Beats', font='ubuntu 15', bg='#F0F2F6', fg='#545454')
lb_item.grid(row=0, column=0, columnspan=4, sticky='nw', pady=10)

# label for song status
status_time = Label(third_frame, text='00:00', bg='#F0F2F6', font='ubuntu 10', fg='#545454')
status_time.grid(row=1, column=0, sticky='nw') 

# label for song total length
total_time = Label(third_frame, text='00:00', bg='#F0F2F6', font='ubuntu 10', fg='#545454')
total_time.grid(row=1, column=2, sticky='ne')

# slider for changing song position
slider = ttk.Scale(third_frame, from_=0, to=100, length=325, command=slide)
slider.grid(row=2, column=0, columnspan=3)

# play and pause button
play_button = Button(third_frame, command=pause, image=play_image, bg='#F0F2F6', 
       borderwidth=0, activebackground='#F0F2F6', highlightthickness=0)
play_button.grid(row=3, column=1, sticky='news',pady=15)

# prev and next buttons
Button(third_frame, image=play_prev, font='ubuntu 20 bold', bg='#F0F2F6', command=previous,
       borderwidth=0, activebackground='#F0F2F6', highlightthickness=0).grid(row=3, column=0, sticky='ne', pady=15, padx=15) 
Button(third_frame, image=play_next, font='ubuntu 20 bold', bg='#F0F2F6', command=next,
       borderwidth=0, activebackground='#F0F2F6', highlightthickness=0).grid(row=3, column=2, sticky='nw', pady=15, padx=15)    
       
root.mainloop()