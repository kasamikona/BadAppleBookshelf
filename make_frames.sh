cd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
dest=$PWD/frames
mkdir $dest
ffmpeg -i input.mp4 -f lavfi -i color=#666666:s=48x24 -f lavfi -i color=black:s=48x24 -f lavfi -i color=white:s=48x24 -filter_complex fps=20,scale=48x24,threshold "$dest/frame_%04d.png"
