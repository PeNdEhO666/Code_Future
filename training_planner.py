import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x500")
        
        # Данные для хранения тренировок
        self.trainings = []
        self.data_file = "trainings.json"
        
        # Загрузка данных из JSON
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Поле Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Поле Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=["Бег", "Плавание", "Велосипед", "Йога", "Силовая"], width=15)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Поле Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Кнопка Добавить
        self.add_btn = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Рамка для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type_var = tk.StringVar(value="Все")
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["Все", "Бег", "Плавание", "Велосипед", "Йога", "Силовая"], width=15)
        self.filter_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.filter_type_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.filter_date_entry.bind("<KeyRelease>", lambda e: self.refresh_table())
        
        # Кнопка сброса фильтров
        self.reset_btn = ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters)
        self.reset_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Таблица для отображения тренировок
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание Treeview
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Дата", "Тип", "Длительность"), show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность (мин)")
        
        self.tree.column("ID", width=50)
        self.tree.column("Дата", width=100)
        self.tree.column("Тип", width=150)
        self.tree.column("Длительность", width=120)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка удаления
        self.delete_btn = ttk.Button(self.root, text="Удалить выбранную тренировку", command=self.delete_training)
        self.delete_btn.pack(pady=5)
    
    def validate_date(self, date_str):
        """Проверка формата даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_duration(self, duration_str):
        """Проверка длительности (положительное число)"""
        try:
            duration = float(duration_str)
            return duration > 0
        except ValueError:
            return False
    
    def add_training(self):
        """Добавление новой тренировки"""
        date = self.date_entry.get().strip()
        training_type = self.type_var.get().strip()
        duration = self.duration_entry.get().strip()
        
        # Валидация
        if not date:
            messagebox.showerror("Ошибка", "Введите дату")
            return
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return
        
        if not training_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return
        
        if not duration:
            messagebox.showerror("Ошибка", "Введите длительность")
            return
        
        if not self.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return
        
        # Создание ID
        training_id = max([t["id"] for t in self.trainings], default=0) + 1
        
        # Добавление тренировки
        training = {
            "id": training_id,
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }
        
        self.trainings.append(training)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей (кроме даты)
        self.type_var.set("")
        self.duration_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Тренировка добавлена!")
    
    def delete_training(self):
        """Удаление выбранной тренировки"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тренировку для удаления")
            return
        
        # Получение ID из выбранной строки
        item = self.tree.item(selected[0])
        training_id = item["values"][0]
        
        # Удаление из списка
        self.trainings = [t for t in self.trainings if t["id"] != training_id]
        
        self.save_data()
        self.refresh_table()
        messagebox.showinfo("Успех", "Тренировка удалена!")
    
    def filter_trainings(self):
        """Фильтрация тренировок"""
        filtered = self.trainings.copy()
        
        # Фильтр по типу
        filter_type = self.filter_type_var.get()
        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]
        
        # Фильтр по дате
        filter_date = self.filter_date_entry.get().strip()
        if filter_date:
            if self.validate_date(filter_date):
                filtered = [t for t in filtered if t["date"] == filter_date]
            else:
                # Если дата невалидна, показываем все
                pass
        
        return filtered
    
    def refresh_table(self):
        """Обновление таблицы"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Получение отфильтрованных данных
        filtered = self.filter_trainings()
        
        # Заполнение таблицы
        for training in filtered:
            self.tree.insert("", "end", values=(
                training["id"],
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_table()
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.trainings = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.trainings = []
        else:
            self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
