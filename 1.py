import random
from textwrap import wrap
from tkinter import *
from tkinter import messagebox

def encode(text, r):
    text_to_binary = "".join(format(x, "08b") for x in bytearray(text, "utf-8"))
    n = 2 ** (r - 1)
    razbiv = wrap(text_to_binary, n)

    for i in range(len(razbiv)):
        encode_str = ["0"] * (n + r)
        j = 0
        for k in range(n + r):
            if k not in [2 ** t - 1 for t in range(r)]:
                if j < len(razbiv[i]):
                    encode_str[k] = razbiv[i][j]
                    j += 1
        for w in range(r):
            check_index = 2 ** w - 1
            check_value = calc_check_value(encode_str, check_index, n, r)
            encode_str[check_index] = check_value
        razbiv[i] = ''.join(encode_str)
    return razbiv

def calc_check_value(encoded_str, check_index, n, r):
    check_value = 0
    for i in range(check_index, n + r, 2 * check_index + 2):
        for j in range(i, min(i + check_index + 1, n + r)):
            check_value ^= int(encoded_str[j])

    return str(check_value)

def decode(razbiv, r):
    n = 2 ** (r - 1)
    for k in range(len(razbiv)):
        razbiv[k] = ''.join([razbiv[k][i] for i in range(n + r) if i not in [2 ** t - 1 for t in range(r)]])
    decode_str = ''.join(razbiv)
    decode_str = int(decode_str, 2).to_bytes((len(decode_str) + 7) // 8, byteorder='big').decode('utf-8')
    return decode_str

def add_error(razbiv, block_index):
    error_position = random.randint(0, len(razbiv[block_index]) - 1)
    while error_position in [2 ** t - 1 for t in range(len(razbiv[block_index]))]:
        error_position = random.randint(0, len(razbiv[block_index]) - 1)
    razbiv[block_index] = razbiv[block_index][:error_position] + ('0' if razbiv[block_index][error_position] == '1' else '1') + razbiv[block_index][error_position + 1:]

    return razbiv

def correct_error(razbiv, r):
    for i in range(len(razbiv)):
        bits = [0] * r
        for k in range(r):
            for w in range(len(razbiv[i])):
                if ((w + 1) >> k) & 1:
                    bits[k] ^= int(razbiv[i][w])
        poz = 0
        for y, bit in enumerate(bits):
            poz += bit * (2 ** y)
        if poz != 0:
            if razbiv[i][poz - 1] == "1":
                razbiv[i] = razbiv[i][:poz - 1] + "0" + razbiv[i][poz:]
            else:
                razbiv[i] = razbiv[i][:poz - 1] + "1" + razbiv[i][poz:]
    return razbiv
def coder():
    window_c = Tk()
    window_c.title("Процесс кодирования")
    window_c.geometry("400x400")
    text_run = text.get()
    r_run = r.get()

    if text_run == "":
        messagebox.showerror("Ошибка", "Пожалуйста, введите текст.")
        window_c.destroy()
        return
    if r_run.isdigit() != True or int(r_run) <= 1:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное значение (число) для r (больше 1).")
        window_c.destroy()
        return
    text_info = Label(window_c, text='Закодированные блоки')
    text_info.pack()
    out_text = '\n'.join(encode(text_run, int(r_run)))
    out_window = Text(window_c, width=40, height=12)
    out_window.pack()
    out_window.insert(END, out_text)
    out_window.config(state='disabled')


def check():
    window_d = Tk()
    window_d.title("Процесс декодирования")
    window_d.geometry("400x600")
    text_run = text.get()
    r_run = r.get()
    out_razbiv = encode(text_run, int(r_run))
    error_block_use = error_block.get()
    if int(error_block_use) < 0 or int(error_block_use) > (len(out_razbiv) - 1):
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректный номер блока.")
        window_d.destroy()
        return
    else:
        text_info = Label(window_d, text='Блоки с ошибкой')
        text_info.pack()
        out_window = Text(window_d, width=40, height=12)
        out_window.pack()
        out_add = add_error(out_razbiv, int(error_block_use))
        out = '\n'.join(out_add)
        out_window.insert(END, out)
        out_window.config(state='disabled')
        text_info_err = Label(window_d, text='Проверка исправления ошибки')
        text_info_err.pack()
        out_window_err = Text(window_d, width=40, height=12)
        out_window_err.pack()
        out_err_add = correct_error(out_add, int(r_run))
        out_err = '\n'.join(out_err_add)
        out_window_err.insert(END, out_err)
        out_window_err.config(state='disabled')
        text_info_dec = Label(window_d, text='Декодирование нашей строки')
        text_info_dec.pack()
        out_window_dec = Text(window_d, width=40, height=8)
        out_window_dec.pack()
        out_err_dec = decode(out_err_add, int(r_run))
        out_window_dec.insert(END, out_err_dec)
        out_window_dec.config(state='disabled')


window_m = Tk()
window_m.title("Код Хэмминга")
window_m.geometry("600x300")
text_info = Label(window_m, text='Введите символы в поле ниже')
text_info.pack()
text = Entry(window_m)
text.pack()
r_info = Label(window_m, text='Введите кол-во контрольных битов в поле ниже')
r_info.pack()
r = Entry(window_m)
r.pack()
error_block_text = Label(window_m, text='Введите номер блока для добавления ошибки (начинается с 0)')
error_block_text.pack()
error_block = Entry(window_m)
error_block.pack()
label_text = Label(window_m, text="Выберите окно")
label_text.pack()
code_button = Button(window_m, text='Начать кодирование', command=coder)
code_button.pack()
error_but = Button(window_m, text="Начать декодирование", command=check)
error_but.pack()
window_m.mainloop()