import pygame


class SoundService:

    @classmethod
    def play_clik_sound(cls):
        click_sound = pygame.mixer.Sound("resource/audio/effect1.wav")
        click_sound.set_volume(0.1)
        pygame.mixer.Sound.play(click_sound)

    @classmethod
    def play_bgm(cls):
        """
        pygame init 후 실행해야 한다.
        """
        pygame.mixer.music.load("resource/audio/bgm.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
