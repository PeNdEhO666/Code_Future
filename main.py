import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Предопределённые задачи
        self.predefined_tasks = [
            {"name": "Прочитать статью по Python", "type": "учёба"},
            {"name": "Сделать зарядку 15 минут", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Изучить новый фреймворк", "type": "учёба"},
            {"name": "Пробежка 2 км", "type": "спорт"},
            {"name": "Провести встречу", "type": "работа"},
            {"name": "Решить задачу на LeetCode", "type": "учёба"},
            {"name": "Йога и растяжка", "type": "спорт"},
            {"name": "Обновить документацию", "type": "работа"}
        ]
        
        # История задач (каждая задача - словарь с полями: name, type, timestamp)
        self.history = []
        
        # Загрузка истории из файла
        self.load_history()
        
        # Переменные для фильтра
        self.filter_var = tk.StringVar(value="все")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения истории
        self.update_history_display()
    
    def create_widgets(self):
        # Верхняя панель с кнопкой генерации
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Button(top_frame, text="🎲 Сгенерировать задачу", 
                  command=self.generate_task, width=25).pack(pady=5)
        
        # Панель фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация по типу", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Radiobutton(filter_frame, text="Все задачи", variable=self.filter_var, 
                       value="все", command=self.update_history_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Учёба", variable=self.filter_var, 
                       value="учёба", command=self.update_history_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Спорт", variable=self.filter_var, 
                       value="спорт", command=self.update_history_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Работа", variable=self.filter_var, 
                       value="работа", command=self.update_history_display).pack(side=tk.LEFT, padx=5)
        
        # Панель добавления новой задачи
        add_frame = ttk.LabelFrame(self.root, text="Добавить свою задачу", padding="10")
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(add_frame, text="Название:").pack(side=tk.LEFT, padx=5)
        self.new_task_entry = ttk.Entry(add_frame, width=30)
        self.new_task_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_frame, text="Тип:").pack(side=tk.LEFT, padx=5)
        self.type_combobox = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], 
                                          width=10, state="readonly")
        self.type_combobox.set("учёба")
        self.type_combobox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_frame, text="➕ Добавить", command=self.add_custom_task).pack(side=tk.LEFT, padx=5)
        
        # История задач
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Список с прокруткой
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set,
                                          font=("Arial", 10), height=15)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопка очистки истории
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)
        
        ttk.Button(bottom_frame, text="🗑️ Очистить историю", 
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="💾 Сохранить историю", 
                  command=self.save_history).pack(side=tk.LEFT, padx=5)
    
    def generate_task(self):
        """Генерирует случайную задачу из предопределённого списка"""
        if self.predefined_tasks:
            task = random.choice(self.predefined_tasks).copy()
            task["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(task)
            self.save_history()
            self.update_history_display()
            
            # Показываем уведомление
            messagebox.showinfo("Новая задача", f"Ваша задача на сегодня:\n\n{task['name']}")
    
    def add_custom_task(self):
        """Добавляет пользовательскую задачу"""
        task_name = self.new_task_entry.get().strip()
        task_type = self.type_combobox.get()
        
        # Проверка на пустую строку
        if not task_name:
            messagebox.showwarning("Ошибка", "Название задачи не может быть пустым!")
            return
        
        # Добавляем задачу
        new_task = {
            "name": task_name,
            "type": task_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(new_task)
        
        # Очищаем поле ввода
        self.new_task_entry.delete(0, tk.END)
        
        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Успех", f"Задача '{task_name}' добавлена в историю!")
    
    def update_history_display(self):
        """Обновляет отображение истории с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        
        filter_type = self.filter_var.get()
        
        # Фильтруем задачи
        filtered_history = self.history
        if filter_type != "все":
            filtered_history = [task for task in self.history if task["type"] == filter_type]
        
        # Отображаем задачи в обратном порядке (новые сверху)
        for task in reversed(filtered_history):
            display_text = f"[{task['timestamp']}] [{task['type'].upper()}] {task['name']}"
            self.history_listbox.insert(tk.END, display_text)
        
        # Обновляем статус
        count = len(filtered_history)
        self.root.title(f"Random Task Generator - Задач в истории: {count}")
    
    def clear_history(self):
        """Очищает всю историю"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("История очищена", "Все задачи удалены из истории.")
    
    def save_history(self):
        """Сохраняет историю в JSON файл"""
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
    
    def load_history(self):
        """Загружает историю из JSON файла"""
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
                self.history = []

def main():
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
