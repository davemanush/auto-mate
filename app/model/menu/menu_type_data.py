import uuid


class MenuTypeData:
    def __init__(self, menu_id: uuid, text: str, order: int, send_render_event: bool, style_override=None):
        self.menu_id = menu_id
        self.text = text
        self.order = order
        self.send_render_render = send_render_event
        self.style_override = style_override

    def rerender(self):
        return self.send_render_render