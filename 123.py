import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import datetime
import random
import hashlib
import json
import os


# Класс для хранения данных пользователей
class UserDatabase:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()

    def load_users(self):
        """Загрузка пользователей из файла"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_users(self):
        """Сохранение пользователей в файл"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def add_user(self, login, password, fio, email, operator_id, age):
        """Добавление нового пользователя с возрастом"""
        # Хешируем пароль
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.users[login] = {
            'password': hashed_password,
            'fio': fio,
            'email': email,
            'operator_id': operator_id,
            'age': age  # Добавляем возраст
        }
        self.save_users()

    def check_user(self, login, password):
        """Проверка логина и пароля"""
        if login in self.users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return self.users[login]['password'] == hashed_password
        return False

    def get_user_data(self, login):
        """Получение данных пользователя"""
        return self.users.get(login, {})


# Создаем глобальный экземпляр базы данных
db = UserDatabase()


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Нейрободр - Авторизация")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # Центрируем окно
        self.center_window(self.root, 400, 350)

        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок
        title_label = tk.Label(main_frame, text="Нейрободр",
                               font=("Arial", 28, "bold"),
                               bg='white', fg='#2c3e50')
        title_label.pack(pady=(30, 5))

        # Подзаголовок
        login_label = tk.Label(main_frame, text="Авторизация",
                               font=("Arial", 14),
                               bg='white', fg='#34495e')
        login_label.pack(pady=(0, 30))

        # Фрейм для полей ввода
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(pady=10)

        # Логин
        login_text_label = tk.Label(input_frame, text="Логин:",
                                    font=("Arial", 11),
                                    bg='white', fg='black')
        login_text_label.grid(row=0, column=0, sticky='w', pady=5, padx=5)

        self.login_entry = tk.Entry(input_frame, font=("Arial", 11),
                                    bd=1, relief='solid', width=20)
        self.login_entry.grid(row=0, column=1, pady=5, padx=5)

        # Пароль
        password_text_label = tk.Label(input_frame, text="Пароль:",
                                       font=("Arial", 11),
                                       bg='white', fg='black')
        password_text_label.grid(row=1, column=0, sticky='w', pady=5, padx=5)

        self.password_entry = tk.Entry(input_frame, font=("Arial", 11),
                                       bd=1, relief='solid', width=20, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        # Кнопка входа
        login_btn = tk.Button(main_frame, text="Войти",
                              command=self.check_login,
                              bg='#3498db', fg='white',
                              font=("Arial", 11, "bold"),
                              width=15, height=1,
                              relief='raised', bd=1,
                              cursor='hand2', activebackground='#2980b9')
        login_btn.pack(pady=20)

        # Кнопка регистрации
        register_btn = tk.Button(main_frame, text="Зарегистрироваться",
                                 command=self.open_register,
                                 bg='#27ae60', fg='white',
                                 font=("Arial", 10),
                                 width=15, height=1,
                                 relief='raised', bd=1,
                                 cursor='hand2', activebackground='#2ecc71')
        register_btn.pack(pady=5)

        self.root.mainloop()

    def check_login(self):
        """Проверка логина и пароля"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if db.check_user(login, password):
            messagebox.showinfo("Успешно", "Авторизация пройдена!")
            user_data = db.get_user_data(login)
            self.root.destroy()
            MainWindow(login, user_data)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def open_register(self):
        """Открыть окно регистрации"""
        self.root.destroy()
        RegisterWindow()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')


class RegisterWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Нейрободр - Регистрация")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        self.center_window(self.root, 400, 500)

        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок
        title_label = tk.Label(main_frame, text="Нейрободр",
                               font=("Arial", 28, "bold"),
                               bg='white', fg='#2c3e50')
        title_label.pack(pady=(30, 5))

        # Подзаголовок
        reg_label = tk.Label(main_frame, text="Регистрация нового пользователя",
                             font=("Arial", 12),
                             bg='white', fg='#34495e')
        reg_label.pack(pady=(0, 20))

        # Фрейм для полей ввода
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(pady=10)

        # Поля для регистрации
        fields = [
            ("Логин:", "login"),
            ("Пароль:", "password"),
            ("Подтверждение:", "confirm"),
            ("ФИО:", "fio"),
            ("Возраст:", "age"),
            ("Email:", "email"),
            ("ID оператора:", "operator_id")
        ]

        self.entries = {}
        self.operator_id_value = None

        for i, (label_text, key) in enumerate(fields):
            # Метка
            label = tk.Label(input_frame, text=label_text,
                             font=("Arial", 11),
                             bg='white', fg='black')
            label.grid(row=i, column=0, sticky='w', pady=5, padx=5)

            # Поле ввода
            show_char = "*" if "пароль" in label_text.lower() or "подтверждение" in label_text.lower() else ""

            if key == "operator_id":
                # Для ID - генерируем автоматически
                self.operator_id_value = random.randint(100000, 999999)
                entry = tk.Entry(input_frame, font=("Arial", 11),
                                 bd=1, relief='solid', width=20)
                entry.insert(0, str(self.operator_id_value))
                entry.config(state='readonly', readonlybackground='#f0f0f0')
            else:
                entry = tk.Entry(input_frame, font=("Arial", 11),
                                 bd=1, relief='solid', width=20, show=show_char)

            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[key] = entry

        # Кнопка регистрации
        register_btn = tk.Button(main_frame, text="Зарегистрироваться",
                                 command=self.register_user,
                                 bg='#27ae60', fg='white',
                                 font=("Arial", 11, "bold"),
                                 width=20, height=1,
                                 relief='raised', bd=1,
                                 cursor='hand2', activebackground='#2ecc71')
        register_btn.pack(pady=20)

        # Кнопка назад к авторизации
        back_btn = tk.Button(main_frame, text="← Назад",
                             command=self.back_to_login,
                             bg='#7f8c8d', fg='white',
                             font=("Arial", 10),
                             width=10, height=1,
                             relief='raised', bd=1,
                             cursor='hand2', activebackground='#95a5a6')
        back_btn.pack()

        self.root.mainloop()

    def register_user(self):
        """Регистрация нового пользователя"""
        login = self.entries['login'].get()
        password = self.entries['password'].get()
        confirm = self.entries['confirm'].get()
        fio = self.entries['fio'].get()
        age = self.entries['age'].get()
        email = self.entries['email'].get()
        operator_id = self.operator_id_value

        # Проверка заполнения
        if not all([login, password, confirm, fio, age, email]):
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return

        # Проверка возраста (должен быть числом и не меньше 18)
        try:
            age_int = int(age)
            if age_int < 18:
                messagebox.showerror("Ошибка", "Возраст должен быть не менее 18 лет!")
                return
            # Убрано ограничение сверху
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст должен быть числом!")
            return

        # Проверка совпадения паролей
        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return

        # Проверка длины пароля
        if len(password) < 3:
            messagebox.showerror("Ошибка", "Пароль должен быть не менее 3 символов!")
            return

        # Проверка уникальности логина
        if login in db.users:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
            return

        # Сохраняем пользователя
        db.add_user(login, password, fio, email, operator_id, age)

        messagebox.showinfo("Успешно",
                            f"Пользователь {login} успешно зарегистрирован!\n"
                            f"Ваш ID оператора: {operator_id}\n"
                            f"Возраст: {age}\n"
                            "Теперь вы можете войти в систему.")

        self.root.destroy()
        LoginWindow()

    def back_to_login(self):
        """Вернуться к окну авторизации"""
        self.root.destroy()
        LoginWindow()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')


class MainWindow:
    def __init__(self, login, user_data):
        self.login = login
        self.user_data = user_data
        self.operator_id = user_data.get('operator_id', random.randint(100000, 999999))
        self.fio = user_data.get('fio', 'Иванов Иван Иванович')
        self.age = user_data.get('age', '18')

        self.root = tk.Tk()
        self.root.title("Нейрободр - Регистрация оператора")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # Центрируем окно
        self.center_window(self.root, 550, 650)

        # Основной фрейм с белым фоном
        main_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок
        title_label = tk.Label(main_frame, text="Нейрободр",
                               font=("Arial", 28, "bold"),
                               bg='white', fg='#2c3e50')
        title_label.pack(pady=(20, 5))

        # Заголовок регистрации
        reg_label = tk.Label(main_frame, text="Регистрация оператора",
                             font=("Arial", 16, "bold"),
                             bg='white', fg='#34495e')
        reg_label.pack(pady=(0, 20))

        # Фрейм для полей ввода (слева)
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(side='left', fill='y', padx=(30, 10), pady=10, anchor='n')

        # Поля ввода
        labels = ['Фамилия', 'Имя', 'Отчество', 'Возраст']
        self.entries = {}

        fio_parts = self.fio.split()
        surname = fio_parts[0] if len(fio_parts) > 0 else 'Иванов'
        name = fio_parts[1] if len(fio_parts) > 1 else 'Иван'
        patronymic = fio_parts[2] if len(fio_parts) > 2 else 'Иванович'

        for i, label_text in enumerate(labels):
            label = tk.Label(input_frame, text=label_text,
                             font=("Arial", 12, "bold"),
                             bg='white', fg='black', anchor='w')
            label.pack(anchor='w', pady=(10 if i > 0 else 0, 0))

            entry = tk.Entry(input_frame, font=("Arial", 11),
                             bd=1, relief='solid', width=15)
            entry.pack(anchor='w', pady=(0, 5))

            if label_text == 'Фамилия':
                entry.insert(0, surname)
            elif label_text == 'Имя':
                entry.insert(0, name)
            elif label_text == 'Отчество':
                entry.insert(0, patronymic)
            elif label_text == 'Возраст':
                entry.insert(0, self.age)

            self.entries[label_text.lower()] = entry

        # Отображаем ID оператора
        id_label = tk.Label(input_frame, text="ID оператора:",
                            font=("Arial", 12, "bold"),
                            bg='white', fg='black', anchor='w')
        id_label.pack(anchor='w', pady=(10, 0))

        id_display = tk.Label(input_frame, text=str(self.operator_id),
                              font=("Arial", 11),
                              bg='#f0f0f0', fg='black', anchor='w',
                              relief='sunken', bd=1, width=15)
        id_display.pack(anchor='w', pady=(0, 5))

        # Кнопка записи
        register_btn = tk.Button(input_frame, text="Записать",
                                 command=self.register_operator,
                                 bg='#3498db', fg='white',
                                 font=("Arial", 11, "bold"),
                                 width=15, height=1,
                                 relief='raised', bd=1,
                                 cursor='hand2', activebackground='#2980b9')
        register_btn.pack(pady=20)

        # Фрейм для фото (по центру)
        photo_frame_container = tk.Frame(main_frame, bg='white')
        photo_frame_container.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Фрейм для фото
        photo_frame = tk.Frame(photo_frame_container, bg='#ecf0f1', width=150, height=150, relief='solid', bd=1)
        photo_frame.pack(anchor='center', pady=(30, 10))
        photo_frame.pack_propagate(False)

        # Метка для фото
        self.photo_label = tk.Label(photo_frame, bg='#ecf0f1', text="Нет фото", font=("Arial", 10))
        self.photo_label.pack(expand=True, fill='both')

        # Кнопка загрузки фото
        load_photo_btn = tk.Button(photo_frame_container, text="Загрузить фото",
                                   command=self.load_photo,
                                   font=("Arial", 9), bg='#3498db', fg='white',
                                   width=15, relief='raised', bd=1, cursor='hand2')
        load_photo_btn.pack(anchor='center')

        # Фрейм для идентификации (справа)
        id_frame = tk.Frame(main_frame, bg='white')
        id_frame.pack(side='right', fill='y', padx=(10, 30), pady=10, anchor='n')

        # Заголовок идентификации
        id_title = tk.Label(id_frame, text="Идентификация",
                            font=("Arial", 16, "bold"),
                            bg='white', fg='#34495e')
        id_title.pack(anchor='w', pady=(30, 15))

        # Оператор
        operator_frame = tk.Frame(id_frame, bg='white')
        operator_frame.pack(anchor='w', pady=(0, 5))

        self.operator_text = tk.Label(operator_frame, text="Оператор не определен",
                                      font=("Arial", 12),
                                      bg='white', fg='black')
        self.operator_text.pack(side='left')

        # Красный крестик
        self.cross_label = tk.Label(operator_frame, text="❌",
                                    font=("Arial", 12),
                                    bg='white', fg='red')
        self.cross_label.pack(side='left', padx=(5, 0))

        # ID
        self.id_display_label = tk.Label(id_frame, text=f"ID {self.operator_id}",
                                         font=("Arial", 12),
                                         bg='white', fg='black')
        self.id_display_label.pack(anchor='w', pady=(0, 15))

        # Запуск программы
        self.impossible_label = tk.Label(id_frame, text="Запуск программы невозможен",
                                         font=("Arial", 12, "bold"),
                                         bg='white', fg='#e74c3c')
        self.impossible_label.pack(anchor='w')

        # Фрейм для кнопок внизу
        bottom_button_frame = tk.Frame(main_frame, bg='white')
        bottom_button_frame.pack(side='bottom', fill='x', pady=20)

        # Кнопка Отмена
        cancel_button = tk.Button(bottom_button_frame, text="Отмена",
                                  command=self.root.quit,
                                  bg='#e74c3c', fg='white',
                                  font=("Arial", 11, "bold"),
                                  width=10, height=1,
                                  relief='raised', bd=1,
                                  cursor='hand2', activebackground='#c0392b')
        cancel_button.pack(side='left', padx=30)

        # Кнопка Далее
        self.next_button = tk.Button(bottom_button_frame, text="Далее →",
                                     command=self.open_next,
                                     bg='#27ae60', fg='white',
                                     font=("Arial", 11, "bold"),
                                     width=10, height=1,
                                     relief='raised', bd=1,
                                     cursor='hand2', activebackground='#2ecc71',
                                     state='disabled')
        self.next_button.pack(side='right', padx=30)

        # Кнопка выхода из аккаунта
        logout_btn = tk.Button(main_frame, text="Выйти",
                               command=self.logout,
                               bg='#7f8c8d', fg='white',
                               font=("Arial", 9),
                               width=8, height=1,
                               relief='raised', bd=1,
                               cursor='hand2', activebackground='#95a5a6')
        logout_btn.place(x=10, y=10)

        self.root.mainloop()

    def register_operator(self):
        """Регистрация оператора"""
        surname = self.entries['фамилия'].get()
        name = self.entries['имя'].get()
        patronymic = self.entries['отчество'].get()
        age = self.entries['возраст'].get()

        if surname and name and patronymic and age:
            # Проверка возраста (только не меньше 18)
            try:
                age_int = int(age)
                if age_int < 18:
                    messagebox.showerror("Ошибка", "Возраст должен быть не менее 18 лет!")
                    return
                # Убрано ограничение сверху
            except ValueError:
                messagebox.showerror("Ошибка", "Возраст должен быть числом!")
                return

            # Меняем статус идентификации
            self.operator_text.config(text="Оператор определен", fg='#27ae60')
            self.cross_label.config(text="✓", fg='green')

            # ID уже отображается
            self.id_display_label.config(fg='#27ae60')

            # Меняем текст о запуске
            self.impossible_label.config(text="Запуск программы возможен", fg='#27ae60')

            # Активируем кнопку Далее
            self.next_button.config(state='normal', bg='#27ae60')

            messagebox.showinfo("Успешно",
                                f"Оператор успешно зарегистрирован!\nID: {self.operator_id}\nВозраст: {age} лет")
        else:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")

    def load_photo(self):
        """Загрузка фотографии"""
        file_path = filedialog.askopenfilename(
            title="Выберите фотографию",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Все файлы", "*.*")
            ]
        )

        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((148, 148), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.photo_label.config(image=photo, text='')
                self.photo_label.image = photo

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def open_next(self):
        self.root.destroy()
        NextWindow()

    def logout(self):
        """Выход из аккаунта"""
        result = messagebox.askyesno("Подтверждение", "Вы действительно хотите выйти?")
        if result:
            self.root.destroy()
            LoginWindow()


class NextWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Нейрободр - Мониторинг")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        self.center_window(self.root, 400, 300)

        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок
        title_label = tk.Label(main_frame, text="Нейрободр",
                               font=("Arial", 22, "bold"),
                               bg='white', fg='#2c3e50')
        title_label.pack(pady=(40, 10))

        # Сообщение
        msg_label = tk.Label(main_frame, text="Мониторинг запущен",
                             font=("Arial", 14),
                             bg='white', fg='#27ae60')
        msg_label.pack(pady=30)

        # Кнопка выхода
        exit_button = tk.Button(main_frame, text="Выход",
                                command=self.root.quit,
                                bg='#e74c3c', fg='white',
                                font=("Arial", 11, "bold"),
                                width=12, height=1,
                                relief='raised', bd=1,
                                cursor='hand2', activebackground='#c0392b')
        exit_button.pack(pady=20)

        self.root.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    # Проверяем наличие библиотеки PIL
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("Установите библиотеку PIL: pip install Pillow")
        exit(1)

    # Запускаем окно авторизации
    app = LoginWindow()