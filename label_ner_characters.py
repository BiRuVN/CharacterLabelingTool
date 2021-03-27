import os
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Label coordinate')
root.geometry('650x250')

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

def load_sentence(sent):
    global load, sentence_frame
    load = [x for x in current_sentence]

    sentence_frame = Frame(height=200, width=650, bg='green')
    sentence_frame.grid(row=0, column=0)
    sentence_frame.grid_propagate(False)
    vars = []

    print(current_sentence)
    print(load)
    row = 0
    column = 0
    for i in range(len(load)):
        column = i % 50
        row = int(i / 50)

        char_frame = Frame(sentence_frame)
        char_frame.grid(row=row, column=column)

        lbl = Label(char_frame, height=1, width=1, text=load[i])
        var = Text(char_frame, height=1, width=1)
        lbl.grid(row=0, column=0)
        var.grid(row=1, column=0)

        var.delete(1.0, END)
        var.insert(1.0, '0')
        var.bind("<Tab>", focus_next_widget)
        var.bind("<Shift-Tab>", focus_prev_widget)
        var.bind("<FocusIn>", select_all)
        vars.append(var)

    # with open(target_folder + current_sentence.split('.')[0] + '.txt', 'r') as label_file:
    #     r = label_file.read()
    #     r = r.strip().split(' ')
    #     i = 0
    #     for v in check_vars:
    #         v.delete(1.0, END)
    #         v.insert(1.0, '{} {}'.format(str(r[0+i*2]), str(r[1+i*2])))

    #         if str(r[0+i*2]) == '-1' or str(r[1+i*2]) == -1:
    #             render = ImageTk.PhotoImage(load)
    #             sent_lbl.configure(image=render)
    #             sent_lbl.image = render
    #         else:
    #             create_circle(x=int(r[0+i*2]), y=int(r[1+i*2]), color=label_colors[str(i)])

    #         i +=1

    chars = []

    # for c in load:
    #     char = Text(text_frame, height=2, width=2)
    # sent_lbl.configure(text=sent)

    return vars

def render_sentence_holder(parent):
    global current_sentence

    # sentence_frame = Frame(parent)
    # sentence_frame.grid(row=0, column=0)

    # sent_lbl = Label(sentence_frame)

    # sent_lbl.pack(side='top')
    check_vars = load_sentence(current_sentence)

    progress_frame = Frame(parent)
    progress_frame.grid(row=1, column=0)

    progress_lbl = Label(progress_frame)
    progress_lbl.configure(text='{} of {}'.format(sentence_index+1, len(sentences)))
    progress_lbl.pack(side='bottom')
    
    return progress_lbl

# def render_label_box(parent):
#     label_box_frame = Frame(parent)
#     label_box_frame.grid(row=0, column=1)
    
#     text_frame = Frame(label_box_frame)
#     text_frame.pack(pady=20)

#     vars = []
#     for label in target_labels.keys():
#         lbl = Label(text_frame, height=2, text=label)
#         var = Text(text_frame, height=2, width=20)
#         lbl.grid(row=target_labels[label], column=0)
#         var.grid(row=target_labels[label], column=1)
#         var.delete(1.0, END)
#         var.insert(1.0, '-1 -1')
#         vars.append(var)

#     return vars

def next_sent():
    global sentence_index, sentences, current_sentence, sent_lbl, sentence_frame
    global progress_lbl
    sentence_index += 1
    if sentence_index < len(sentences):
        # with open(target_folder + current_sentence.split('.')[0] + '.txt', 'w') as label_file:
        #     for v in check_vars:
        #         s = v.get(1.0, END).strip().split(' ')
        #         label_file.write('{} {}'.format(str(s[0]), str(s[1])))
        #         label_file.write(' ')
        
        current_sentence = sentences[sentence_index]
        for widget in sentence_frame.winfo_children():
            widget.destroy()
        vars = load_sentence(sent=current_sentence)
        vars = None
        
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
        vars = load_sentence(sent=current_sentence)
        vars = None
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

with open('sentences.txt', 'r') as f:
    sentences = [x.strip() for x in f.read().split('\n')]
    f.close()

print('Got total {} sentences'.format(len(sentences)))

label_path = './labels.txt'

if not os.path.exists(label_path):
    with open('labels.txt', 'w+') as f:
        for sent in sentences:
            f.write('1'*len(sent))
            f.write('\n')
        f.close()

current_sentence = sentences[sentence_index]
sent_lbl = None
load = None
vars = load_sentence(current_sentence)
progress_lbl = render_sentence_holder(root)
root.bind('<Key>', key_stroke)

root.mainloop()

