from textual.app import ComposeResult
from textual.widgets import Button, Input, Label
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual import events
import json
import os

class SetTargets(ModalScreen):
    """Экран для установки цели по КБЖУ"""
    
    def compose(self) -> ComposeResult:
        # Пытаемся загрузить текущие цели для отображения
        current_targets = self.load_current_targets()
        
        yield Container(
            Label("Set your daily targets"),
            Input(placeholder="Daily calories", id="target-kcal", value=str(current_targets.get("calories", ""))),
            Input(placeholder="Protein (g)", id="target-protein", value=str(current_targets.get("protein", ""))),
            Input(placeholder="Fat (g)", id="target-fat", value=str(current_targets.get("fat", ""))),
            Input(placeholder="Carbs (g)", id="target-carbs", value=str(current_targets.get("carbs", ""))),
            Horizontal(
                Button("Save", id="save-targets-btn"),
                Button("Cancel", id="cancel-targets-btn"),
            ),
            id="set-targets-container"
        )

    def load_current_targets(self) -> dict:
        """Загружает текущие цели из файла"""
        try:
            with open("data/targets.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Возвращаем пустые значения, если файла нет или он поврежден
            return {"calories": "", "protein": "", "fat": "", "carbs": ""}

    def on_input_changed(self, event: Input.Changed) -> None:
        """Валидация числовых полей"""
        numeric_fields = {"target-kcal", "target-protein", "target-fat", "target-carbs"}
        
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
        if event.button.id == "save-targets-btn":
            self.save_targets()
        else:
            self.dismiss()
    
    def save_targets(self) -> None:
        """Сохранение целей в файл targets.json"""
        try:
            # Получаем значения из полей ввода
            kcal = self.query_one("#target-kcal", Input).value.strip()
            protein = self.query_one("#target-protein", Input).value.strip()
            fat = self.query_one("#target-fat", Input).value.strip()
            carbs = self.query_one("#target-carbs", Input).value.strip()
            
            # Проверяем, что все обязательные поля заполнены
            if not all([kcal, protein, fat, carbs]):
                self.notify("Please fill all fields", severity="error")
                return
            
            # Преобразуем числовые значения
            try:
                targets_data = {
                    "calories": int(kcal),
                    "protein": int(protein),
                    "fat": int(fat),
                    "carbs": int(carbs)
                }
            except ValueError:
                self.notify("Please enter valid numbers", severity="error")
                return
            
            # Записываем данные в файл
            with open("data/targets.json", "w", encoding="utf-8") as f:
                json.dump(targets_data, f, indent=4, ensure_ascii=False)
            
            self.notify("Targets saved successfully!", severity="information")
            self.dismiss()
            
        except Exception as e:
            self.notify(f"Error saving targets: {str(e)}", severity="error")