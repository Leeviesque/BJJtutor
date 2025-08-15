"""
Application for learning jiujitsu
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import datetime


class BJJtutor(toga.App):
    
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        
        self.main_page = self.make_main_page()
        self.diary_page = self.make_diary_page()
        self.learning_page = self.make_learning_page()
        self.newnotes_page = self.make_newnotes_page()

        # bottom bar for navigating the pages
        bar = toga.Box(style = Pack(direction=ROW))
        for name, label in [("profile", "Profile"), ("diary", "Diary"), ("learning", "Learning")]:
              bar.add(toga.Button(label,
                                on_press = lambda w, n=name: self.show_page(n),
                                style = Pack(padding = 6, flex = 1))) 

        # root - where the content (pages etc.) of the app is displayed and the content area
        self.content_area = toga.Box(style=Pack(flex=1)) 
        root = toga.Box(style=Pack(direction=COLUMN, flex=1))
        root.add(self.content_area)
        root.add(bar)

        # container for the notes
        self.entries = []

        self.main_window = toga.MainWindow(title='Profile')
        self.main_window.content = root
        self.main_window.show()

        self.show_page('learning')

    # helper functions for creating the pages
    def make_main_page(self):
            return toga.Box(style=Pack(direction=COLUMN, padding=12), 
                            children = [toga.Label('Profile & Stats')])
    
        # method for btn to make a new diary entry
    def make_newnotes_page (self, init_topic=None, init_notes=None, init_date=None):
        topic = (init_topic or "")
        notes = (init_notes or "")
        date = (init_date or "")
        
        # if this is a fresh entry, set todays date, otherwise use the given parameter
        if not init_topic and not init_notes:
            date = datetime.date.today().strftime("%d.%m.%Y")

        # the content itself
        back_btn = toga.Button(style=Pack(flex=0, margin=8),
                               text="Back",  
                                on_press = lambda w: self.show_page("diary"))
        
        self.topic = toga.TextInput(style=Pack(flex=1, font_weight="bold", font_size=14, margin=8), 
                                placeholder="What was the topic of todays trainings?",
                                value=topic)
        self.date_field = toga.TextInput(style=Pack(flex=0, margin=8), 
                                    value=date)                        
        self.new_notes = toga.MultilineTextInput(style = Pack(flex=5, margin=8), 
                                    placeholder = "What did you learn on the mats today?",
                                    value=notes)
        
        save_btn = toga.Button(style=Pack(flex=0, margin=8), 
                               text="Save",
                               on_press = lambda w: self.add_notes())

        content_area = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=12),
                                children=[back_btn, self.topic, self.date_field, self.new_notes, save_btn])
        return content_area

    #  method for saving notes
    def add_notes(self):
        saved_topic = self.topic.value
        saved_date = self.date_field.value
        saved_notes = self.new_notes.value

        if self.no_notes:
            self.old_notes_box.clear()
            self.no_notes = False

        # Saves notes and date as text that user cant edit, unless the user presses the topic -> summons new_notes_page with saved vals21mm
        new_entry_topic = toga.Button(text=saved_topic, 
                                         style=Pack(flex=1, margin=4, font_weight="bold"),
                                         on_press = lambda w: self.show_page("new notes", saved_topic, saved_notes, saved_date))
        new_entry_date = toga.TextInput(value=saved_date, 
                                        readonly=True,
                                        style=Pack(flex=0, margin=4))
        new_entry_notes = toga.MultilineTextInput(value=saved_notes,
                                                  readonly=True, 
                                                  style=Pack(flex=5, margin=4))

        new_entry = toga.Box(style=Pack(direction=COLUMN, padding=4, flex=1),
                                        children=[new_entry_topic, new_entry_date, new_entry_notes])

        self.old_notes_box.add(new_entry)
        self.show_page("diary")

    def make_diary_page(self):
        
        self.no_notes = True

        # main pages content
        btn_for_newnotes_box = toga.Box(style=Pack(
                                        align_items="end",
                                        justify_content="end"
                                        ),
                                children=[toga.Button(text="New notes", 
                                        on_press= lambda w: self.show_page("new notes")
                                        )]) 
        label = toga.Label('Notes and Discoveries',
                           style=Pack(font_size=14, font_weight='bold'))     

            # container for all the previous training notes
        self.old_notes_box = toga.Box(id = "empty", style=Pack(direction=COLUMN, padding=8),
                             children = [toga.Label("No training notes added yet!")])  
        
        scroller = toga.ScrollContainer(
            content=self.old_notes_box,
            style=Pack(flex=1))
        
        return toga.Box(style=Pack(direction=COLUMN, padding=12, flex=1), 
                        children=[label, scroller, btn_for_newnotes_box])
                 

        

    def make_learning_page(self): 
            return toga.Box(style=Pack(direction=COLUMN, padding=12), 
                            children=[toga.Label('Learning & Associations')])
    
    # switching the page
    def show_page(self, name, *init_vals):
          routes = {
                "profile":   lambda: self.main_page, 
                "diary":     lambda: self.diary_page,
                "learning":  lambda: self.learning_page,
                "new notes": lambda: self.make_newnotes_page(*init_vals)
          }
          page = routes[name]()
          self.content_area.clear()
          self.content_area.add(page)
   

def main():
    return BJJtutor()
