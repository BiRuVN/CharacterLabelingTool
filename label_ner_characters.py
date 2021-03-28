import os
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Label coordinate')
root.geometry('420x310')

# # Define dataset path and labels here
# label_folder = './data/training/cursor/seq_01/'

target_labels = {
    'not_address': 0,
    'address': 1
    # 'address': 3
}

sentence_index = 0

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return 'break'

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return 'break'

def select_all(event):
    event.widget.tag_add(SEL, "1.0", END)
    event.widget.mark_set(INSERT, "1.0")
    event.widget.see(INSERT)
    return 'break'

def get_sent_label(sent_idx):
	if not os.path.exists('./labels/{}.txt'.format(str(sent_idx))):
		with open('./labels/{}.txt'.format(str(sent_idx)), 'w+') as f:
			f.close()
	with open('./labels/{}.txt'.format(str(sent_idx)), 'r') as f:
		l = f.read()
		f.close()
	return l

def load_sentence(sent, sent_label=''):
    global sentence_frame, label_vars

    if sent_label == '':
    	sent_label = [0]*len(sent)

    load = list(current_sentence)

    sentence_frame = Frame(height=285, width=420, bg='green')
    sentence_frame.grid(row=0, column=0)
    sentence_frame.grid_propagate(False)
    label_vars = []

    print(current_sentence)
    print(load)
    row = 0
    column = 0
    for i in range(len(load)):
        column = i % 32
        row = int(i / 32)

        char_frame = Frame(sentence_frame)
        char_frame.grid(row=row, column=column)

        lbl = Label(char_frame, height=1, width=1, text=load[i])
        var = Text(char_frame, height=1, width=1)
        lbl.grid(row=0, column=0)
        var.grid(row=1, column=0)
        var.delete(1.0, END)
        var.insert(1.0, sent_label[i])

        var.bind("<Tab>", focus_next_widget)
        var.bind("<Shift-Tab>", focus_prev_widget)
        var.bind("<FocusIn>", select_all)
        label_vars.append(var)

    return label_vars

def render_sentence_holder(parent):
    global current_sentence, label_vars

    label_vars = load_sentence(current_sentence)

    progress_frame = Frame(parent)
    progress_frame.grid(row=1, column=0)

    progress_lbl = Label(progress_frame)
    progress_lbl.configure(text='{} of {}'.format(sentence_index+1, len(sentences)))
    progress_lbl.pack(side='bottom')
    
    return progress_lbl

def next_sent():
    global sentence_index, sentences, current_sentence, sentence_frame, label_vars
    global progress_lbl
    sentence_index += 1
    if sentence_index < len(sentences):
        with open('./labels/{}.txt'.format(str(sentence_index-1)), 'w+') as f:
            for v in label_vars:
                l = v.get(1.0, END).strip()
                f.write(l)
            f.close()
        
        current_sentence = sentences[sentence_index]
        for widget in sentence_frame.winfo_children():
            widget.destroy()
        label_vars = load_sentence(sent=current_sentence, sent_label=get_sent_label(sentence_index))
        
    else:
        sentence_index -= 1

    progress_lbl.configure(text='{} of {}'.format(sentence_index+1, len(sentences)))

def prev_sent():
    global sentence_index, sentences, current_sentence, sent_lbl, sentence_frame
    global progress_lbl
    sentence_index -= 1
    if sentence_index > -1:
        current_sentence = sentences[sentence_index]
        for widget in sentence_frame.winfo_children():
            widget.destroy()
        label_vars = load_sentence(sent=current_sentence, sent_label=get_sent_label(sentence_index))

    else:
        sentence_index += 1

    progress_lbl.configure(text='{} of {}'.format(sentence_index+1, len(sentences)))
    
def key_stroke(event):
    # while True:
    c = event.char
    if c == 'a':
        prev_sent()
        # break
    elif c == 'd':
        next_sent()
        # break

# get all sentences that need to be labeled
sentences = []
sentence_index = 0

with open('sentences.txt', 'r') as f:
    sentences = [x.strip() for x in f.read().split('\n')]
    f.close()

print('Got total {} sentences'.format(len(sentences)))

if not os.path.exists('./labels'):
	os.mkdir('labels')

current_sentence = sentences[sentence_index]
sent_lbl = None
# label_vars = load_sentence(current_sentence)
progress_lbl = render_sentence_holder(root)
root.bind('<Key>', key_stroke)

root.mainloop()

