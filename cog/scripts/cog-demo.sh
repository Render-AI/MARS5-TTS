if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # ...
        echo "You're on Linux."
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
        echo "You're on MacOS."        
fi
cd mars5-tts/cog;
cog predict  -i 'text="Hey there, this is a test."'  -i 'ref_audio_file="https://files.catbox.moe/be6df3.wav"' -i $'ref_audio_transcript="This is text audio, generated with Mars5."'