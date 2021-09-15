from pocketsphinx import LiveSpeech

hmm = '/home/michaellimyuguang/pocket_test/en-us'
lm = '/home/michaellimyuguang/pocket_test/6402.lm.bin'
dict = '/home/michaellimyuguang/pocket_test/6402.dic'

speech = LiveSpeech(
verbose=False,
sampling_rate=16000,
buffer_size=2048,
no_search=False,
full_utt=False,
hmm=hmm,
lm=lm,
dic=dict
)

for phrase in speech:
    print("You said:")
    print(phrase)
