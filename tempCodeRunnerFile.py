ixer.music.load('temp.mp3')
            mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(temp.mp3)