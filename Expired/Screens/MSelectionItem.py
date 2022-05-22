from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import MDList
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import (
    Ellipse,
    RoundedRectangle,
    SmoothLine,
)
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.animation import Animation
from kivy.clock import Clock


class MSelectionItem(ThemableBehavior, MDRelativeLayout, TouchBehavior):
    selected = BooleanProperty(False)
    owner = ObjectProperty()
    instance_item = ObjectProperty()
    instance_icon = ObjectProperty()
    overlay_color = ColorProperty([0, 0, 0, 0.2])
    progress_round_size = NumericProperty(dp(46))
    progress_round_color = ColorProperty(None)

    _progress_round = NumericProperty(0)
    _progress_line_end = NumericProperty(0)
    _progress_animation = BooleanProperty(False)
    _touch_long = BooleanProperty(False)
    _instance_progress_inner_circle_color = ObjectProperty()
    _instance_progress_inner_circle_ellipse = ObjectProperty()
    _instance_progress_inner_outer_color = ObjectProperty()
    _instance_progress_inner_outer_line = ObjectProperty()
    _instance_overlay_color = ObjectProperty()
    _instance_overlay_rounded_rec = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.set_progress_round)

    def set_progress_round(self, interval):
        with self.canvas.after:
            self._instance_progress_inner_circle_color = Color(
                rgba=(0, 0, 0, 0)
            )
            self._instance_progress_inner_circle_ellipse = Ellipse(
                size=self.get_progress_round_size(),
                pos=self.get_progress_round_pos(),
            )
            self.bind(
                pos=self.update_progress_inner_circle_ellipse,
                size=self.update_progress_inner_circle_ellipse,
            )
            # FIXME: Radius value is not displayed.
            self._instance_overlay_color = Color(rgba=(0, 0, 0, 0))
            """ THIS IS WHERE THE OVERLAY SIZE IS GIVEN?"""
            self._instance_overlay_rounded_rec = RoundedRectangle(
                size=self.size, # LOOK HERE
                # size=[self.size_hint_x,self.size_hint_y], # LOOK HERE
                # size=[10,40],
                pos=self.pos,
                radius=self.instance_item.radius
                if hasattr(self.instance_item, "radius")
                else [
                    0,
                ],
            )
            self.bind(
                pos=self.update_overlay_rounded_rec,
                size=self.update_overlay_rounded_rec,
            )
            self._instance_progress_inner_outer_color = Color(rgba=(0, 0, 0, 0))
            self._instance_progress_inner_outer_line = SmoothLine(
                width=dp(4),
                circle=[
                    self.center_x,
                    self.center_y,
                    self.progress_round_size * 0.58,
                    0,
                    0,
                ],
            )

    def do_selected_item(self, *args):
        Animation(scale=1, d=0.2).start(self.instance_icon)
        self.selected = True
        self._progress_animation = False
        self._instance_overlay_color.rgba = self.get_overlay_color()
        self.owner.dispatch("on_selected", self)

    def do_unselected_item(self):
        Animation(scale=0, d=0.2).start(self.instance_icon)
        self.selected = False
        self._instance_overlay_color.rgba = self.get_overlay_color()
        self.owner.dispatch("on_unselected", self)

    def do_animation_progress_line(self, animation, instance, value):
        self._instance_progress_inner_outer_line.circle = (
            self.center_x,
            self.center_y,
            self.progress_round_size * 0.58,
            0,
            360 * value,
        )

    def update_overlay_rounded_rec(self, *args):
        self._instance_overlay_rounded_rec.size = self.size
        self._instance_overlay_rounded_rec.pos = self.pos

    def update_progress_inner_circle_ellipse(self, *args):
        self._instance_progress_inner_circle_ellipse.size = (
            self.get_progress_round_size()
        )
        self._instance_progress_inner_circle_ellipse.pos = (
            self.get_progress_round_pos()
        )

    def reset_progress_animation(self):
        Animation.cancel_all(self)
        self._progress_animation = False
        self._instance_progress_inner_circle_color.rgba = (0, 0, 0, 0)
        self._instance_progress_inner_outer_color.rgba = (0, 0, 0, 0)
        self._instance_progress_inner_outer_line.circle = [
            self.center_x,
            self.center_y,
            self.progress_round_size * 0.58,
            0,
            0,
        ]
        self._progress_line_end = 0

    def get_overlay_color(self):
        return self.overlay_color if self.selected else (0, 0, 0, 0)

    def get_progress_round_pos(self):
        return (
            self.center_x - self.progress_round_size / 2,
            self.center_y - self.progress_round_size / 2,
        )

    def get_progress_round_size(self):
        return self.progress_round_size, self.progress_round_size

    def get_progress_round_color(self):
        return (
            self.theme_cls.primary_color
            if not self.progress_round_color
            else self.progress_round_color
        )

    def get_progress_line_color(self):
        return (
            self.theme_cls.primary_color[:-1] + [0.5]
            if not self.progress_round_color
            else self.progress_round_color[:-1] + [0.5]
        )

    def on_long_touch(self, *args):
        if not self.owner.get_selected():
            self._touch_long = True
            self._progress_animation = True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self._touch_long:
                self._touch_long = False
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.selected:
                self.do_unselected_item()
            else:
                if self.owner.selected_mode:
                    self.do_selected_item()
        return super().on_touch_down(touch)

    def on__touch_long(self, instance, value):
        if not value:
            self.reset_progress_animation()

    # CHANGED d=-3 from d=1!!!
    def on__progress_animation(self, instance, value):
        if value:
            # anim = Animation(_progress_line_end=360, d=.3, t="in_out_quad")
            anim = Animation(_progress_line_end=360, d=.3, t="in_out_quad")
            anim.bind(
                on_progress=self.do_animation_progress_line,
                on_complete=self.do_selected_item,
            )
            anim.start(self)
            self._instance_progress_inner_outer_color.rgba = (
                self.get_progress_line_color()
            )
            self._instance_progress_inner_circle_color.rgba = (
                self.get_progress_round_color()
            )
        else:
            self.reset_progress_animation()


