from os import walk
import pygame


def import_folder(path, size: tuple) -> list:
    surface_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            changed_img = pygame.transform.scale(image_surf, size)
            surface_list.append(changed_img)

    return surface_list

def import_audio(path) -> list:
    audio_list = []
    for _, __, audio_files in walk(path):
        for audio in sorted(audio_files):
            full_path = path + '/' + audio
            audio_object = pygame.mixer.Sound(full_path)
            audio_list.append(audio_object)

    return audio_list
