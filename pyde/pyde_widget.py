class PydeWidget(object):
    
    def keyPressEvent(self, event):
        if not self.app.key_press_fire_action(event, self):
            super().keyPressEvent(event)
    
    