from pprint import pprint
import unittest


class Widget:
    def __init__(self, name: str, size=(50, 50)) -> None:
        self.name = name
        self.size = size

    def resize(self, newSize: tuple[int, int]) -> None:
        self.size = newSize

    def dispose(self) -> None:
        del self


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()

    def test_default_widget_size(self):
        self.assertEqual(self.widget.size, (50, 50), 'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize((100, 100))
        self.assertEqual(self.widget.size, (100, 100),
                         'incorrect size after resize')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    pprint(suite())
    runner.run(suite())
