from talon import Module, ui

mod = Module()

@mod.action_class
class Actions:
    def unminimize():
        ""
        for x in ui.active_window().app.windows():
            if x.hidden:
                #x.hidden = False  #???
                x.focus()
                return # comment this to focus all hidden windows
