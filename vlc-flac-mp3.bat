rem    does them all at once (CPU!)... and does not get ID3 tags

rem    run below in terminal in the folder with the flac files

# https://gist.github.com/asather/63cbea92ed6734f5ee70

for %i in (*.flac) do "C:\Program Files\VideoLAN\VLC\vlc.exe" --sout=#transcode{acodec=mp3,ab=192,channels=2,samplerate=44100}:file{dst="%~ni.mp3"} "%i" vlc://quit


