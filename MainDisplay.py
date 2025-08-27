from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container
from datetime import datetime

import json
import DefaultTargets

class MainDisplay(Static):
    """Основной виджет для отображения прогресса и истории"""
    
    def __init__(self):
        super().__init__()
        self.daily_progress = self.calculate_daily_progress()
        self.history_meals = self.load_today_meals()
    
    def load_today_meals(self) -> list:
        """Загрузка приемов пищи за сегодня из meals.json"""
        try:
            with open('meals.json', 'r') as f:
                meals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        today = datetime.now().strftime("%d.%m.%Y")
        today_meals = []
        
        for meal in meals:
            if today in meal.get("Datetime", ""):
                # Форматируем данные для отображения
                kcal = meal.get("Caloric Value", 0)
                protein = meal.get("Protein", 0)
                fat = meal.get("Fat", 0)
                carbs = meal.get("Carbohydrates", 0)
                grams = meal.get("Grams", 0)
                
                today_meals.append({
                    "name": meal.get("food", "Unknown"),
                    "values": f"{kcal}/{protein}/{fat}/{carbs}",
                    "grams": f"{grams}g"
                })
        
        return today_meals
    
    def calculate_daily_progress(self) -> dict:
        """Вычисление прогресса за сегодня"""
        today_meals = self.load_today_meals()
        
        # Суммируем питательные вещества за день
        total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
        
        for meal in today_meals:
            # Парсим значения из строки "kcal/protein/fat/carbs"
            values = meal["values"].split('/')
            if len(values) == 4:
                total["kcal"] += int(values[0])
                total["protein"] += int(values[1]) 
                total["fat"] += int(values[2]) 
                total["carbs"] += int(values[3]) 
        
        # Рассчитываем проценты и статусы
        progress = {}
        for nutrient in ["kcal", "protein", "fat", "carbs"]:
            current = total[nutrient]
            target = DefaultTargets.DEFAULT_TARGETS[nutrient]
            percent = round((current / target) * 100) if target > 0 else 0
            
            # Определяем статус
            if current < target: 
                status = "missed"
            elif current > target:
                status = "over"
            
            progress[nutrient] = {
                'current': round(current),
                'target': target,
                'percent': percent,
                'status': status,
                'value': round(current)  # Текущее значение питательного вещества
            }
        
        return progress
    
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
        content += f"    Prot {progress['protein']['current']}/{progress['protein']['target']} ({progress['protein']['percent']}%) {progress['protein']['status']} {abs(progress['protein']['value']-progress['protein']['target'])} prots\n"
        content += f"    Fat {progress['fat']['current']}/{progress['fat']['target']} ({progress['fat']['percent']}%) {progress['fat']['status']} {abs(progress['fat']['value']-progress['fat']['target'])} fats\n"
        content += f"    Carbs {progress['carbs']['current']}/{progress['carbs']['target']} ({progress['carbs']['percent']}%) {progress['carbs']['status']} {abs(progress['carbs']['value']-progress['carbs']['target'])} carbs"
        return Static(content, id="daily-progress")
    
    def render_history(self) -> Static:
        """Рендеринг истории питания"""
        content = "History meals\n"
        for food in self.history_meals:
            content += f"    {food['name']} {food['values']} ({food['grams']})\n"
        return Static(content, id="history-meals")
    
    def refresh_data(self) -> None:
        """Обновление данных при добавлении/удалении приемов пищи"""
        self.daily_progress = self.calculate_daily_progress()
        self.history_meals = self.load_today_meals()
        self.update()