from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, ListView, ListItem
from textual import events
import json

class RemoveScreenFood(ModalScreen):
    """Экран для удаления приемов пищи или продуктов"""
    
    def __init__(self):
        super().__init__()
        self.foods_data = self.load_foods()
        self.filtered_foods = self.foods_data.copy()
        self.selected_indices = set()
    
    def load_foods(self):
        """Загрузка базы продуктов"""
        try:
            with open("data/food.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Select then remove food", classes="title"),
            Input(placeholder="Search food...", id="food-search"),
            ListView(
                *[ListItem(Label(f"{food['food']} - {food['Caloric Value']}kcal")) 
                for food in self.filtered_foods],
                id="food-results",
                classes="search-results"
            ),
            Horizontal(
                Button("Delete Selected", id="delete-btn", variant="error"),
                Button("Cancel", id="cancel-btn"),
                id="buttons-container"
            ),
            id="remove-food-container"
        )
    
    def on_mount(self) -> None:
        """Установка фокуса на поисковую строку при открытии"""
        self.query_one("#food-search").focus()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Обработка поиска"""
        if event.input.id == "food-search":
            search_term = event.input.value.lower().strip()
            if not search_term:
                self.filtered_foods = self.foods_data.copy()
            else:
                self.filtered_foods = [
                    food for food in self.foods_data 
                    if search_term in food['food'].lower()
                ]
            
            # Обновление списка результатов
            results_list = self.query_one("#food-results")
            results_list.clear()
            for food in self.filtered_foods:
                results_list.append(
                    ListItem(Label(f"{food['food']} - {food['Caloric Value']}kcal"))
                )
            
            # Сброс выделения при изменении поиска
            self.selected_indices.clear()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Обработка выбора продукта из списка"""
        if not self.filtered_foods:
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
        results_list = self.query_one("#food-results")
        
        for i, item in enumerate(results_list.children):
            if i in self.selected_indices:
                item.add_class("selected")
            else:
                item.remove_class("selected")
    
    def on_list_view_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш в ListView"""
        if event.key == "enter":
            # При нажатии Enter - переключаем выделение текущего элемента
            if self.filtered_foods:
                results_list = self.query_one("#food-results")
                current_index = results_list.index
                
                # Переключаем выделение
                if current_index in self.selected_indices:
                    self.selected_indices.remove(current_index)
                else:
                    self.selected_indices.add(current_index)
                
                # Обновляем стили
                self.update_selection_styles()
                
                event.stop()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Обработка нажатия Enter в поиске - переход к списку"""
        if event.input.id == "food-search":
            if self.filtered_foods:
                results_list = self.query_one("#food-results")
                results_list.focus()
                results_list.index = 0
    
    def on_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш"""
        if event.key == "escape":
            self.dismiss()
        elif event.key == "ctrl+t":
            self.query_one("#food-search").focus()
            # Сброс выделения при переходе к поиску
            self.selected_indices.clear()
            self.update_selection_styles()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработка нажатия кнопок"""
        if event.button.id == "delete-btn":
            self.delete_foods()
        else:
            self.dismiss()
    
    def delete_foods(self) -> None:
        """Удаление выбранных продуктов из food.json"""
        try:
            if not self.selected_indices:
                self.notify("Please select foods first", severity="error")
                return
            
            # Получаем выбранные продукты для удаления
            foods_to_delete = []
            for index in sorted(self.selected_indices, reverse=True):
                if index < len(self.filtered_foods):
                    foods_to_delete.append(self.filtered_foods[index])
            
            if not foods_to_delete:
                self.notify("No valid foods selected", severity="error")
                return
            
            # Подтверждение удаления (можно добавить диалог подтверждения)
            food_names = [food['food'] for food in foods_to_delete]
            
            # Удаляем выбранные продукты из данных
            self.foods_data = [
                food for food in self.foods_data 
                if food not in foods_to_delete
            ]
            
            # Сохраняем обновленные данные
            with open("data/food.json", "w", encoding="utf-8") as f:
                json.dump(self.foods_data, f, indent=4, ensure_ascii=False)
            
            # Обновляем отфильтрованный список
            self.filtered_foods = [
                food for food in self.filtered_foods 
                if food not in foods_to_delete
            ]
            
            # Обновляем список на экране
            results_list = self.query_one("#food-results")
            results_list.clear()
            for food in self.filtered_foods:
                results_list.append(
                    ListItem(Label(f"{food['food']} - {food['Caloric Value']}kcal"))
                )
            
            # Сброс выделения
            self.selected_indices.clear()
            
            # Если список не пуст, устанавливаем фокус на первый элемент
            if self.filtered_foods:
                results_list.index = 0
                results_list.focus()
            else:
                # Если список пуст, переходим к поиску
                self.query_one("#food-search").focus()
            
            if len(food_names) == 1:
                self.notify(f"'{food_names[0]}' deleted successfully!", severity="information")
            else:
                self.notify(f"Deleted {len(food_names)} items successfully!", severity="information")
            
        except Exception as e:
            self.notify(f"Error deleting food: {str(e)}", severity="error")