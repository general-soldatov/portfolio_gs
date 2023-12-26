from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import csv

class LuxCalc(object):
    """
    Расчёт освещённости
    """

    def __init__(self, lux, length, width, heigth, dust, lamp, count_lamp, reflector, color_room):
        """Инициализация переменных"""
        dict_color = {"Чёрный": 0.1, "Тёмный": 0.3, "Средней светлости": 0.5, "Светлый": 0.7, "Белый": 0.8}
        self.lux = lux
        self.length = length
        self.width = width
        self.heigth = heigth
        self.dust = dust
        self.lamp = lamp
        self.count_lamp = count_lamp
        self.reflector = reflector
        self.color_room = dict_color[color_room]

    def stock_ratio(self):  # функция загрязнения
        dict_dust = {
            "LED": [0.0999, 1.2],
            "Газоразрядная": [0.125, 1.375],
            "Накаливания": [0.0999, 1.2],
            "Естественный": [0.05, 1.25]
        }
        lamp_dust = dict_dust[self.lamp]
        return lamp_dust[0] * self.dust + lamp_dust[1]

    def luminous_flux(self):
        forms_room = (self.length * self.width) / (self.heigth * (self.length + self.width))
        with open('luminous_flux.csv', newline='') as csvfile:
            csReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csReader:
                if row[0] == "светильник":
                    svet = ','.join(row[4:])
                    svet = svet.split(",")
                if row[0] == self.reflector and float(row[2]) <= self.color_room:
                    lum = ','.join(row[4:])

            lum = lum.split(",")

            for ks in range(len(lum)):
                if float(svet[ks]) <= forms_room:
                    fr = float(lum[ks])
                else:
                    fr = float(lum[0])

        return fr

    def room(self):
        dict_reflector = {"С затемнением": [0.82, -2.51, 2.96],
                          "Без отражателя": [0.97, -3.01, 3.38],
                          "Эмалированный": [0.99, -3.03, 3.32]}
        l2h = self.length / self.heigth
        cuff = dict_reflector[self.reflector]
        uneven_illumination = cuff[0] * l2h ** 2 + cuff[1] * l2h + cuff[2]
        floor_area = self.length * self.width
        number_of_lamps = self.count_lamp
        flux_factor = self.luminous_flux()
        stock_ratio_c = self.stock_ratio()
        standard_illumination = self.lux
        luminos = stock_ratio_c * floor_area * standard_illumination / (number_of_lamps * flux_factor * uneven_illumination)
        return luminos




root = Tk()

root.title("Калькулятор освещённости")
#root.iconbitmap(default="favicon.ico")
#root.iconphoto(False, icon)
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

wr = int(w/2)
hr = int(0.4*h)
root.geometry(f"{wr}x{hr}")
canvas = Canvas(root, height=hr, width=wr)



root.minsize(wr, hr)   # минимальные размеры: ширина - 200, высота - 150
root.maxsize(wr, hr)   # максимальные размеры: ширина - 400, высота - 300

#константы для элементов
font_text = 10
width_text = int(0.015*w)
width_element = int(0.02*w)
heigth_element = int(0.0042*h)
row = [0, 10, 160, 330, 470]
line = [0, 15, 65, 115, 165, 215]

clicks = 0





def click(): #функция вычислений при нажатии на кнопку
    try:
        global clicks, length, heigth, weigth, dust, light, lamp, reflector, color
        luxCalc = LuxCalc(float(lux.get()), float(length.get()),
                          float(weigth.get()), float(heigth.get()), int(dust.get()), light.get(),
                          int(lamp.get()), reflector.get(), color.get())


        clicks = luxCalc.room()

        showinfo(title="Результат вычислений", message=f"Расчётная величина светового потока {round(clicks, 4)} лм \n"
                                       f"Рекомендуется лампа {luxCalc.lamp.lower()} мощностью 0 Вт\n"
                                       f"в количестве {luxCalc.count_lamp} шт.")
    except ZeroDivisionError as e:
        showerror(title="Ошибка", message=f"Деление на ноль: {e}.")

    except ValueError as e:
        showerror(title="Ошибка", message=f"Ошибка преобразования типа: {e}")

    except IndexError as e:
        showerror(title="Ошибка", message=f"Ошибка индексации: {e}")

    except Exception as e:
        showerror(title="Ошибка", message=f"Проверьте правильность заполнения ячеек {e}.")



