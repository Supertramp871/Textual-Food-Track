from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.screen import ModalScreen
from datetime import datetime
import os

import modules.AddFoodScreen as AddFoodScreen
import modules.AddMealScreen as AddMealScreen
import modules.MainDisplay as MainDisplay
import modules.RemoveFoodScreen as RemoveFoodScreen
import modules.RemoveMealScreen as RemoveMealScreen
import modules.SetTargets as SetTargets
import modules.StatisticScreen as StatisticScreen

class Food: 
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

class FoodTracker(App):
    CSS_PATH = "styles/styles.tcss"

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
        yield Header()
        yield MainDisplay.MainDisplay()
        yield Footer()

    def action_add_meal(self) -> None:
        self.push_screen(AddMealScreen.AddMealScreen())

    def action_add_food(self) -> None:
        self.push_screen(AddFoodScreen.AddFoodScreen())
    
    def action_remove_meal(self) -> None:
        self.push_screen(RemoveMealScreen.RemoveScreenMeal())
    
    def action_remove_food(self) -> None:
        self.push_screen(RemoveFoodScreen.RemoveScreenFood())
    
    def action_set_targets(self) -> None:
        self.push_screen(SetTargets.SetTargets())

    def action_show_statistic(self) -> None:
        #self.push_screen(StatisticScreen.StatisticScreen())
        pass

def create_empty_file_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            pass 
        print(f"Создан файл: {file_path}")

if __name__ == "__main__":
    create_empty_file_if_not_exists('data/food.json')
    create_empty_file_if_not_exists('data/meals.json')
    create_empty_file_if_not_exists('data/targets.json')  
    app = FoodTracker()
    app.run()