from pytube import Playlist

playlist = Playlist('https://www.youtube.com/watch?v=yubJ_KuW_3I&list=PLkVMKZ6ot8T8da3UL_cxXwwBLFNJirqWL&ab_channel=LosPajaritosdeTacupa-Topic')
print('Number of videos in playlist: %s' % len(playlist.video_urls))

i = 1
for video in playlist.videos:
    # download mp3 in music folder if title is not already in music folder
    print(f'Downloading {video.title} ({i}/{len(playlist.video_urls)})')
    f = video.streams.filter(only_audio=True).first()
    if f is not None:
        f.download(output_path='music')
        # change file extension from mp4 to mp3
        default_filename = f.default_filename
        new_filename = default_filename.replace('.mp4', '.mp3')
        # rename file
        import os
        os.rename(f'music/{default_filename}', f'music/{new_filename}')
    else:
        print(f'Could not download {video.title}')
    i += 1
