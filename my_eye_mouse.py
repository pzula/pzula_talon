from talon import Module
from user.knausj_talon.code import mouse
from talon_plugins import eye_mouse, eye_zoom_mouse

mod = Module()

@mod.action_class
class Actions:
    def do_pop():
        """"""
        mouse.on_pop(False)
        if eye_zoom_mouse.zoom_mouse.enabled:
            eye_zoom_mouse.zoom_mouse.on_pop(False)