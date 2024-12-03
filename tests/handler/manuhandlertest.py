import unittest

from app.service.cursorhandler import get_menu_options_by_view_type, MenuOptions, render_menu_bar
from app.model.viewtype import ViewType


class MenuHandlerTest(unittest.TestCase):

    def test_MainMenuBar(self):
        expected = [
            MenuOptions.RUN,
            MenuOptions.DETAILS,
            MenuOptions.SCRIPT_CREATE_NEW,
            MenuOptions.SETTINGS_DETAILS,
            MenuOptions.QUIT_WINDOW]
        self.assertEqual(get_menu_options_by_view_type(ViewType.MAIN), expected)

    def test_ViewScriptBar(self):
        expected = [
            MenuOptions.EDIT,
            MenuOptions.BACK]
        self.assertEqual(get_menu_options_by_view_type(ViewType.SCRIPT_VIEW), expected)

    def test_ViewStepBar(self):
        expected = [
            MenuOptions.EDIT,
            MenuOptions.DRY_RUN,
            MenuOptions.BACK]
        self.assertEqual(get_menu_options_by_view_type(ViewType.STEP_VIEW), expected)

    def test_EditScriptBar(self):
        expected = [
            MenuOptions.SAVE,
            MenuOptions.ADD,
            MenuOptions.DETAILS,
            MenuOptions.EDIT,
            MenuOptions.DELETE,
            MenuOptions.QUIT_WITHOUT_SAVING]
        self.assertEqual(get_menu_options_by_view_type(ViewType.SCRIPT_EDIT), expected)

    def test_EditStepBar(self):
        expected = [
            MenuOptions.SAVE,
            MenuOptions.EDIT,
            MenuOptions.DELETE,
            MenuOptions.QUIT_WITHOUT_SAVING]
        self.assertEqual(get_menu_options_by_view_type(ViewType.STEP_EDIT), expected)

    def test_edit_step_render_menu_bar(self):
        expected = 'Save | [30m[47mEdit[0m | Delete | Quit without saving'
        self.assertEqual(render_menu_bar(ViewType.STEP_EDIT, 19), expected)

if __name__ == '__main__':
    unittest.main()