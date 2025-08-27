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
# не получается динамически обновлять показатели главного экрана

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
# /% ХЗ как работает %/


# Add food
#   Enter data about new Food (Nutrition on 100g)
#   (check that ths is new food try find it in list of foods)
#       Name: Any name
#       Kcal: Onlu int
#       Prot: Only int
#       Fat: Only int
#       Carbs: Only int
# /% ХЗ как работает %/

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
from textual.widgets import Footer, Header
from textual.screen import ModalScreen
from datetime import datetime

import AddFoodScreen
import AddMealScreen
from MainDisplay import MainDisplay
import DefaultTargets


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

class RemoveScreenMeal(ModalScreen):
    """Экран для удаления приемов пищи или продуктов"""

class RemoveScreenFood(ModalScreen):
    """Экран для удаления приемов пищи или продуктов """

class StatisticScreen(ModalScreen):
    """Экран для показа статистики"""

class SetTargets(ModalScreen):
    """Экран для установки цели по кбжу"""


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

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield MainDisplay()
        yield Footer()

    # region Основные действия
    def action_add_meal(self) -> None:
        """Действие для добавления приема пищи."""
        self.push_screen(AddMealScreen.AddMealScreen())

    def action_add_food(self) -> None:
        """Действие для добавления продукта."""
        self.push_screen(AddFoodScreen.AddFoodScreen())
    
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