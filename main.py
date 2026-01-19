from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label
from textual.containers import Grid, Vertical, Center
from textual.screen import Screen
import datetime

class DayScreen(Screen):
    """Screen for a day of the advent calendar!"""
    
    CSS = """
    DayScreen {
        align: center middle;
        background: $boost;
    }
    
    #dialog {
        width: 50;
        height: auto;
        border: thick #9a4dbd;
        background: #431f53;
        padding: 2;
        align: center middle;
    }
    
    #dialog Label {
        width: 100%;
        text-align: center;
        margin-bottom: 1;
    }
    
    #dialog Button {
        width: auto;
        color: $text;
        background: #aa4343;
    }
    """

    gifts = {
        1: "React Workshop!",
        2: "A Fusering Workshop!",
        3: "Keyring with Onshape!",
        4: "Hono Backend!",
        5: "Full Stack App with Flask!",
        6: "3D Printable Ruler!",
        7: "Interactive Christmas Tree!",
        8: "Automating Cookie Clicker!",
        9: "TUI in Textual!",
        10: "No leeks :3",
        11: "No leeks :p",
        12: "Still no leeks :3c"
    }
    
    def __init__(self, day: int) -> None:
        self.day = day
        super().__init__()
    
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Here's what's in day {str(self.day)}: {self.gifts.get(self.day)}")
            with Center():
                yield Button("Close", id="close")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
        event.stop()

class AdventCalendarApp(App):
    """A Textual app for an advent calendar."""
    
    CSS = """
    Grid {
        grid-size: 6 2;
        grid-gutter: 1 4;
    }
    
    Grid Button {
        width: 100%;
        height: 100%;
        margin-bottom: 1;
        margin-top: 1;
        margin-left: 1;
        margin-right: 1;
        color: #f4e9dd;
        background: #a968c8;
    }
    
    Grid Button:hover {
        background: #59296f;
    }
    
    Grid Button.opened {
        background: #aa4343;
    }
    """
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("r", "reset_days", "Reset opened days")]
    START_DATE = datetime.date(2025, 12, 13)
    DAYS = 12

    def __init__(self) -> None:
        super().__init__()
        self.open_days: set[int] = set()
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label(self._counter_text(), id="counter")
        with Grid():
            for day in range(1, self.DAYS + 1):
                yield Button(str(day), id=f"day-{day}")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button = event.button
        day = str(button.label)
        unlock_day = self.START_DATE + datetime.timedelta(days=int(day) - 1)
        if datetime.date.today() < unlock_day:
            self.notify(f"You will be able to unlock day {day} on {unlock_day}")
            return None
        if not button.has_class("opened"):
            button.add_class("opened")
            self.open_days.add(int(day))
            self._update_counter()
        self.push_screen(DayScreen(int(day)))
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
        
    def action_reset_days(self) -> None:
        """Clear all opened days and reset the counter."""
        for button in self.query("Grid Button"):
            button.remove_class("opened")
        self.open_days.clear()
        self._update_counter()

    def _counter_text(self) -> str:
        return f"Days opened: {len(self.open_days)}/{self.DAYS}"

    def _update_counter(self) -> None:
        counter = self.query_one("#counter", Label)
        counter.update(self._counter_text())

def main():
    app = AdventCalendarApp()
    app.run()

if __name__ == "__main__":
    main()
