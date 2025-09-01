from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.screen import ModalScreen
from datetime import datetime

import modules.AddFoodScreen as AddFoodScreen
import modules.AddMealScreen as AddMealScreen
import modules.MainDisplay as MainDisplay
import modules.RemoveFoodScreen as RemoveFoodScreen
import modules.RemoveMealScreen as RemoveMealScreen
import modules.SetTargets as SetTargets
import modules.StatisticScreen as StatisticScreen

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

class FoodTracker(App):
    """A Textual track food."""

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
        """Create child widgets for the app."""
        yield Header()
        yield MainDisplay.MainDisplay()
        yield Footer()

    def action_add_meal(self) -> None:
        """Действие для добавления приема пищи."""
        self.push_screen(AddMealScreen.AddMealScreen())

    def action_add_food(self) -> None:
        """Действие для добавления продукта."""
        self.push_screen(AddFoodScreen.AddFoodScreen())
    
    def action_remove_meal(self) -> None:
        """Действие для удаления приема пищи."""
        self.push_screen(RemoveMealScreen.RemoveScreenMeal())
    
    def action_remove_food(self) -> None:
        """Действие для удаления продукта."""
        self.push_screen(RemoveFoodScreen.RemoveScreenFood())
    
    def action_set_targets(self) -> None:
        """Действие для установки целей."""
        self.push_screen(SetTargets.SetTargets())

    def action_show_statistic(self) -> None:
        """Действие для показа статистики."""
        #self.push_screen(StatisticScreen.StatisticScreen())
    

if __name__ == "__main__":
    app = FoodTracker()
    app.run()