from textual.app import ComposeResult
from textual.widgets import Button, Input, Label
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual import events
import json

class AddFoodScreen(ModalScreen):
    """Экран для добавления пищи (на 100г)"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Add your food (per 100g)"),
            Input(placeholder="Food name", id="food-name"),
            Input(placeholder="Kcal", id="food-kcal"),
            Input(placeholder="Protein", id="food-protein"),
            Input(placeholder="Fat", id="food-fat"),
            Input(placeholder="Carbs", id="food-carbs"),
            Horizontal(
                Button("Add", id="add-food-btn"),
                Button("Cancel", id="cancel-food-btn"),
            ),
            id="add-food-container"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Валидация числовых полей"""
        numeric_fields = {"food-kcal", "food-protein", "food-fat", "food-carbs"}
        
        if event.input.id in numeric_fields:
            # Удаляем все нечисловые символы
            cleaned_value = ''.join(filter(str.isdigit, event.input.value))

            # Убираем ведущие нули, кроме случая когда число равно 0
            if cleaned_value.startswith('0') and len(cleaned_value) > 1:
                cleaned_value = cleaned_value.lstrip('0')
                if not cleaned_value:  # Если после удаления нулей ничего не осталось
                    cleaned_value = '0'

            
            # Если значение изменилось после очистки, обновляем поле
            if cleaned_value != event.input.value:
                event.input.value = cleaned_value
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Обработка нажатия Enter - переход к следующему полю"""
        if event.input.value.strip():  # Если поле не пустое
            self.focus_next_widget(event.input)
    
    def focus_next_widget(self, current_input: Input) -> None:
        """Переход к следующему виджету (поле или кнопка)"""
        inputs = list(self.query(Input))
        buttons = list(self.query(Button))
        all_widgets = inputs + buttons
        
        current_index = None
        
        # Находим индекс текущего поля среди всех виджетов
        for i, widget in enumerate(all_widgets):
            if widget == current_input:
                current_index = i
                break
        
        # Если нашли текущий виджет и есть следующий - фокусируемся на нем
        if current_index is not None and current_index < len(all_widgets) - 1:
            next_widget = all_widgets[current_index + 1]
            next_widget.focus()

    def on_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш"""
        if event.key == "escape":
            self.dismiss()  # ESC == Cancel

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-food-btn":
            self.add_food()
        else:
            self.dismiss()
    
    def add_food(self) -> None:
        """Добавление приема пищи в файл food.json"""
        try:
            # Получаем значения из полей ввода
            food_name = self.query_one("#food-name", Input).value.strip()
            kcal = self.query_one("#food-kcal", Input).value.strip()
            protein = self.query_one("#food-protein", Input).value.strip()
            fat = self.query_one("#food-fat", Input).value.strip()
            carbs = self.query_one("#food-carbs", Input).value.strip()
            
            # Проверяем, что все обязательные поля заполнены
            if not all([food_name, kcal, protein, fat, carbs]):
                self.notify("Please fill all fields", severity="error")
                return
            
            # Преобразуем числовые значения
            try:
                food_data = {
                    "food": food_name,
                    "Caloric Value": int(kcal),
                    "Protein": int(protein),
                    "Fat": int(fat),
                    "Carbohydrates": int(carbs)
                }
            except ValueError:
                self.notify("Please enter valid numbers", severity="error")
                return
            
            # Читаем существующие данные из файла
            try:
                with open("food.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            
            # Добавляем новую запись
            data.append(food_data)
            
            # Записываем обновленные данные обратно в файл
            with open("food.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.notify("Food added successfully!", severity="information")
            self.dismiss()
            
        except Exception as e:
            self.notify(f"Food adding meal: {str(e)}", severity="error")
