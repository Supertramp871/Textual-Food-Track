from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, ListView, ListItem
from textual import events
import modules.MainDisplay as MainDisplay
import json

class AddMealScreen(ModalScreen):
    
    def __init__(self):
        super().__init__()
        self.foods_data = self.load_foods()
        self.filtered_foods = self.foods_data.copy()
        self.selected_food = None
    
    def load_foods(self):
        try:
            with open("data/food.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
              
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Find your meal in foods", classes="title"),
            Input(placeholder="Search food...", id="food-search"),
            Label("Search results:", classes="subtitle"),
            ListView(
                *[ListItem(Label(f"{food['food']} - {food['Caloric Value']}kcal")) 
                for food in self.filtered_foods[:]],
                id="food-results",
                classes="search-results"
            ),
            Horizontal(
                Vertical(
                    Label("Selected food:", classes="subtitle"),
                    Label("No food selected", id="selected-food-name"),
                    Label("Kcal: 0", id="selected-food-kcal"),
                    Label("Protein: 0g", id="selected-food-protein"),
                    Label("Fat: 0g", id="selected-food-fat"),
                    Label("Carbs: 0g", id="selected-food-carbs"),
                ),
                Vertical(
                    Label("Calculated values:", classes="subtitle"),
                    Label("", id="calculated-values"),
                ),
                Vertical(
                    Label("Serving size:", classes="subtitle"),
                    Input(placeholder="Grams", id="meal-grams", value="100"),
                    Horizontal(
                        Button("Add meal", id="add-meal-btn", variant="primary"),
                        Button("Cancel", id="cancel-meal-btn"),
                    ),
                ),
            ),
            id="add-meal-container"
        )
    
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "food-search":
            search_term = event.input.value.lower().strip()
            if not search_term:
                self.filtered_foods = self.foods_data.copy()
            else:
                self.filtered_foods = [
                    food for food in self.foods_data 
                    if search_term in food['food'].lower()
                ]
            
            results_list = self.query_one("#food-results")
            results_list.clear()
            for food in self.filtered_foods[:3]:
                results_list.append(
                    ListItem(Label(f"{food['food']} - {food['Caloric Value']}kcal"))
                )
        
        elif event.input.id == "meal-grams":
            self.update_calculated_values()
    
    def update_calculated_values(self):
        if not self.selected_food:
            return
        
        try:
            grams = int(self.query_one("#meal-grams").value.strip() or "100")
            ratio = grams / 100
            
            calculated_text = (
                f"Per {grams}g:\n"
                f"Kcal: {int(self.selected_food['Caloric Value'] * ratio)}\n"
                f"Protein: {int(self.selected_food['Protein'] * ratio)}g\n"
                f"Fat: {int(self.selected_food['Fat'] * ratio)}g\n"
                f"Carbs: {int(self.selected_food['Carbohydrates'] * ratio)}g"
            )
            
            self.query_one("#calculated-values").update(calculated_text)
        except ValueError:
            self.query_one("#calculated-values").update("Enter valid grams")
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if not self.filtered_foods:
            return
        
        selected_index = event.list_view.index
        if selected_index < len(self.filtered_foods):
            self.selected_food = self.filtered_foods[selected_index]  
            
            self.query_one("#selected-food-name").update(self.selected_food['food'])  
            self.query_one("#selected-food-kcal").update(f"Kcal: {self.selected_food['Caloric Value']}")  
            self.query_one("#selected-food-protein").update(f"Protein: {self.selected_food['Protein']}g")  
            self.query_one("#selected-food-fat").update(f"Fat: {self.selected_food['Fat']}g")  
            self.query_one("#selected-food-carbs").update(f"Carbs: {self.selected_food['Carbohydrates']}g")  
            
            self.update_calculated_values()
            
            self.query_one("#meal-grams").focus()
    
    def on_list_view_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.query_one("#meal-grams").focus()
            event.stop()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "food-search":
            if self.filtered_foods:
                self.query_one("#food-results").focus()
        elif event.input.id == "meal-grams":
            self.query_one("#add-meal-btn").focus()
    
    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-meal-btn":
            self.add_meal()
        else:
            self.dismiss()
    
    def add_meal(self) -> None:
        try:
            if not self.selected_food:
                self.notify("Please select a food first", severity="error")
                return
            
            grams_input = self.query_one("#meal-grams", Input).value.strip()
            if not grams_input:
                self.notify("Please enter grams", severity="error")
                return
            
            try:
                grams = int(grams_input)
                if grams <= 0:
                    self.notify("Grams must be positive", severity="error")
                    return
            except ValueError:
                self.notify("Please enter valid grams", severity="error")
                return

            ratio = grams / 100
            meal_data = {
                "food": self.selected_food['food'],
                "Caloric Value": int(self.selected_food['Caloric Value'] * ratio),
                "Protein": int(self.selected_food['Protein'] * ratio),
                "Fat": int(self.selected_food['Fat'] * ratio),
                "Carbohydrates": int(self.selected_food['Carbohydrates'] * ratio),
                "Grams": grams,
                "Datetime": datetime.now().strftime("%H:%M-%d.%m.%Y")
            }
            
            try:
                with open("data/meals.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            
            data.append(meal_data)
            
            with open("data/meals.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.notify("Meal added successfully!", severity="information")
            self.dismiss()
            
        
        except Exception as e:
            self.notify(f"Error adding meal: {str(e)}", severity="error")
        