import tkinter as tk  # Импорт основной библиотеки для создания GUI
from tkinter import ttk  # Импорт расширенных виджетов tkinter
import math  # Импорт математических функций (тригонометрия, константы)
import random  # Импорт для генерации случайных чисел
import sys  # Импорт системных функций (для завершения программы)
from PIL import Image, ImageTk, ImageDraw  # Импорт библиотеки для работы с изображениями
import os  # Импорт для работы с файловой системой


class SolarSystemSimulation:
    """Главный класс симуляции Солнечной системы"""

    def __init__(self, root):
        """Конструктор класса, инициализация всех компонентов"""
        self.root = root  # Сохраняем ссылку на главное окно
        self.root.title("Симуляция Солнечной системы")  # Устанавливаем заголовок окна
        self.root.geometry("1600x900")  # Устанавливаем размер окна (ширина x высота)
        self.root.configure(bg='#000010')  # Устанавливаем цвет фона (темно-синий)
        self.root.resizable(False, False)  # Запрещаем изменение размера окна

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Привязываем функцию закрытия окна

        # Константы симуляции
        self.AU = 90  # Астрономическая единица в пикселях (расстояние от Солнца до Земли)
        self.BASE_SPEED = 0.001  # Базовая скорость анимации
        self.time_multiplier = 1.0  # Множитель времени (ускорение/замедление)
        self.zoom_factor = 1.0  # Коэффициент масштабирования
        self.selected_planet = None  # Текущая выбранная планета (изначально None)
        self.paused = False  # Флаг паузы (False - анимация активна)
        self.animation_id = None  # ID текущей анимации для возможности отмены
        self.running = True  # Флаг работы программы (True - работает)

        # Словарь для хранения изображений планет
        self.planet_images = {}

        # Создание изображений планет
        self.create_planet_images()

        # Данные о планетах (список словарей)
        self.planets_data = [
            # Внутренние планеты
            {"name": "Меркурий", "distance": 0.4, "radius": 5, "color": "#A9A9A9",
             "speed": 1 / 0.24, "angle": random.uniform(0, 2 * math.pi), "image_key": "mercury"},
            {"name": "Венера", "distance": 0.7, "radius": 7, "color": "#F0E68C",
             "speed": 1 / 0.62, "angle": random.uniform(0, 2 * math.pi), "image_key": "venus"},
            {"name": "Земля", "distance": 1.0, "radius": 8, "color": "#4169E1",
             "speed": 1.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "earth"},
            {"name": "Марс", "distance": 1.5, "radius": 6, "color": "#CD5C5C",
             "speed": 1 / 1.88, "angle": random.uniform(0, 2 * math.pi), "image_key": "mars"},

            # Пояс астероидов - карликовая планета
            {"name": "Церера", "distance": 2.77, "radius": 4, "color": "#A9A9A9",
             "speed": 1 / 4.6, "angle": random.uniform(0, 2 * math.pi), "image_key": "ceres"},

            # Газовые гиганты
            {"name": "Юпитер", "distance": 5.2, "radius": 16, "color": "#DAA520",
             "speed": 1 / 11.86, "angle": random.uniform(0, 2 * math.pi), "image_key": "jupiter"},
            {"name": "Сатурн", "distance": 9.5, "radius": 14, "color": "#F4A460",
             "speed": 1 / 29.46, "angle": random.uniform(0, 2 * math.pi), "image_key": "saturn"},
            {"name": "Уран", "distance": 19.0, "radius": 12, "color": "#7FFFD4",
             "speed": 1 / 84.01, "angle": random.uniform(0, 2 * math.pi), "image_key": "uranus"},
            {"name": "Нептун", "distance": 30.0, "radius": 12, "color": "#1E90FF",
             "speed": 1 / 164.8, "angle": random.uniform(0, 2 * math.pi), "image_key": "neptune"},

            # Пояс Койпера - карликовые планеты
            {"name": "Плутон", "distance": 39.5, "radius": 4, "color": "#DEB887",
             "speed": 1 / 248.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "pluto"},
            {"name": "Хаумеа", "distance": 43.0, "radius": 3.5, "color": "#87CEEB",
             "speed": 1 / 285.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "haumea"},
            {"name": "Макемаке", "distance": 45.5, "radius": 3.5, "color": "#98FB98",
             "speed": 1 / 309.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "makemake"},
            {"name": "Эрида", "distance": 68.0, "radius": 4, "color": "#B0C4DE",
             "speed": 1 / 557.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "eris"},

            # Рассеянный диск - транснептуновые объекты
            {"name": "Седна", "distance": 76.0, "radius": 3, "color": "#8B4513",
             "speed": 1 / 11400.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "sedna"},
            {"name": "Квавар", "distance": 43.5, "radius": 3, "color": "#CD853F",
             "speed": 1 / 288.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "quaoar"},
            {"name": "Орк", "distance": 39.4, "radius": 3, "color": "#8FBC8F",
             "speed": 1 / 247.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "orcus"},
            {"name": "Варуна", "distance": 42.9, "radius": 3, "color": "#B8860B",
             "speed": 1 / 281.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "varuna"},
            {"name": "Иксион", "distance": 39.6, "radius": 3, "color": "#9ACD32",
             "speed": 1 / 249.0, "angle": random.uniform(0, 2 * math.pi), "image_key": "ixion"},
        ]

        # Данные для информационной панели (подробная информация о планетах)
        self.planet_info = {}

        # Создание интерфейса
        self.create_widgets()

        # Сбор справочной информации о планетах
        self.collect_planet_info()

        # Запуск анимации
        self.animate()

    def create_planet_images(self):
        """Создание изображений планет (загрузка из файлов или генерация)"""
        try:
            # Пытаемся загрузить реальные изображения, если они есть
            image_files = {
                "mercury": "меркурый.jpg",  # для Меркурия
                "venus": "венера.avif",  # для Венеры
                "earth": "земл.webp",  # для Земли
                "mars": "марс.avif",  # для Марса
                "jupiter": "юпитер.webp",  # для Юпитера
                "saturn": "сатурн.jpg",  # для Сатурна
                "ceres": "церера.webp",  # для Цереры
                # для остальных планет файлов нет – они будут созданы синтетически
            }

            # Если файлы есть, загружаем их
            for key, filename in image_files.items():
                if os.path.exists(filename):  # Проверяем существование файла
                    img = Image.open(filename)  # Открываем изображение
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Изменяем размер
                    self.planet_images[key] = ImageTk.PhotoImage(img)  # Конвертируем для tkinter
                else:
                    # Если файла нет, создаем синтетическое изображение
                    self.create_synthetic_image(key)
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем синтетические изображения для всех планет
            for key in ["mercury", "venus", "earth", "mars", "jupiter", "saturn",
                        "uranus", "neptune", "pluto", "ceres", "haumea", "makemake",
                        "eris", "sedna", "quaoar", "orcus", "varuna", "ixion"]:
                self.create_synthetic_image(key)

    def create_synthetic_image(self, key):
        """Создание синтетического изображения планеты с помощью рисования"""
        try:
            # Создаем изображение
            img = Image.new('RGB', (150, 150), color='#1a1a2e')  # Новое изображение с фоном
            draw = ImageDraw.Draw(img)  # Создаем объект для рисования

            # Цвета для разных планет
            colors = {
                "mercury": "#A9A9A9",
                "venus": "#F0E68C",
                "earth": "#4169E1",
                "mars": "#CD5C5C",
                "jupiter": "#DAA520",
                "saturn": "#F4A460",
                "uranus": "#7FFFD4",
                "neptune": "#1E90FF",
                "pluto": "#DEB887",
                "ceres": "#A9A9A9",
                "haumea": "#87CEEB",
                "makemake": "#98FB98",
                "eris": "#B0C4DE",
                "sedna": "#8B4513",
                "quaoar": "#CD853F",
                "orcus": "#8FBC8F",
                "varuna": "#B8860B",
                "ixion": "#9ACD32"
            }

            color = colors.get(key, "#FFFFFF")  # Получаем цвет или белый по умолчанию

            # Рисуем планету (эллипс)
            draw.ellipse([25, 25, 125, 125], fill=color, outline='white', width=2)

            # Добавляем детали в зависимости от планеты
            if key == "earth":
                # Континенты Земли (дуги)
                draw.arc([35, 35, 115, 115], start=30, end=150, fill='#228B22', width=3)
                draw.arc([35, 35, 115, 115], start=210, end=330, fill='#228B22', width=3)
                # Облака (эллипсы)
                draw.ellipse([45, 45, 65, 55], fill='white', outline=None)
                draw.ellipse([85, 75, 105, 85], fill='white', outline=None)
            elif key == "jupiter":
                # Полосы Юпитера (дуги)
                draw.arc([30, 60, 120, 90], start=0, end=360, fill='#8B4513', width=4)
                draw.arc([30, 70, 120, 100], start=0, end=360, fill='#CD853F', width=3)
                # Большое красное пятно (эллипс)
                draw.ellipse([70, 65, 90, 80], fill='#8B0000', outline=None)
            elif key == "saturn":
                # Кольца Сатурна (эллипсы)
                draw.ellipse([10, 55, 140, 95], outline='#D2B48C', width=3)
                draw.ellipse([15, 50, 135, 100], outline='#D2B48C', width=2)
                draw.ellipse([20, 45, 130, 105], outline='#DEB887', width=1)
            elif key == "mars":
                # Поверхность Марса (точки)
                draw.point((70, 70), fill='#8B4513')
                draw.point((80, 80), fill='#8B4513')
                draw.point((90, 60), fill='#8B4513')
                # Полярные шапки (эллипс)
                draw.ellipse([50, 30, 100, 45], fill='white', outline=None)
            elif key == "venus":
                # Облака Венеры (эллипсы)
                draw.ellipse([55, 45, 95, 105], fill='#FFFFFF', outline=None)
                draw.ellipse([45, 55, 105, 95], fill='#F0E68C', outline=None)
            elif key == "mercury":
                # Кратеры Меркурия (эллипсы)
                draw.ellipse([45, 45, 65, 65], fill='#808080', outline=None)
                draw.ellipse([85, 75, 105, 95], fill='#808080', outline=None)
                draw.ellipse([60, 90, 75, 105], fill='#808080', outline=None)
            elif key == "uranus":
                # Уран
                draw.ellipse([45, 45, 105, 105], fill='#7FFFD4', outline=None)
                draw.arc([30, 30, 120, 120], start=0, end=360, fill='#40E0D0', width=2)
            elif key == "neptune":
                # Нептун
                draw.ellipse([40, 40, 110, 110], fill='#1E90FF', outline=None)
                draw.arc([35, 35, 115, 115], start=45, end=135, fill='#4169E1', width=3)
            elif key == "pluto":
                # Плутон с сердцем
                draw.ellipse([50, 50, 100, 100], fill='#DEB887', outline=None)
                draw.ellipse([65, 65, 85, 85], fill='#FFFFFF', outline=None)
            elif key == "ceres":
                # Церера
                draw.ellipse([45, 45, 105, 105], fill='#A9A9A9', outline=None)
                draw.point((70, 70), fill='#FFFFFF')
                draw.point((80, 80), fill='#FFFFFF')
            elif key == "haumea":
                # Хаумеа (эллипсоидная форма)
                draw.ellipse([35, 45, 115, 105], fill='#87CEEB', outline=None)
            elif key == "makemake":
                # Макемаке
                draw.ellipse([40, 40, 110, 110], fill='#98FB98', outline=None)
                draw.ellipse([60, 60, 90, 90], fill='#32CD32', outline=None)
            elif key == "eris":
                # Эрида
                draw.ellipse([35, 35, 115, 115], fill='#B0C4DE', outline=None)
                draw.ellipse([60, 60, 90, 90], fill='#778899', outline=None)
            elif key == "sedna":
                # Седна (красноватая)
                draw.ellipse([40, 40, 110, 110], fill='#8B4513', outline=None)
                draw.ellipse([65, 65, 85, 85], fill='#CD853F', outline=None)
            elif key == "quaoar":
                # Квавар
                draw.ellipse([45, 45, 105, 105], fill='#CD853F', outline=None)
                draw.ellipse([60, 60, 90, 90], fill='#8B4513', outline=None)
            elif key == "orcus":
                # Орк
                draw.ellipse([40, 40, 110, 110], fill='#8FBC8F', outline=None)
                draw.ellipse([65, 65, 85, 85], fill='#2E8B57', outline=None)
            elif key == "varuna":
                # Варуна
                draw.ellipse([45, 45, 105, 105], fill='#B8860B', outline=None)
                draw.ellipse([65, 65, 85, 85], fill='#8B4513', outline=None)
            elif key == "ixion":
                # Иксион
                draw.ellipse([40, 40, 110, 110], fill='#9ACD32', outline=None)
                draw.ellipse([65, 65, 85, 85], fill='#6B8E23', outline=None)

            # Добавляем блик на всех планетах
            draw.ellipse([35, 35, 55, 55], fill='white', outline=None)

            self.planet_images[key] = ImageTk.PhotoImage(img)  # Конвертируем для tkinter
        except Exception as e:
            print(f"Ошибка создания изображения для {key}: {e}")
            self.planet_images[key] = None  # В случае ошибки сохраняем None

    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Основной фрейм для canvas и панели информации
        main_frame = tk.Frame(self.root, bg='#000010')  # Создаем фрейм-контейнер
        main_frame.pack(fill=tk.BOTH, expand=True)  # Размещаем с заполнением всего пространства

        # Левая панель с canvas (симуляция)
        left_frame = tk.Frame(main_frame, bg='#000010')  # Фрейм для левой части
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Слева, с расширением

        # Canvas для отрисовки Солнечной системы
        self.canvas = tk.Canvas(left_frame, width=1100, height=800, bg='#000010', highlightthickness=0)
        self.canvas.pack(pady=15, padx=15)  # Размещаем с отступами

        # Привязка событий мыши для выбора планет
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # Левый клик мыши

        # Фрейм с ползунками управления
        controls_frame = tk.Frame(left_frame, bg='#1a1a2e', relief=tk.RAISED, bd=3)
        controls_frame.pack(fill=tk.X, padx=15, pady=10)  # Растягиваем по горизонтали

        # Ползунок ускорения времени
        tk.Label(controls_frame, text="Ускорение времени:", bg='#1a1a2e', fg='white',
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=10)  # Метка

        self.time_scale = tk.Scale(controls_frame, from_=0.5, to=20, orient=tk.HORIZONTAL,
                                   length=250, resolution=0.5, bg='#1a1a2e', fg='white',
                                   font=('Arial', 10), command=self.change_time_speed)
        self.time_scale.set(1.0)  # Устанавливаем начальное значение
        self.time_scale.pack(side=tk.LEFT, padx=10)  # Размещаем слева

        tk.Label(controls_frame, text="x1", bg='#1a1a2e', fg='white',
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=5)  # Метка единицы измерения

        # Отображение текущего ускорения
        self.speed_label = tk.Label(controls_frame, text="1.0x", bg='#1a1a2e', fg='yellow',
                                    font=('Arial', 12, 'bold'))
        self.speed_label.pack(side=tk.LEFT, padx=15)

        # Ползунок зума
        tk.Label(controls_frame, text="Зум:", bg='#1a1a2e', fg='white',
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=25)  # Метка

        self.zoom_scale = tk.Scale(controls_frame, from_=0.3, to=3.0, orient=tk.HORIZONTAL,
                                   length=200, resolution=0.1, bg='#1a1a2e', fg='white',
                                   font=('Arial', 10), command=self.change_zoom)
        self.zoom_scale.set(1.0)  # Начальный зум
        self.zoom_scale.pack(side=tk.LEFT, padx=10)  # Размещаем

        tk.Label(controls_frame, text="1.0x", bg='#1a1a2e', fg='white',
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=5)  # Метка

        # Кнопка паузы
        self.pause_btn = tk.Button(controls_frame, text="⏸️ Пауза", command=self.toggle_pause,
                                   bg='#4a4a6a', fg='white', font=('Arial', 11, 'bold'),
                                   width=10, height=1)
        self.pause_btn.pack(side=tk.RIGHT, padx=15)  # Справа

        # Кнопка сброса
        reset_btn = tk.Button(controls_frame, text="🔄 Сброс", command=self.reset_simulation,
                              bg='#4a4a6a', fg='white', font=('Arial', 11, 'bold'),
                              width=10, height=1)
        reset_btn.pack(side=tk.RIGHT, padx=10)  # Справа от кнопки паузы

        # Правая панель с информацией о планете
        self.info_frame = tk.Frame(main_frame, width=400, bg='#1a1a2e', relief=tk.RAISED, bd=3)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=15)  # Справа, по высоте
        self.info_frame.pack_propagate(False)  # Запрещаем изменение размера

        # Заголовок информационной панели
        tk.Label(self.info_frame, text="Информация о планете", bg='#1a1a2e', fg='white',
                 font=('Arial', 18, 'bold')).pack(pady=15)

        # Фрейм для изображения планеты
        self.image_frame = tk.Frame(self.info_frame, bg='#1a1a2e', height=200)
        self.image_frame.pack(fill=tk.X, pady=10)  # По горизонтали
        self.image_frame.pack_propagate(False)  # Фиксированная высота

        # Метка для изображения
        self.planet_image_label = tk.Label(self.image_frame, bg='#1a1a2e')
        self.planet_image_label.pack(expand=True)  # Центрируем

        # Фрейм для содержимого информации
        self.info_content = tk.Frame(self.info_frame, bg='#1a1a2e')
        self.info_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)  # Заполняем

        # Начальное сообщение
        self.show_welcome_message()

    def collect_planet_info(self):
        """Сбор справочной информации о планетах для отображения"""
        self.planet_info = {
            "Меркурий": {
                "radius_km": 2440,  # Радиус в км
                "mass_kg": "3.30×10²³",  # Масса в кг
                "mass_earth": 0.055,  # Масса в массах Земли
                "density": 5.43,  # Плотность в г/см³
                "gravity": 3.7,  # Ускорение свободного падения в м/с²
                "temperature": "-173°C до +427°C",  # Температура
                "orbital_period": "88 дней",  # Орбитальный период
                "rotation_period": "58.6 дней",  # Период вращения
                "atmosphere": "Почти отсутствует",  # Состав атмосферы
                "moons": 0,  # Количество спутников
                "discovery": "Известна с древности",  # Дата открытия
                "name_origin": "Римский бог торговли",  # Происхождение названия
                "features": "Наибольшие суточные перепады температур в Солнечной системе"  # Особенности
            },
            "Венера": {
                "radius_km": 6052,
                "mass_kg": "4.87×10²⁴",
                "mass_earth": 0.815,
                "density": 5.24,
                "gravity": 8.9,
                "temperature": "+462°C",
                "orbital_period": "225 дней",
                "rotation_period": "243 дней (ретроградное)",
                "atmosphere": "CO₂, облака H₂SO₄",
                "moons": 0,
                "discovery": "Известна с древности",
                "name_origin": "Римская богиня любви",
                "features": "Самая горячая планета, вращается в обратную сторону"
            },
            "Земля": {
                "radius_km": 6371,
                "mass_kg": "5.97×10²⁴",
                "mass_earth": 1.0,
                "density": 5.52,
                "gravity": 9.8,
                "temperature": "-89°C до +58°C",
                "orbital_period": "365.25 дней",
                "rotation_period": "24 часа",
                "atmosphere": "N₂, O₂, Ar",
                "moons": 1,
                "discovery": "Наш дом",
                "name_origin": "Почва, суша",
                "features": "Единственная известная планета с жизнью"
            },
            "Марс": {
                "radius_km": 3390,
                "mass_kg": "6.42×10²³",
                "mass_earth": 0.107,
                "density": 3.93,
                "gravity": 3.7,
                "temperature": "-63°C (средняя)",
                "orbital_period": "687 дней",
                "rotation_period": "24.6 часов",
                "atmosphere": "CO₂, Ar, N₂",
                "moons": 2,
                "discovery": "Известен с древности",
                "name_origin": "Римский бог войны",
                "features": "Самый большой вулкан Олимп (21 км), долины Маринера"
            },
            "Церера": {
                "radius_km": 473,
                "mass_kg": "9.39×10²⁰",
                "mass_earth": 0.00016,
                "density": 2.16,
                "gravity": 0.27,
                "temperature": "-105°C",
                "orbital_period": "4.6 лет",
                "rotation_period": "9.07 часов",
                "atmosphere": "Следы водяного пара",
                "moons": 0,
                "discovery": "1801, Джузеппе Пиацци",
                "name_origin": "Римская богиня земледелия",
                "features": "Крупнейший объект в поясе астероидов"
            },
            "Юпитер": {
                "radius_km": 69911,
                "mass_kg": "1.90×10²⁷",
                "mass_earth": 317.8,
                "density": 1.33,
                "gravity": 24.8,
                "temperature": "-145°C (облака)",
                "orbital_period": "11.86 лет",
                "rotation_period": "9.93 часов",
                "atmosphere": "H₂, He",
                "moons": 79,
                "discovery": "Известен с древности",
                "name_origin": "Верховный римский бог",
                "features": "Самая большая планета, Большое Красное Пятно (шторм)"
            },
            "Сатурн": {
                "radius_km": 60268,
                "mass_kg": "5.68×10²⁶",
                "mass_earth": 95.2,
                "density": 0.69,
                "gravity": 10.4,
                "temperature": "-178°C",
                "orbital_period": "29.46 лет",
                "rotation_period": "10.7 часов",
                "atmosphere": "H₂, He",
                "moons": 83,
                "discovery": "Известен с древности",
                "name_origin": "Римский бог земледелия",
                "features": "Имеет великолепные кольца из льда и пыли, самая низкая плотность"
            },
            "Уран": {
                "radius_km": 25362,
                "mass_kg": "8.68×10²⁵",
                "mass_earth": 14.5,
                "density": 1.27,
                "gravity": 8.7,
                "temperature": "-224°C",
                "orbital_period": "84.01 лет",
                "rotation_period": "17.2 часов",
                "atmosphere": "H₂, He, CH₄",
                "moons": 27,
                "discovery": "1781, Уильям Гершель",
                "name_origin": "Греческий бог неба",
                "features": "Вращается на боку, ось наклонена на 98°"
            },
            "Нептун": {
                "radius_km": 24624,
                "mass_kg": "1.02×10²⁶",
                "mass_earth": 17.1,
                "density": 1.64,
                "gravity": 11.2,
                "temperature": "-218°C",
                "orbital_period": "164.8 лет",
                "rotation_period": "16.1 часов",
                "atmosphere": "H₂, He, CH₄",
                "moons": 14,
                "discovery": "1846, Галле и д'Арре",
                "name_origin": "Римский бог морей",
                "features": "Самые сильные ветры в Солнечной системе (до 2100 км/ч)"
            },
            "Плутон": {
                "radius_km": 1188,
                "mass_kg": "1.30×10²²",
                "mass_earth": 0.0022,
                "density": 1.85,
                "gravity": 0.62,
                "temperature": "-229°C",
                "orbital_period": "248 лет",
                "rotation_period": "6.4 дней",
                "atmosphere": "Азот, метан, угарный газ",
                "moons": 5,
                "discovery": "1930, Клайд Томбо",
                "name_origin": "Римский бог подземного мира",
                "features": "Имеет сердцеобразную область из азотного льда"
            },
            "Хаумеа": {
                "radius_km": "~620 (эллипсоид)",
                "mass_kg": "4.01×10²¹",
                "mass_earth": 0.00067,
                "density": 1.88,
                "gravity": 0.4,
                "temperature": "-223°C",
                "orbital_period": "285 лет",
                "rotation_period": "3.9 часов",
                "atmosphere": "Отсутствует",
                "moons": 2,
                "discovery": "2004, Браун и др.",
                "name_origin": "Гавайская богиня плодородия",
                "features": "Эллипсоидная форма из-за быстрого вращения"
            },
            "Макемаке": {
                "radius_km": 715,
                "mass_kg": "3.1×10²¹",
                "mass_earth": 0.00052,
                "density": 1.7,
                "gravity": 0.5,
                "temperature": "-239°C",
                "orbital_period": "309 лет",
                "rotation_period": "22.8 часов",
                "atmosphere": "Метан, азот",
                "moons": 1,
                "discovery": "2005, Браун и др.",
                "name_origin": "Божество с острова Пасхи",
                "features": "Покрыт метановым льдом"
            },
            "Эрида": {
                "radius_km": 1163,
                "mass_kg": "1.66×10²²",
                "mass_earth": 0.0028,
                "density": 2.43,
                "gravity": 0.8,
                "temperature": "-243°C",
                "orbital_period": "557 лет",
                "rotation_period": "25.9 часов",
                "atmosphere": "Метан, азот",
                "moons": 1,
                "discovery": "2005, Браун и др.",
                "name_origin": "Греческая богиня раздора",
                "features": "Самая массивная карликовая планета"
            },
            "Седна": {
                "radius_km": "~500",
                "mass_kg": "~8.3×10²⁰",
                "mass_earth": 0.00014,
                "density": "~1.5",
                "gravity": "~0.3",
                "temperature": "-240°C",
                "orbital_period": "~11400 лет",
                "rotation_period": "~10 часов",
                "atmosphere": "Неизвестно",
                "moons": 0,
                "discovery": "2003, Браун и др.",
                "name_origin": "Инуитская богиня моря",
                "features": "Очень вытянутая орбита, один из самых удаленных объектов"
            },
            "Квавар": {
                "radius_km": "~555",
                "mass_kg": "1.4×10²¹",
                "mass_earth": 0.00023,
                "density": "~2.0",
                "gravity": "~0.4",
                "temperature": "-230°C",
                "orbital_period": "288 лет",
                "rotation_period": "8.8 часов",
                "atmosphere": "Метан",
                "moons": 1,
                "discovery": "2002, Браун и др.",
                "name_origin": "Мифическое существо народа тонгва",
                "features": "Имеет кольца как у Сатурна"
            },
            "Орк": {
                "radius_km": "~460",
                "mass_kg": "6.4×10²⁰",
                "mass_earth": 0.00011,
                "density": "~1.5",
                "gravity": "~0.3",
                "temperature": "-230°C",
                "orbital_period": "247 лет",
                "rotation_period": "13 часов",
                "atmosphere": "Метан, азот",
                "moons": 1,
                "discovery": "2004, Браун и др.",
                "name_origin": "Римский бог подземного мира",
                "features": "Назван в честь бога смерти, часто считается анти-Плутоном"
            },
            "Варуна": {
                "radius_km": "~400",
                "mass_kg": "~3.7×10²⁰",
                "mass_earth": 0.00006,
                "density": "~1.5",
                "gravity": "~0.2",
                "temperature": "-230°C",
                "orbital_period": "281 лет",
                "rotation_period": "~6 часов",
                "atmosphere": "Неизвестно",
                "moons": 0,
                "discovery": "2000, МакМиллан и др.",
                "name_origin": "Ведическое божество воды",
                "features": "Быстро вращающийся объект"
            },
            "Иксион": {
                "radius_km": "~350",
                "mass_kg": "~2.8×10²⁰",
                "mass_earth": 0.00005,
                "density": "~1.5",
                "gravity": "~0.2",
                "temperature": "-230°C",
                "orbital_period": "249 лет",
                "rotation_period": "~12 часов",
                "atmosphere": "Неизвестно",
                "moons": 0,
                "discovery": "2001, Сколл и др.",
                "name_origin": "Царь лапифов в греческой мифологии",
                "features": "Находится в резонансе с Нептуном"
            }
        }

    def show_welcome_message(self):
        """Показывает приветственное сообщение в информационной панели"""
        try:
            for widget in self.info_content.winfo_children():
                widget.destroy()  # Удаляем все виджеты из фрейма

            # Очищаем изображение
            self.planet_image_label.config(image='')

            tk.Label(self.info_content, text="🌌", bg='#1a1a2e', fg='white',
                     font=('Arial', 64)).pack(pady=30)  # Иконка галактики

            tk.Label(self.info_content, text="Добро пожаловать в симуляцию\nСолнечной системы!",
                     bg='#1a1a2e', fg='white', font=('Arial', 16, 'bold')).pack(pady=15)  # Приветствие

            tk.Label(self.info_content, text="Нажмите на любую планету,\nчтобы увидеть информацию о ней",
                     bg='#1a1a2e', fg='#ADD8E6', font=('Arial', 14)).pack(pady=15)  # Инструкция

            tk.Label(self.info_content, text="В симуляции представлены:",
                     bg='#1a1a2e', fg='yellow', font=('Arial', 14, 'bold')).pack(pady=(25, 10))  # Заголовок

            planets_list = "• 8 основных планет\n• 5 карликовых планет\n• 5 транснептуновых объектов\n• Пояс астероидов\n• Пояс Койпера"
            tk.Label(self.info_content, text=planets_list, bg='#1a1a2e', fg='white',
                     font=('Arial', 12), justify=tk.LEFT).pack(pady=10)  # Список объектов

            tk.Label(self.info_content, text="Управление:",
                     bg='#1a1a2e', fg='yellow', font=('Arial', 14, 'bold')).pack(pady=(25, 10))  # Заголовок управления

            controls = [
                "• Ползунок скорости: ускорение времени",
                "• Ползунок зума: масштабирование",
                "• Кнопка паузы: остановить/продолжить",
                "• Кнопка сброса: начать заново"
            ]

            for ctrl in controls:
                tk.Label(self.info_content, text=ctrl, bg='#1a1a2e', fg='white',
                         font=('Arial', 11), anchor='w', justify=tk.LEFT).pack(fill=tk.X, pady=3)  # Элементы управления
        except:
            pass  # Игнорируем ошибки при создании интерфейса

    def show_planet_info(self, planet_name):
        """Отображает информацию о выбранной планете"""
        try:
            if planet_name not in self.planet_info:  # Если нет подробной информации
                self.show_basic_info(planet_name)  # Показываем базовую
                return

            info = self.planet_info[planet_name]  # Получаем информацию о планете

            # Очищаем предыдущее содержимое
            for widget in self.info_content.winfo_children():
                widget.destroy()

            # Находим ключ изображения для планеты
            image_key = None
            for planet in self.planets_data:
                if planet["name"] == planet_name:
                    image_key = planet["image_key"]
                    break

            # Отображаем изображение планеты
            if image_key and image_key in self.planet_images and self.planet_images[image_key]:
                self.planet_image_label.config(image=self.planet_images[image_key])  # Устанавливаем изображение
            else:
                self.planet_image_label.config(image='')  # Убираем изображение

            # Название планеты
            tk.Label(self.info_content, text=f"🪐 {planet_name}", bg='#1a1a2e', fg='#FFD700',
                     font=('Arial', 20, 'bold')).pack(pady=10)

            # Разделитель
            tk.Frame(self.info_content, height=2, bg='#4a4a6a').pack(fill=tk.X, pady=8)

            # Основные параметры
            self.add_info_row("Радиус:", f"{info['radius_km']} км")
            self.add_info_row("Масса:", f"{info['mass_kg']} кг ({info['mass_earth']} M⊕)")
            self.add_info_row("Плотность:", f"{info['density']} г/см³")
            self.add_info_row("Сила тяжести:", f"{info['gravity']} м/с²")
            self.add_info_row("Температура:", info['temperature'])

            tk.Frame(self.info_content, height=2, bg='#4a4a6a').pack(fill=tk.X, pady=8)

            # Орбитальные характеристики
            tk.Label(self.info_content, text="Орбитальные характеристики",
                     bg='#1a1a2e', fg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=8)

            self.add_info_row("Орбитальный период:", info['orbital_period'])
            self.add_info_row("Период вращения:", info['rotation_period'])

            tk.Frame(self.info_content, height=2, bg='#4a4a6a').pack(fill=tk.X, pady=8)

            # Состав и особенности
            tk.Label(self.info_content, text="Состав и особенности",
                     bg='#1a1a2e', fg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=8)

            self.add_info_row("Атмосфера:", info['atmosphere'])
            self.add_info_row("Спутники:", str(info['moons']))
            self.add_info_row("Открытие:", info['discovery'])
            self.add_info_row("Происхождение названия:", info['name_origin'])

            tk.Label(self.info_content, text="Интересный факт:",
                     bg='#1a1a2e', fg='yellow', font=('Arial', 12, 'bold')).pack(pady=(15, 5))

            tk.Label(self.info_content, text=info['features'],
                     bg='#1a1a2e', fg='white', font=('Arial', 11),
                     wraplength=350, justify=tk.LEFT).pack(pady=8)  # Интересный факт с переносом
        except:
            pass  # Игнорируем ошибки отображения

    def show_basic_info(self, planet_name):
        """Показывает базовую информацию для планет без подробных данных"""
        try:
            for widget in self.info_content.winfo_children():
                widget.destroy()  # Очищаем фрейм

            # Очищаем изображение
            self.planet_image_label.config(image='')

            tk.Label(self.info_content, text=f"🪐 {planet_name}", bg='#1a1a2e', fg='#FFD700',
                     font=('Arial', 20, 'bold')).pack(pady=30)  # Название планеты

            tk.Label(self.info_content, text="Подробная информация\nотсутствует",
                     bg='#1a1a2e', fg='white', font=('Arial', 14)).pack(pady=15)  # Сообщение

            # Находим планету в данных и показываем базовые параметры
            for planet in self.planets_data:
                if planet["name"] == planet_name:
                    self.add_info_row("Расстояние от Солнца:", f"{planet['distance']} АЕ")
                    self.add_info_row("Относительный размер:", f"{planet['radius']} пикс")
                    break
        except:
            pass

    def add_info_row(self, label, value):
        """Добавляет строку с информацией в панель"""
        try:
            row = tk.Frame(self.info_content, bg='#1a1a2e')  # Создаем фрейм для строки
            row.pack(fill=tk.X, pady=4)  # Размещаем с заполнением

            tk.Label(row, text=label, bg='#1a1a2e', fg='#ADD8E6',
                     font=('Arial', 11, 'bold'), width=20, anchor='w').pack(side=tk.LEFT)  # Метка

            tk.Label(row, text=value, bg='#1a1a2e', fg='white',
                     font=('Arial', 11), anchor='w').pack(side=tk.LEFT, padx=8)  # Значение
        except:
            pass

    def change_time_speed(self, val):
        """Изменение скорости симуляции"""
        self.time_multiplier = float(val)  # Устанавливаем множитель времени
        self.speed_label.config(text=f"{self.time_multiplier:.1f}x")  # Обновляем текст метки

    def change_zoom(self, val):
        """Изменение масштаба"""
        self.zoom_factor = float(val)  # Устанавливаем коэффициент зума

    def toggle_pause(self):
        """Пауза/продолжение симуляции"""
        self.paused = not self.paused  # Инвертируем флаг паузы
        if self.paused:
            self.pause_btn.config(text="▶️ Пуск")  # Меняем текст кнопки
        else:
            self.pause_btn.config(text="⏸️ Пауза")  # Меняем текст кнопки
            self.animate()  # Перезапускаем анимацию

    def reset_simulation(self):
        """Сброс симуляции"""
        # Сбрасываем углы планет в случайные позиции
        for planet in self.planets_data:
            planet["angle"] = random.uniform(0, 2 * math.pi)  # Случайный угол

        # Сбрасываем ползунки
        self.time_scale.set(1.0)  # Сбрасываем скорость
        self.zoom_scale.set(1.0)  # Сбрасываем зум
        self.time_multiplier = 1.0  # Сбрасываем множитель
        self.zoom_factor = 1.0  # Сбрасываем зум
        self.speed_label.config(text="1.0x")  # Обновляем метку

        # Снимаем выделение
        self.selected_planet = None  # Убираем выбранную планету
        self.show_welcome_message()  # Показываем приветствие

    def on_canvas_click(self, event):
        """Обработка клика по canvas для выбора планеты"""
        try:
            # Получаем координаты с учетом зума
            canvas_center_x = 550  # Центр canvas по X
            canvas_center_y = 400  # Центр canvas по Y

            # Проверяем, кликнули ли по планете
            clicked_planet = None

            for planet in self.planets_data:
                # Вычисляем позицию планеты
                distance = planet["distance"] * self.AU * self.zoom_factor  # Расстояние от центра
                x = canvas_center_x + distance * math.cos(planet["angle"])  # Координата X
                y = canvas_center_y + distance * math.sin(planet["angle"])  # Координата Y

                # Проверяем расстояние от клика до центра планеты
                click_distance = math.sqrt((event.x - x) ** 2 + (event.y - y) ** 2)
                if click_distance < (planet["radius"] * self.zoom_factor + 8):  # Если попали в планету
                    clicked_planet = planet["name"]  # Запоминаем название
                    break

            if clicked_planet:
                self.selected_planet = clicked_planet  # Устанавливаем выбранную планету
                self.show_planet_info(clicked_planet)  # Показываем информацию
        except:
            pass

    def draw_asteroid_belt(self, center_x, center_y):
        """Рисует пояс астероидов"""
        try:
            belt_inner = 2.0 * self.AU * self.zoom_factor  # Внутренний радиус пояса
            belt_outer = 3.3 * self.AU * self.zoom_factor  # Внешний радиус пояса

            for _ in range(300):  # Рисуем 300 астероидов
                angle = random.uniform(0, 2 * math.pi)  # Случайный угол
                distance = random.uniform(belt_inner, belt_outer)  # Случайное расстояние

                x = center_x + distance * math.cos(angle)  # Координата X
                y = center_y + distance * math.sin(angle)  # Координата Y

                size = random.uniform(0.8, 2.0)  # Случайный размер астероида
                brightness = random.randint(100, 200)  # Случайная яркость
                color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'  # Цвет в HEX

                self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                        fill=color, outline='')  # Рисуем астероид
        except:
            pass

    def draw_kuiper_belt(self, center_x, center_y):
        """Рисует пояс Койпера"""
        try:
            belt_inner = 30.0 * self.AU * self.zoom_factor  # Внутренний радиус
            belt_outer = 50.0 * self.AU * self.zoom_factor  # Внешний радиус

            for _ in range(150):  # Рисуем 150 объектов
                angle = random.uniform(0, 2 * math.pi)  # Случайный угол
                distance = random.uniform(belt_inner, belt_outer)  # Случайное расстояние

                x = center_x + distance * math.cos(angle)  # Координата X
                y = center_y + distance * math.sin(angle)  # Координата Y

                size = random.uniform(0.5, 1.2)  # Размер объекта
                color = '#4a6a8a'  # Синеватый цвет

                self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                        fill=color, outline='')  # Рисуем объект пояса Койпера
        except:
            pass

    def animate(self):
        """Анимация движения планет"""
        if self.paused or not self.running:  # Если на паузе или программа остановлена
            return

        try:
            # Очищаем canvas
            self.canvas.delete("all")

            # Центр canvas
            center_x, center_y = 550, 400

            # Рисуем звезды фона
            self.draw_stars()

            # Рисуем орбиты
            self.draw_orbits(center_x, center_y)

            # Рисуем пояс астероидов
            self.draw_asteroid_belt(center_x, center_y)

            # Рисуем пояс Койпера
            self.draw_kuiper_belt(center_x, center_y)

            # Рисуем Солнце
            sun_radius = 35 * self.zoom_factor  # Радиус Солнца с учетом зума
            if sun_radius < 8:  # Минимальный размер
                sun_radius = 8

            # Солнце с градиентом
            self.canvas.create_oval(center_x - sun_radius, center_y - sun_radius,
                                    center_x + sun_radius, center_y + sun_radius,
                                    fill='#FFD700', outline='#FFA500', width=3)  # Рисуем Солнце

            # Корона Солнца (мерцающая)
            for i in range(16):  # 16 лучей короны
                angle = i * math.pi / 8 + (self.time_multiplier * 0.05)  # Угол с учетом времени
                length = sun_radius * (1.8 + 0.4 * math.sin(angle * 2))  # Длина луча
                x1 = center_x + length * math.cos(angle)  # Конечная точка X
                y1 = center_y + length * math.sin(angle)  # Конечная точка Y
                self.canvas.create_line(center_x, center_y, x1, y1,
                                        fill='#FF8C00', width=2, dash=(2, 3))  # Рисуем луч

            # Рисуем планеты
            planet_positions = {}

            for planet in self.planets_data:
                # Обновляем угол
                if not self.paused:
                    planet["angle"] += self.BASE_SPEED * planet["speed"] * self.time_multiplier  # Приращение угла

                # Вычисляем позицию
                distance = planet["distance"] * self.AU * self.zoom_factor  # Расстояние от Солнца
                x = center_x + distance * math.cos(planet["angle"])  # Координата X
                y = center_y + distance * math.sin(planet["angle"])  # Координата Y

                # Проверяем, видна ли планета на экране
                if -150 < x < 1250 and -150 < y < 950:
                    # Размер планеты
                    radius = planet["radius"] * self.zoom_factor  # Радиус с учетом зума
                    if radius < 2:  # Минимальный размер
                        radius = 2

                    planet_positions[planet["name"]] = (x, y)  # Сохраняем позицию

                    # Рисуем планету с эффектом объема
                    self.canvas.create_oval(x - radius, y - radius,
                                            x + radius, y + radius,
                                            fill=planet["color"], outline='white', width=2)  # Планета

                    # Для Сатурна рисуем кольца
                    if planet["name"] == "Сатурн":
                        self.canvas.create_oval(x - radius * 1.8, y - radius * 0.3,
                                                x + radius * 1.8, y + radius * 0.3,
                                                outline='#D2B48C', width=3, dash=(2, 2))  # Кольца Сатурна

                    # Блик на планете
                    self.canvas.create_oval(x - radius * 0.25, y - radius * 0.25,
                                            x + radius * 0.25, y + radius * 0.25,
                                            fill='white', outline='', stipple='gray50')  # Блик

            # Рисуем названия планет (только для крупных)
            main_planets = ["Меркурий", "Венера", "Земля", "Марс", "Юпитер",
                            "Сатурн", "Уран", "Нептун", "Плутон", "Церера", "Эрида"]

            for name, (x, y) in planet_positions.items():
                if name in main_planets:
                    if y > 700:  # Если планета внизу экрана
                        text_y = y - 35  # Текст сверху
                    else:
                        text_y = y - 25  # Текст снизу

                    self.canvas.create_text(x, text_y, text=name, fill='white',
                                            font=('Arial', 10, 'bold'))  # Название планеты

            # Если выбрана планета, выделяем её
            if self.selected_planet:
                for planet in self.planets_data:
                    if planet["name"] == self.selected_planet:
                        distance = planet["distance"] * self.AU * self.zoom_factor  # Расстояние
                        x = center_x + distance * math.cos(planet["angle"])  # Координата X
                        y = center_y + distance * math.sin(planet["angle"])  # Координата Y
                        radius = planet["radius"] * self.zoom_factor + 6  # Радиус выделения

                        # Рисуем рамку выделения
                        self.canvas.create_oval(x - radius, y - radius,
                                                x + radius, y + radius,
                                                outline='yellow', width=3, dash=(4, 4))  # Пунктирная рамка

                        # Добавляем стрелку-указатель
                        self.canvas.create_line(x, y - radius - 20, x, y - radius - 8,
                                                fill='yellow', width=3, arrow=tk.LAST)  # Стрелка
                        break

            # Продолжаем анимацию
            if self.running:
                self.animation_id = self.root.after(50, self.animate)  # Запускаем следующий кадр через 50 мс

        except Exception as e:
            if self.running:
                print(f"Ошибка в анимации: {e}")  # Вывод ошибки

    def draw_stars(self):
        """Рисует звезды фона с мерцанием"""
        try:
            # Создаем звезды только если их нет или обновляем
            if not hasattr(self, 'stars'):  # Если звезды еще не созданы
                self.stars = []  # Список звезд
                for i in range(300):  # Создаем 300 звезд
                    x = random.randint(0, 1100)  # Случайная X координата
                    y = random.randint(0, 800)  # Случайная Y координата
                    brightness = random.randint(100, 255)  # Случайная яркость
                    twinkle = random.uniform(0.5, 1.5)  # Коэффициент мерцания
                    self.stars.append((x, y, brightness, twinkle))  # Добавляем звезду в список

            # Рисуем звезды
            for i, (x, y, brightness, twinkle) in enumerate(self.stars):
                # Эффект мерцания
                if random.random() < 0.01:  # С вероятностью 1%
                    brightness = random.randint(150, 255)  # Меняем яркость

                color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'  # Цвет в HEX
                size = random.uniform(0.8, 2.0)  # Случайный размер
                self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline='')  # Рисуем звезду
        except:
            pass

    def draw_orbits(self, center_x, center_y):
        """Рисует орбиты планет с разными цветами"""
        try:
            for planet in self.planets_data:
                distance = planet["distance"] * self.AU * self.zoom_factor  # Радиус орбиты

                # Выбираем цвет орбиты в зависимости от типа планеты
                if planet["name"] in ["Меркурий", "Венера", "Земля", "Марс"]:
                    color = '#2a4a6a'  # Синий для внутренних планет
                elif planet["name"] == "Церера":
                    color = '#6a4a2a'  # Коричневый для пояса астероидов
                elif planet["name"] in ["Юпитер", "Сатурн", "Уран", "Нептун"]:
                    color = '#4a6a2a'  # Зеленый для газовых гигантов
                elif planet["name"] in ["Плутон", "Хаумеа", "Макемаке", "Эрида"]:
                    color = '#4a2a6a'  # Фиолетовый для карликовых планет
                else:
                    color = '#2a4a4a'  # Сине-зеленый для остальных

                # Рисуем орбиту
                self.canvas.create_oval(center_x - distance, center_y - distance,
                                        center_x + distance, center_y + distance,
                                        outline=color, width=2, dash=(2, 4))  # Пунктирная линия
        except:
            pass

    def on_closing(self):
        """Обработка закрытия окна"""
        self.running = False  # Останавливаем анимацию
        if self.animation_id:
            self.root.after_cancel(self.animation_id)  # Отменяем запланированную анимацию
        self.root.destroy()  # Закрываем окно


if __name__ == "__main__":
    """Точка входа в программу"""
    try:
        root = tk.Tk()  # Создаем главное окно
        app = SolarSystemSimulation(root)  # Создаем экземпляр приложения
        root.mainloop()  # Запускаем главный цикл обработки событий
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")  # Обработка Ctrl+C
        sys.exit(0)  # Выход с кодом 0 (успешно)
    except Exception as e:
        print(f"Ошибка: {e}")  # Вывод ошибки
        sys.exit(1)  # Выход с кодом 1 (ошибка)