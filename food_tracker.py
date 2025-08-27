# ТЗ

# %/ это коментарий /%
# --- Text --- обозначет центрирование


# ГЛАВНЫЙ ЭКРАН
# --- Daily progress ?/KCTARGET kcal (...%) ---
#   Prot ?/PTARGET (...%) missed ... prots
#   Fat ?/FTARGET (...%) over ... fats
#   Carbs ?/CTARGET (...%) missed ... carbs

# %/ где ...% процент употребленных kc/p/f/c от TARGET, missed/over ... перебор или недобор p/f/c в числовом формате /%

# Today meals
#   Chicken 533/45/3/4 (100g)       Adolf 455/11/40/2 (20g)     Chicken 533/45/3/4 (100g)
#   Rice 100/23/2/1 (700g)          Dog 344/23/45/1 (2000g)     Dog 344/23/45/1 (2000g)
#   Rice 100/23/2/1 (700g)          Dog 344/23/45/1 (2000g)     Dog 344/23/45/1 (2000g)
#   ... %/ scrolable element /%

# %/ Числа взяты для примера все данные должны браться из файла meals.json за сегодняшний день/%

# Footer
# r Add Meal t Add Food ^r Remove Meal ^T Remove food u Show statistic s Set Target


# ОПЦИИ

# Add Meal 
#   Enter data about todays meal
#       Name: Any name
#       Kcal: Onlu int
#       Prot: Only int
#       Fat: Only int
#       Carbs: Only int
#       Grams: Only int
# /% Внешний вид релизован механика добавления приема пищи нет %/


# Add food
#   Enter data about new Food (Nutrition on 100g)
#   (check that ths is new food try find it in list of foods)
#       Name: Any name
#       Kcal: Onlu int
#       Prot: Only int
#       Fat: Only int
#       Carbs: Only int
# /% Внешний вид релизован механика добавления блюда нет %/

# Remove Meal
#   Select then remove meal
#   блок 1
#   /% Выводится список приемов пищи за сегодня%/
#       - meal 1
#       - meal 2 
#       - ... 
#   конец блока 1
#   блок 2 и 3
#       Delete Selected / Exit 
#   конец блока 2 и 3
#  %/ при нажатии ctlr + t по умолчанию фокус на блоке 1 и 
#  при нажатии таба фокус идет на блок 2 затем на блок 3
#  и так по кругу стандартное поведение 
#  когда фокус на блоке 1 выбранный прием пищ подсвечивается 
#  при нажатии enter он выделяется и фокус переходит на след прием пищи /%

# Remove Food
#   Select then remove food
#   блок 1
#      Seacrh Line:      
#   конец блока 1 
#   блок 2
#   /% Выводится весь список продуктов и из nutritin_data.json и из food.json %/
#       - rice
#       - bacon 
#       - ... 
#   конец блока 2
#   блок 3 и 4
#       Delete Selected / Exit 
#   конец блока 3 и 4
#  %/ при нажатии ctlr + t по умолчанию фокус на блоке 1 и 
#  поле готову к вводу названия продука 
#  при нажатии таба фокус идет на блок 2 затем на блок 3 затем на блок 4
#  и так по кругу стандартное поведение 
#  когда фокус на блоке 2 выбранный продуктв подсвечивается 
#  при нажатии enter он выделяется и фокус переходит на след продукт /%



# Show statistic
#  do this later, after complete all of other things

# Set target
# Set your goals
#   Ccalorie: Only int
#   Protein: Only int
#   Fat: Only int
#   Carbs: Only int

# База данных по умолчания nutridion_data.json
# данные пользовательских блюд food.json
# формат для них одинаков   
    # "food":"cream cheese",
    # "Caloric Value":51,
    # "Protein":0.9,
    # "Fat":5.0,
    # "Carbohydrates":0.8
# данные приемов пищи meal.json
# тут надо скорее всего учитьывать дату в полном формате: 14:30 28.08.2025
    # "food":"cream cheese",
    # "Caloric Value":51,
    # "Protein":1,
    # "Fat":5,
    # "Carbohydrates":1,
    # "Datatime":14:30-28.08.2025


