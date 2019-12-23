# RasPiAudioPlayer
Use a Raspberry Pi and 5 buttons (start/pause, next, previous, vol +, vol -) as an audio player. An LED lights up when a sound is playing. Songs are played automatically after another.

I tested this on a Raspberry Pi Zero W, with Raspbian Buster Lite (2019-09-26)

## Things you need (to do)
1. Several audio files
  * Name your audio files `1.wav`, `2.wav`, `3.wav`, etc, in the order you want them to de played.
  * A file named `0.wav` will be played upon start.
  * The code assumes you make use of .wav files. If you use other formats, you have to change this on two lines in the `playSong()` function. 
  * You have to manually define the number of songs (excluding the startup song) in the `nSongs` variable. I might consider this to be done automagically in a future version.

2. Five buttons and an LED
  * Check the code for the GPIO pins to connect them to.
