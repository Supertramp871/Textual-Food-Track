from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListView, ListItem
from textual import events
import json
from datetime import datetime

class RemoveScreenMeal(ModalScreen):
    """Экран для удаления приемов пищи за сегодняшний день"""
    
    def __init__(self):
        super().__init__()
        self.meals_data = self.load_meals()
        self.today_meals = self.filter_today_meals()
        self.selected_indices = set()
    
    def load_meals(self):
        """Загрузка базы приемов пищи"""
        try:
            with open("data/meals.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def filter_today_meals(self):
        """Фильтрация приемов пищи за сегодняшний день"""
        today = datetime.now().strftime("%d.%m.%Y")
        return [
            meal for meal in self.meals_data 
            if meal['Datetime'].endswith(today)
        ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Select meals to remove (today only)", classes="title"),
            ListView(
                *[ListItem(Label(self.format_meal_display(meal))) 
                for meal in self.today_meals],
                id="meal-results",
                classes="search-results"
            ),
            Horizontal(
                Button("Delete Selected", id="delete-btn", variant="error"),
                Button("Cancel", id="cancel-btn"),
                id="buttons-container"
            ),
            id="remove-meal-container"
        )
    
    def format_meal_display(self, meal):
        """Форматирование отображения приема пищи"""
        return (f"{meal['food']} - {meal['Grams']}g - "
                f"{meal['Caloric Value']}kcal - {meal['Datetime']}")
    
    def on_mount(self) -> None:
        """Установка фокуса на список при открытии"""
        if self.today_meals:
            self.query_one("#meal-results").focus()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Обработка выбора приема пищи из списка"""
        if not self.today_meals:
            return
        
        selected_index = event.list_view.index
        
        # Переключаем выделение: если уже выделен - снимаем, если нет - добавляем
        if selected_index in self.selected_indices:
            self.selected_indices.remove(selected_index)
        else:
            self.selected_indices.add(selected_index)
        
        # Обновляем стили всех элементов
        self.update_selection_styles()
    
    def update_selection_styles(self):
        """Обновление стилей всех элементов списка"""
        results_list = self.query_one("#meal-results")
        
        for i, item in enumerate(results_list.children):
            if i in self.selected_indices:
                item.add_class("selected")
            else:
                item.remove_class("selected")
    
    def on_list_view_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш в ListView"""
        if event.key == "enter":
            # При нажатии Enter - переключаем выделение текущего элемента
            if self.today_meals:
                results_list = self.query_one("#meal-results")
                current_index = results_list.index
                
                # Переключаем выделение
                if current_index in self.selected_indices:
                    self.selected_indices.remove(current_index)
                else:
                    self.selected_indices.add(current_index)
                
                # Обновляем стили
                self.update_selection_styles()
                
                event.stop()
    
    def on_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш"""
        if event.key == "escape":
            self.dismiss()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработка нажатия кнопок"""
        if event.button.id == "delete-btn":
            self.delete_meals()
        else:
            self.dismiss()
    
    def delete_meals(self) -> None:
        """Удаление выбранных приемов пищи из meals.json"""
        try:
            if not self.selected_indices:
                self.notify("Please select meals first", severity="error")
                return
            
            # Получаем выбранные приемы пищи для удаления
            meals_to_delete = []
            for index in sorted(self.selected_indices, reverse=True):
                if index < len(self.today_meals):
                    meals_to_delete.append(self.today_meals[index])
            
            if not meals_to_delete:
                self.notify("No valid meals selected", severity="error")
                return
            
            # Удаляем выбранные приемы пищи из данных
            self.meals_data = [
                meal for meal in self.meals_data 
                if meal not in meals_to_delete
            ]
            
            # Сохраняем обновленные данные
            with open("data/meals.json", "w", encoding="utf-8") as f:
                json.dump(self.meals_data, f, indent=4, ensure_ascii=False)
            
            # Обновляем список за сегодня
            self.today_meals = [
                meal for meal in self.today_meals 
                if meal not in meals_to_delete
            ]
            
            # Обновляем список на экране
            results_list = self.query_one("#meal-results")
            results_list.clear()
            for meal in self.today_meals:
                results_list.append(
                    ListItem(Label(self.format_meal_display(meal)))
                )
            
            # Сброс выделения
            self.selected_indices.clear()
            
            # Если список не пуст, устанавливаем фокус на первый элемент
            if self.today_meals:
                results_list.index = 0
                results_list.focus()
            
            # Уведомление об успешном удалении
            if len(meals_to_delete) == 1:
                self.notify(f"'{meals_to_delete[0]['food']}' deleted successfully!", severity="information")
            else:
                self.notify(f"Deleted {len(meals_to_delete)} meals successfully!", severity="information")
            
        except Exception as e:
            self.notify(f"Error deleting meal: {str(e)}", severity="error")