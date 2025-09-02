from textual.app import ComposeResult
from textual.widgets import Button, Input, Label
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual import events
import json
import os

class SetTargets(ModalScreen):
    def compose(self) -> ComposeResult:
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
        try:
            with open("data/targets.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"calories": "", "protein": "", "fat": "", "carbs": ""}

    def on_input_changed(self, event: Input.Changed) -> None:
        numeric_fields = {"target-kcal", "target-protein", "target-fat", "target-carbs"}
        
        if event.input.id in numeric_fields:
            cleaned_value = ''.join(filter(str.isdigit, event.input.value))

            if cleaned_value.startswith('0') and len(cleaned_value) > 1:
                cleaned_value = cleaned_value.lstrip('0')
                if not cleaned_value:
                    cleaned_value = '0'

            if cleaned_value != event.input.value:
                event.input.value = cleaned_value
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.value.strip():
            self.focus_next_widget(event.input)
    
    def focus_next_widget(self, current_input: Input) -> None:
        inputs = list(self.query(Input))
        buttons = list(self.query(Button))
        all_widgets = inputs + buttons
        
        current_index = None

        for i, widget in enumerate(all_widgets):
            if widget == current_input:
                current_index = i
                break

        if current_index is not None and current_index < len(all_widgets) - 1:
            next_widget = all_widgets[current_index + 1]
            next_widget.focus()

    def on_key(self, event: events.Key) -> None:
        """Обработка нажатия клавиш"""
        if event.key == "escape":
            self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-targets-btn":
            self.save_targets()
        else:
            self.dismiss()
    
    def save_targets(self) -> None:
        try:
            kcal = self.query_one("#target-kcal", Input).value.strip()
            protein = self.query_one("#target-protein", Input).value.strip()
            fat = self.query_one("#target-fat", Input).value.strip()
            carbs = self.query_one("#target-carbs", Input).value.strip()
            
            if not all([kcal, protein, fat, carbs]):
                self.notify("Please fill all fields", severity="error")
                return

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

            with open("data/targets.json", "w", encoding="utf-8") as f:
                json.dump(targets_data, f, indent=4, ensure_ascii=False)
            
            self.notify("Targets saved successfully!", severity="information")
            self.dismiss()
            
        except Exception as e:
            self.notify(f"Error saving targets: {str(e)}", severity="error")