class MSelectionList(MDList):
    """
    :Events:
        `on_selected`
            Called when a list item is selected.
        `on_unselected`
            Called when a list item is unselected.
    """

    selected_mode = BooleanProperty(False)
    icon = StringProperty("check")

    # CUSTOM
    icon_size = NumericProperty()

    icon_pos = ListProperty()

    icon_bg_color = ColorProperty([1, 1, 1, 1])

    icon_check_color = ColorProperty([0, 0, 0, 1])

    overlay_color = ColorProperty([0, 0, 0, 0.2])

    # CHANGED DPI FROM 46 to 30
    progress_round_size = NumericProperty(dp(30))

    progress_round_color = ColorProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_selected")
        self.register_event_type("on_unselected")

    def add_widget(self, widget, index=0, canvas=None):
        selection_icon = SelectionIconCheck(
            # user_font_size = self.icon_size,
            icon=self.icon,
            md_bg_color=self.icon_bg_color,
            icon_check_color=self.icon_check_color,
        )
        """ CUSTOMIZED. otherwise "readding" widgets would be locked to prev parent (although the same??? idk)"""
        widget.parent = None
        # CUSTOM
        # selection_icon.width = self.icon_size
        # selection_icon.height = self.icon_size
        # user_font_size = "5sp"
        # selection_icon.user_font_size = self.icon_size

        container = MSelectionItem(
            size_hint=(1, None),
            # size_hint=(1, 1),
            height=widget.height,
            instance_item=widget,
            instance_icon=selection_icon,
            overlay_color=self.overlay_color,
            progress_round_size=self.progress_round_size,
            progress_round_color=self.progress_round_color,
            owner=self, 
        )
        container.add_widget(widget)
        if not self.icon_pos:
            pos = (
                dp(12), # CHANGED FROM 12
                container.height / 2 - selection_icon.height / 2,
                # container.height / 2 - selection_icon.user_font_size / 2,
            )
        else:
            pos = self.icon_pos
        selection_icon.pos = pos
        # container.add_widget(selection_icon)
        return super().add_widget(container, index, canvas)

    def get_selected(self):
        selected = False
        for item in self.children:
            if item.selected:
                selected = True
                break
        return selected

    def get_selected_list_items(self):
        selected_list_items = []
        for item in self.children:
            if item.selected:
                selected_list_items.append(item)
        return selected_list_items

    def unselected_all(self):
        for item in self.children:
            item.do_unselected_item()
        self.selected_mode = False

    def selected_all(self):
        for item in self.children:
            item.do_selected_item()
        self.selected_mode = True

    def on_selected(self, *args):
        """Called when a list item is selected."""

        if not self.selected_mode:
            self.selected_mode = True

    def on_unselected(self, *args):
        """Called when a list item is unselected."""

        self.selected_mode = self.get_selected()

class SelectionIconCheck(MDIconButton):

    user_font_size = dp(10)
    scale = NumericProperty(0)
    icon_check_color = ColorProperty([0, 0, 0, 1])
    # height = dp(40)

    # width = dp(40)
    # height = "40dp"
    # width = "40dp"


    # CUSTOM
    def set_size(self, interval):
        pass

        """
        Sets the custom icon size if the value of the `user_font_size`
        attribute is not zero. Otherwise, the icon size is set to `(48, 48)`.
        """
        # self.width = self.user_font_size
        # self.height = self.user_font_size
        """
        """

        self.width = (
            "48dp" if not self.user_font_size else dp(self.user_font_size + 23)
            
        )
        self.height = (
            "48dp" if not self.user_font_size else dp(self.user_font_size + 23)
        )

