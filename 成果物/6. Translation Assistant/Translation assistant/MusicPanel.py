# -*- coding: utf-8 -*-
"""
这个类负责所有和音乐有关的操作
"""
import wx
import pygame
import os


class MusicControl:
    MusicPath = ""
    musicList = []
    index = 0

    def __init__(self):
        pygame.mixer.init()
        # Music单独保存自己的路径，与工作相独立,存在默认播放路径
        self.MusicPath = "d:\\Music"
        self.musicList = \
            [self.MusicPath + '\\' + music for music in os.listdir(self.MusicPath) if music.endswith('.mp3')]

    def ChangeMusicFilePath(self):
        dlg = wx.DirDialog(None, u"更改音乐文件夹路径", style=wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.MusicPath = dlg.GetPath()
            self.musicList = \
                [self.MusicPath + '\\' + music for music in os.listdir(self.MusicPath) if music.endswith('.mp3')]
            self.index = 0
        dlg.Destroy()

    def PreviousMusic(self):
        self.index -= 1
        if self.index == -1:
            self.index = len(self.musicList)-1
        pygame.mixer.music.load(self.musicList[self.index])
        pygame.mixer.music.play()
        return self.musicList[self.index]


    def NextMusic(self):
        self.index += 1
        if self.index == len(self.musicList):
            self.index = 0
        pygame.mixer.music.load(self.musicList[self.index])
        pygame.mixer.music.play()
        return self.musicList[self.index]

    def StopMusic(self):
        pygame.mixer.music.stop()

    def PlayMusic(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.musicList[self.index])
            pygame.mixer.music.play(loops=0)
            return self.musicList[self.index]
        else:
            pygame.mixer.music.unpause()
            return self.musicList[self.index]
        pass

    def PauseMusic(self):
            pygame.mixer.music.pause()
    pass

    def ChangeVolume(self,volume):
        pygame.mixer.music.set_volume(volume)