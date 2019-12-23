import time, pygame
import RPi.GPIO as GPIO

nSongs = 16
currentSong = 1

pygame.mixer.init(44100, -16, 2, 4096)
pygame.mixer.music.set_volume(0.2)
# We need pygame.display.init() to use the pygame event queue.
# But remember to run this script as root to make this work on a headless Pi!
pygame.display.init() 

GPIO.setmode(GPIO.BCM)
btnNextPin = 17
btnPlayPin = 27
btnPrevPin = 22
btnVolUpPin = 23
btnVolDownPin = 24
ledPin = 4

paused = False

btnTime = time.time()

def btnPlayCallback(channel):
    global btnTime
    if time.time() - btnTime > 0.2:
        btnTime = time.time()
        print("btnPlay")
        global paused
        if pygame.mixer.music.get_busy() == False:
            paused = False
            playSong(currentSong)
            GPIO.output(ledPin, True)
        else:
            if paused == False:
                print("Pause")
                paused = True
                pygame.mixer.music.pause()
                GPIO.output(ledPin, False)
            else:
                print("Unpause")
                paused = False
                pygame.mixer.music.unpause()
                GPIO.output(ledPin, True)

def btnNextCallback(channel):
    global btnTime
    if time.time() - btnTime > 0.2:
        btnTime = time.time()
        print("btnNext")
        paused = False
        GPIO.output(ledPin, True)
        global currentSong
        currentSong = currentSong + 1
        if currentSong > nSongs:
            currentSong = 1
        pygame.mixer.music.stop()
        playSong(currentSong)
        GPIO.output(ledPin, True)

def btnPrevCallback(channel):
    global btnTime
    if time.time() - btnTime > 0.2:
        btnTime = time.time()
        print("btnPrev")
        paused = False
        GPIO.output(ledPin, True)
        global currentSong
        currentSong = currentSong - 1
        if currentSong < 1:
            currentSong = nSongs
        pygame.mixer.music.stop()
        playSong(currentSong)
        GPIO.output(ledPin, True)

def btnVolUpCallback(channel):
    print("btnVolUp")
    paused = False
    vol = pygame.mixer.music.get_volume() + 0.02
    if vol > 1:
        vol = 1
    print("Volume: " + str(vol))
    pygame.mixer.music.set_volume(vol)

def btnVolDownCallback(channel):
    print("btnVolDown")
    vol = pygame.mixer.music.get_volume() - 0.02
    if vol < 0:
        vol = 0
    print("Volume: " + str(vol))
    pygame.mixer.music.set_volume(vol)

def playSong(song):
    print("Playing song: " + str(song))
    pygame.mixer.music.load("/home/pi/" + str(song) + ".wav")
    pygame.mixer.music.play()
    nextSong = song + 1
    if nextSong > nSongs:
        nextSong = 1
    pygame.mixer.music.queue("/home/pi/" + str(nextSong) + ".wav")

GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, False)

GPIO.setup(btnPlayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btnPlayPin, GPIO.FALLING, callback = btnPlayCallback)

GPIO.setup(btnNextPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btnNextPin, GPIO.FALLING, callback = btnNextCallback)

GPIO.setup(btnPrevPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btnPrevPin,   GPIO.FALLING, callback = btnPrevCallback)

GPIO.setup(btnVolUpPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btnVolUpPin,   GPIO.FALLING, callback = btnVolUpCallback)

GPIO.setup(btnVolDownPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btnVolDownPin,   GPIO.FALLING, callback = btnVolDownCallback)

playSong(0)
while pygame.mixer.music.get_busy() == True:
    continue
GPIO.output(ledPin, True)
time.sleep(0.25)
GPIO.output(ledPin, False)

pygame.mixer.music.set_endevent(pygame.USEREVENT)

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                currentSong += 1
                if currentSong > nSongs:
                    currentSong = 1
                playSong(currentSong)
    except KeyboardInterrupt: # Ctrl+C
        print("Bye bye")
        GPIO.cleanup()
        exit()