#вывод элементов
lux = Entry(root, width=int(0.96*width_element))
length = Spinbox(root, from_=1.1, to=30.0, width=int(0.91*width_element))
weigth = Spinbox(root, from_=1.1, to=30.0, width=int(0.91*width_element))
heigth = Spinbox(root, from_=1.1, to=30.0, width=int(0.91*width_element))
dust = Spinbox(root, from_=1, to=5, width=int(0.91*width_element))

light = Combobox(root, width=int(0.8*width_element))
lamp = Spinbox(root, from_=0.1, to=30.0, width=int(0.91*width_element))
reflector = Combobox(root, width=int(0.8*width_element))
color = Combobox(root, width=int(0.8*width_element))


exit_btn = Button(root, text='Закрыть', command=root.destroy, height=1, width=10, font=("Arial", font_text))
button = Button(text="Вычислить", height=1, width=10, font=("Arial", font_text), command=click)

#наполнитель для бокса
light['values'] = ("LED", "Газоразрядная", "Накаливания", "Естественный")
reflector['values'] = ("С затемнением", "Без отражателя", "Эмалированный")
color['values'] = ("Чёрный", "Тёмный", "Средней светлости", "Светлый", "Белый")

#размещение элементов
lux.place(x=row[2], y=line[1])
length.place(x=row[2], y=line[2])
weigth.place(x=row[2], y=line[3])
heigth.place(x=row[2], y=line[4])
dust.place(x=row[2], y=line[5])

#размещение элементов 2-го ряда
light.place(x=row[4], y=line[1])
lamp.place(x=row[4], y=line[2])
reflector.place(x=row[4], y=line[3])
color.place(x=row[4], y=line[4])
#размещение кнопок
button.place(x=0.69*wr, y=0.86*hr)
exit_btn.place(x=0.85*wr, y=0.86*hr)


#вывод картинки на задний фон
image = Image.open("kandinsky-download-1693585934773.png")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(0, 0, anchor='nw', image=photo)
canvas.place(x=1, y=1)

#подписи блоков 1 ряд
text_lux = canvas.create_text(row[1], line[1], anchor='nw',font=("Arial", font_text), text="Освещённость, лк", fill="Black")
text_length = canvas.create_text(row[1], line[2], anchor='nw', font=("Arial", font_text), text="Длина помещения, м", fill="Black")
text_weigth = canvas.create_text(row[1], line[3], anchor='nw', font=("Arial", font_text), text="Ширина помещения, м", fill="Black")
text_heigth = canvas.create_text(row[1], line[4], anchor='nw', font=("Arial", font_text), text="Высота помещения, м", fill="Black")
text_dust = canvas.create_text(row[1], line[5], anchor='nw', font=("Arial", font_text), text="Загрязнённость, мг/м^3", fill="Black")
#подписи блоков 2 ряд
text_ligth = canvas.create_text(row[3], line[1], anchor='nw', font=("Arial", font_text), text="Тип лампы", fill="Black")
text_lamp = canvas.create_text(row[3], line[2], anchor='nw', font=("Arial", font_text), text="Количество ламп, шт.", fill="Black")
text_reflector = canvas.create_text(row[3], line[3], anchor='nw', font=("Arial", font_text), text="Тип плафона", fill="Black")
text_color = canvas.create_text(row[3], line[4], anchor='nw', font=("Arial", font_text), text="Цвет комнаты", fill="Black")


root.mainloop()




