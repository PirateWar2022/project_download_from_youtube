# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from pytube import YouTube
from pytube import Stream
import os
import sys

class Prosses(QObject):

    length = QtCore.pyqtSignal(str, str, str)
    receiv = QtCore.pyqtSignal(int)


    def __init__(self, link='', output='', title=''):
        super().__init__()


        self.link = link
        self.video = YouTube(self.link)
        self.video1 = YouTube(self.link, on_progress_callback = self.on_progress)
        self.output = output

        # Empty string for files title
        self.title = title


    def get_files_titles(self):
        self.title = self.video.title
        self.title = self.title.replace('.', '')
        self.title = self.title.replace(' ', '')
        self.title = self.title.replace(':', '')

    def get_info(self, video):
        video_title = video.title
        video_description = video.description
        video_thumbnail = video.thumbnail_url

        self.length.emit(video_title, video_description, video_thumbnail)

    def download_video_720(self):
        self.get_files_titles()
        filters = self.video1.streams.filter(res='720p').first()
        try:
            filters.download(output_path=self.output, filename=f'{self.title}720.mp4')
        except:
            print('error')


    def download_video_480(self):
        self.get_files_titles()
        filters = self.video1.streams.filter(res='480p').first()
        filters.download(output_path=self.output,filename=f'{self.title}480.mp4')

    def download_video_360(self):
        self.get_files_titles()
        filters = self.video1.streams.filter(res='360p').first()
        filters.download(output_path=self.output,filename=f'{self.title}360.mp4')

    def download_video_1080(self):
        # Download
        self.get_files_titles()
        filters = self.video1.streams.order_by('resolution').desc().first()
        audio = self.video1.streams.get_audio_only()
        filters.download(output_path=self.output,filename='gvideo.mp4')
        audio.download(output_path=self.output, filename='gaudio.mp3')

        # Combine
        output_path = os.path.expanduser(self.output+f'\{self.title}1080.mp4')
        print(output_path)
        video_path = os.path.expanduser(self.output + '\gvideo.mp4')
        audio_path = os.path.expanduser(self.output + '\gaudio.mp3')
        combine = f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {output_path}'
        os.system(combine)

        # Remove
        os.remove(os.path.expanduser(self.output + '\gvideo.mp4'))
        os.remove(os.path.expanduser(self.output + '\gaudio.mp3'))


    def download_only_audio(self):
        video1 = YouTube(self.link, on_progress_callback=self.on_progress)
        self.get_files_titles()
        audio = video1.streams.get_audio_only()
        audio.download(output_path=self.output, filename=f'{self.title}_audio.mp3')


    def on_progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:

        filesize = stream.filesize
        bytes_received = filesize - bytes_remaining
        percent = int(round(100.0 * bytes_received / float(filesize), 0))
        self.receiv.emit(percent)
        print(percent)
        print(bytes_received, filesize)





