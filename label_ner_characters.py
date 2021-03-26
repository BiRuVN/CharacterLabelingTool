import os
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Label coordinate')
root.geometry('1024x720')

# # Define dataset path and labels here
# label_folder = './data/training/cursor/seq_01/'

target_labels = {
    'not_address': 0,
    'address': 1
    # 'address': 3
}


sentence_index = 0

def load_sentence(parent, sent):
    global load
    load = [x for x in current_sentence] + ['']*(256-len(current_sentence))

    sentence_frame = Frame(parent)
    sentence_frame.grid(row=0, column=0)
    # sentence_frame.pack(fill=X)
    vars = []
    i=0
    print(current_sentence)
    print(load)
    row = 0
    column = 0
    for c in load:
        column = load.index(c)+i
        if column >= 50:
            column = column % 50
            row += 1

        char_frame = Frame(sentence_frame)
        char_frame.grid(row=row, column=column)
        lbl = Label(char_frame, height=1, text=c)
        var = Text(char_frame, height=1, width=1)
        lbl.grid(row=0, column=0)
        var.grid(row=1, column=0)
        # lbl.pack(side=TOP)
        # var.pack(side=BOTTOM)
        var.delete(1.0, END)
        var.insert(1.0, '1')
        vars.append(var)
        i += 1

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
    check_vars = load_sentence(parent, current_sentence)

    progress_frame = Frame(parent)
    progress_frame.grid(row=1, column=0)

    progress_lbl = Label(progress_frame)
    progress_lbl.configure(text='{} of {}'.format(sentence_index, len(sentences)))
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

# def next_image():
#     global sentence_index, images, current_sentence, sent_lbl
#     global img_name_lbl, progress_lbl, img_shape
#     if sentence_index < len(images):
#         with open(target_folder + current_sentence.split('.')[0] + '.txt', 'w') as label_file:
#             for v in check_vars:
#                 s = v.get(1.0, END).strip().split(' ')
#                 label_file.write('{} {}'.format(str(s[0]), str(s[1])))
#                 label_file.write(' ')

#         sentence_index += 1
#         current_sentence = images[sentence_index]
#         s = load_image(current_sentence)
#         img_shape.configure(text='shape: {}'.format(s))
        
#     else:
#         sentence_index -= 1

#     img_name_lbl.configure(text=current_sentence)
#     progress_lbl.configure(text='{} of {}'.format(sentence_index, len(images)))

# def prev_image():
#     global sentence_index, images, current_sentence, sent_lbl
#     global img_name_lbl, progress_lbl, img_shape
#     sentence_index -= 1
#     if sentence_index > -1:
#         current_sentence = images[sentence_index]
#         s = load_image(current_sentence)
#         img_shape.configure(text='shape: {}'.format(s))
#     else:
#         sentence_index += 1

#     img_name_lbl.configure(text=current_sentence)
#     progress_lbl.configure(text='{} of {}'.format(sentence_index, len(images)))
    
def create_circle(x, y, color, r=3): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    print("draw")
    draw = ImageDraw.Draw(load)
    draw.ellipse([(x0, y0), (x1, y1)], fill=color)
    render = ImageTk.PhotoImage(load)
    sent_lbl.configure(image=render)
    sent_lbl.image = render
    # return draw.ellipse((x0, y0, x1, y1), fill='red', width=2)

def printcoords(event, color):
    #outputting x and y coords to console
    x, y = event.x, event.y
    create_circle(int(x), int(y), color)
    return (x, y)

def key_stroke(event):
    # while True:
    c = event.char
    if c == 'a':
        prev_image()
        # break
    elif c == 'd':
        next_image()
        # break
    else:
        print(c)
        if c == '1':
            check_vars[0].delete(1.0, END)
            check_vars[0].insert(1.0, printcoords(event, 'red'))
        elif c == '2':
            check_vars[1].delete(1.0, END)
            check_vars[1].insert(1.0, printcoords(event, 'blue'))
        elif c == '3':
            check_vars[2].delete(1.0, END)
            check_vars[2].insert(1.0, printcoords(event, 'green'))
        elif c == '4':
            check_vars[3].delete(1.0, END)
            check_vars[3].insert(1.0, printcoords(event, 'yellow'))
        elif c == '5':
            check_vars[4].delete(1.0, END)
            check_vars[4].insert(1.0, printcoords(event, 'black'))

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
# check_vars = load_sentence(current_sentence)
progress_lbl = render_sentence_holder(root)
root.bind('<Key>', key_stroke)

root.mainloop()

