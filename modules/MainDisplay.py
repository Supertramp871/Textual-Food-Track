from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.containers import Container
from datetime import datetime
import json
import os

class MainDisplay(Static):
    """Основной виджет для отображения прогресса и истории"""
    
    def __init__(self):
        super().__init__()
        self.daily_progress = self.calculate_daily_progress()
        self.history_meals = self.load_today_meals()
    
    def load_targets(self) -> dict:
        """Загрузка целевых значений из targets.json"""
        default_targets = {
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0
        }
        
        try:
            if os.path.exists('data/targets.json'):
                with open('data/targets.json', 'r') as f:
                    return json.load(f)
            else:
                # Создаем файл с значениями по умолчанию, если его нет
                with open('data/targets.json', 'w') as f:
                    json.dump(default_targets, f, indent=4)
                return default_targets
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading targets: {e}")
            return default_targets
    
    def load_today_meals(self) -> list:
        """Загрузка приемов пищи за сегодня из meals.json"""
        try:
            with open('data/meals.json', 'r') as f:
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
        targets = self.load_targets()
        
        # Суммируем питательные вещества за день
        total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
        
        for meal in today_meals:
            # Парсим значения из строки "kcal/protein/fat/carbs"
            values = meal["values"].split('/')
            if len(values) == 4:
                try:
                    total["calories"] += int(values[0])
                    total["protein"] += int(values[1]) 
                    total["fat"] += int(values[2]) 
                    total["carbs"] += int(values[3])
                except ValueError:
                    continue
        
        # Рассчитываем проценты и статусы
        progress = {}
        for nutrient in ["calories", "protein", "fat", "carbs"]:
            current = total[nutrient]
            target = targets.get(nutrient, 0)
            percent = round((current / target) * 100) if target > 0 else 0
            
            # Определяем статус
            status = "normal"
            if current < target: 
                status = "missed"
            elif current > target:
                status = "over"
            
            progress[nutrient] = {
                'current': round(current),
                'target': target,
                'percent': percent,
                'status': status,
                'value': round(current)
            }
        
        return progress
    
    def compose(self) -> ComposeResult:
        yield Container(
            self.render_daily_progress(),
            self.render_history(),
            id="main-container"
        )
    
    def render_daily_progress(self) -> Static:
        """Рендеринг дневного прогреgress"""
        progress = self.daily_progress
        
        content = f"[bold]DAILY PROGRESS[/]\n"
        calories_text = f"[bold]{progress['calories']['current']}[/bold]/[dim]{progress['calories']['target']}[/dim]"
        calories_percent = progress['calories']['percent']
        calories_bar = self._create_progress_bar(calories_percent, 20)
        
        content += f"[bold]CALORIES:[/] {calories_text} kcal\n"
        content += f"{calories_bar} [bold]{calories_percent}%[/]\n\n"
        content += f"{'PROTS':^30}{'FATS':^30}{'CARBS':^30}\n"
        content += f"{str(progress['protein']['current']) + '/' + str(progress['protein']['target']):^30}" \
                f"{str(progress['fat']['current']) + '/' + str(progress['fat']['target']):^30}" \
                f"{str(progress['carbs']['current']) + '/' + str(progress['carbs']['target']):^30}\n"
        content += f"{'(' + str(progress['protein']['percent']) + '%' + ')':^30}" \
                f"{'(' +  str(progress['fat']['percent']) + '%' + ')':^30}" \
                f"{'(' + str(progress['carbs']['percent']) + '%' + ')':^30}\n"
        content += f"{progress['protein']['status'] + ' ' + str(abs(progress['protein']['current'] - progress['protein']['target'])):^30}" \
                f"{progress['fat']['status'] + ' ' + str(abs(progress['fat']['current'] - progress['fat']['target'])):^30}" \
                f"{progress['carbs']['status'] + ' ' + str(abs(progress['carbs']['current'] - progress['carbs']['target'])):^30}"

        return Static(content, id="daily-progress")
    
    def _create_progress_bar(self, percent: int, width: int = 20) -> str:
        """Создает текстовый прогресс-бар"""
        filled = int(percent * width / 100)
        bar = "█" * filled + "░" * (width - filled)
        
        if percent < 50:
            color = "red"
        elif percent < 80:
            color = "yellow"
        else:
            color = "green"
        
        return f"[{color}]{bar}[/]"

    def render_history(self) -> Static:
        """Рендеринг истории питания в три равных столбца"""
        if not self.history_meals:
            return Static("No history meals", id="history-meals")
        
        content = "HISTORY MEALS\n\n"
        
        # Рассчитываем количество строк (каждая строка содержит 3 приема пищи)
        rows = (len(self.history_meals) + 2) // 3  # Округление вверх
        
        for row in range(rows):
            line_parts = []
            
            # Собираем данные для трех столбцов текущей строки
            for col in range(3):
                index = row + col * rows
                if index < len(self.history_meals):
                    food = self.history_meals[index]
                    meal_str = f"{food['name']} {food['values']} ({food['grams']})"
                    line_parts.append(meal_str)
                else:
                    line_parts.append("")
            
            # Форматируем строку с тремя столбцами
            content += f"{line_parts[0]:<35} {line_parts[1]:<35} {line_parts[2]:<35}\n"
        
        return Static(content, id="history-meals")

    def refresh_display(self) -> None:
        self.daily_progress = self.calculate_daily_progress()
        self.history_meals = self.load_today_meals()
        self.query_one("#daily-progress").update(self.render_daily_progress().renderable) # type: ignore
        self.query_one("#history-meals").update(self.render_history().renderable) # type: ignore

    def on_mount(self) -> None:
        self.refresh_display()
        self.set_interval(1.0, self.refresh_display)