from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Button, Input, Label
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from textual import events
from typing import List, Dict, Any
from datetime import datetime
import json


DEFAULT_TARGETS = {
    "kcal": 2500,
    "protein": 150,
    "fat": 70,
    "carbs": 300
}

class Food:
    """Класс кбжу блюда на 100 грамм"""
    def __init__(self, name: str, kcal: int, protein: int, fat: int, carbs: int):
        self.name = name
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.grams = 100
    
    def __str__(self):
        return (f"K{self.kcal}/, P{self.protein}/"f"F{self.fat}/, C{self.carbs}g")

class Meal:
    """Класс для представления приема пищи"""
    def __init__(self, name: str, kcal: int, protein: int, fat: int, carbs: int, gramms: int):
        self.name = name
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.gramms = gramms
        self.time = datetime.now().strftime("%H:%M-%d.%m.%Y")
    
    def __str__(self):
        return (f"'{self.name}', kcal={self.kcal}, protein={self.protein}g, "
                f"fat={self.fat}g, carbs={self.carbs}g, gramms={self.gramms}g, "
                f"time='{self.time}')")

class AddMealScreen(ModalScreen):
    """Экран для добавления приема пищи"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Add your today meal"),
            Input(placeholder="Food name", id="meal-name"),
            Input(placeholder="Kcal", id="meal-kcal"),
            Input(placeholder="Protein", id="meal-protein"),
            Input(placeholder="Fat", id="meal-fat"),
            Input(placeholder="Carbs", id="meal-carbs"),
            Input(placeholder="Grams", id="meal-grams", value="100"),
            Horizontal(
                Button("Add", id="add-meal-btn"),
                Button("Cancel", id="cancel-meal-btn"),
            ),
            id="add-meal-container"
        )
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Валидация числовых полей"""
        numeric_fields = {"meal-kcal", "meal-protein", "meal-fat", "meal-carbs", "meal-grams"}
        
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
        if event.button.id == "add-meal-btn":
            self.add_meal()
        else:
            self.dismiss()
    
    def add_meal(self) -> None:
        """Добавление приема пищи в файл meals.json"""
        try:
            # Получаем значения из полей ввода
            food_name = self.query_one("#meal-name", Input).value.strip()
            kcal = self.query_one("#meal-kcal", Input).value.strip()
            protein = self.query_one("#meal-protein", Input).value.strip()
            fat = self.query_one("#meal-fat", Input).value.strip()
            carbs = self.query_one("#meal-carbs", Input).value.strip()
            grams = self.query_one("#meal-grams", Input).value.strip()
            
            # Проверяем, что все обязательные поля заполнены
            if not all([food_name, kcal, protein, fat, carbs, grams]):
                self.notify("Please fill all fields", severity="error")
                return
            
            # Преобразуем числовые значения
            try:
                meal_data = {
                    "food": food_name,
                    "Caloric Value": int(kcal),
                    "Protein": int(protein),
                    "Fat": int(fat),
                    "Carbohydrates": int(carbs),
                    "Grams": int(grams),
                    "Datetime": datetime.now().strftime("%H:%M-%d.%m.%Y")
                }
            except ValueError:
                self.notify("Please enter valid numbers", severity="error")
                return
            
            # Читаем существующие данные из файла
            try:
                with open("meals.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            
            # Добавляем новую запись
            data.append(meal_data)
            
            # Записываем обновленные данные обратно в файл
            with open("meals.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.notify("Meal added successfully!", severity="information")
            self.dismiss()
            
        except Exception as e:
            self.notify(f"Error adding meal: {str(e)}", severity="error")
        
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

class RemoveScreenMeal(ModalScreen):
    """Экран для удаления приемов пищи или продуктов"""

class RemoveScreenFood(ModalScreen):
    """Экран для удаления приемов пищи или продуктов """

class StatisticScreen(ModalScreen):
    """Экран для показа статистики"""

class SetTargets(ModalScreen):
    """Экран для установки цели по кбжу"""

class MainDisplay(Static): # Должен быть не статичным а после добавления или удаления Приема пищи полностью обновлятся
    """Основной виджет для отображения прогресса и истории"""
    
    def __init__(self):
        super().__init__()
        self.daily_progress = {
            # это пример даннные должны загружаться из meal.json за сегодняшний день и вычисляться
            'kcal': {'current': 123, 'target': 3500, 'percent': 4},
            'protein': {'current': 3, 'target': 4, 'percent': 3, 'status': 'missed', 'value': 40},
            'fat': {'current': 500, 'target': 50, 'percent': 6, 'status': 'over', 'value': 30},
            'carbs': {'current': 7, 'target': 100, 'percent': 5, 'status': 'missed', 'value': 3}
        }
        self.history_meals = [
            {"name": "Niger", "values": "533/45/3/4", "grams": "100g"},
            {"name": "Adolf", "values": "455/11/40/2", "grams": "20g"},
            {"name": "Rice", "values": "100/23/2/1", "grams": "700g"}
        ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            self.render_daily_progress(),
            self.render_history(),
            id="main-container"
        )
    
    def render_daily_progress(self) -> Static:
        """Рендеринг дневного прогресса"""
        progress = self.daily_progress
        content = f"Daily progress {progress['kcal']['current']}/{progress['kcal']['target']} kcal ({progress['kcal']['percent']}%)\n"
        content += f"    Prot {progress['protein']['current']}/{progress['protein']['target']} ({progress['protein']['percent']}%) {progress['protein']['status']} {progress['protein']['value']} prots\n"
        content += f"    Fat {progress['fat']['current']}/{progress['fat']['target']} ({progress['fat']['percent']}%) {progress['fat']['status']} {progress['fat']['value']} fats\n"
        content += f"    Carbs {progress['carbs']['current']}/{progress['carbs']['target']} ({progress['carbs']['percent']}%) {progress['carbs']['status']} {progress['carbs']['value']} carbs"
        return Static(content, id="daily-progress")
    
    def render_history(self) -> Static:
        """Рендеринг истории питания"""
        content = "History meals\n"
        for food in self.history_meals:
            content += f"    {food['name']} {food['values']} ({food['grams']})\n"
        return Static(content, id="history-meals")


class FoodTracker(App):
    """A Textual track food."""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("r", "add_meal", "Add meal"),
        ("t", "add_food", "Add food"),
        ("ctrl+r", "remove_meal", "Remove meal"),
        ("ctrl+t", "remove_food", "Remove food"),
        ("s", "set_targets", "Set targets"),
        ("u", "show_statistic", "Show statistic"),
        ("q", "quit", "Quit"),
    ]

    def save_data(self) -> None:
        """Сохранение данных в файл."""
        # TODO: Реализовать сохранение данных
        pass
    
    def load_data(self) -> None:
        """Загрузка данных из файла."""
        # TODO: Реализовать загрузку данных
        pass
    
    def generate_statistics(self):
        """Генерация статистики."""
        # TODO: Реализовать генерацию статистики

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield MainDisplay()
        yield Footer()

    # region Основные действия
    def action_add_meal(self) -> None:
        """Действие для добавления приема пищи."""
        self.push_screen(AddMealScreen())
    
    def action_add_food(self) -> None:
        """Действие для добавления продукта."""
        self.push_screen(AddFoodScreen())
    
    def action_remove_meal(self) -> None:
        """Действие для удаления приема пищи."""
        #self.push_screen(RemoveScreenMeal())
    
    def action_remove_food(self) -> None:
        """Действие для удаления продукта."""
        #self.push_screen(RemoveScreenFood())
    
    def action_set_targets(self) -> None:
        """Действие для установки целей."""
        #self.push_screen(SetTargets())

    def action_show_statistic(self) -> None:
        """Действие для показа статистики."""
        #self.push_screen(StatisticScreen())
    # endregion
    

if __name__ == "__main__":
    app = FoodTracker()
    app.run()