from builtins import object
from pathlib import Path

from psychopy import visual, event
from psychopy.visual import Window
from psychopy.visual import TextBox2
from psychopy.visual.textbox2.fontmanager import FontManager
import pytest
from psychopy.tests import utils

# cd psychopy/psychopy
# py.test -k textbox --cov-report term-missing --cov visual/textbox

@pytest.mark.textbox
class Test_textbox(object):
    def setup_class(self):
        self.win = Window([128,128], pos=[50,50], allowGUI=False, autoLog=False)

    def teardown_class(self):
        self.win.close()

    def test_glyph_rendering(self):
        textbox = TextBox2(self.win, "", "Arial", pos=(0,0), size=(1,1), letterHeight=0.1, units='height')
        # Add all Noto Sans fonts to cover widest possible base of handles characters
        textbox.fontMGR.addGoogleFonts(["Noto Sans",
                                        "Noto Sans HK",
                                        "Noto Sans JP",
                                        "Noto Sans KR",
                                        "Noto Sans SC",
                                        "Noto Sans TC",
                                        "Niramit",
                                        "Indie Flower"])
        # Some exemplar text to test basic TextBox rendering
        exemplars = [
            # An English pangram
            {"text": "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question.",
             "font": "Noto Sans",
             "screenshot": "textbox_exemplar_1.png"},
            # The same pangram in IPA
            {"text": "ə saɪkəʊpaɪ zɛlət nəʊz ə smidge ɒv wx, bʌt ˈʤɑːvəskrɪpt ɪz ðə ˈkwɛsʧən",
                "font": "Noto Sans",
                "screenshot": "textbox_exemplar_2.png"},
            # The same pangram in Hangul
            {"text": "아 프시초피 제알롣 크노W스 아 s믿게 오f wx, 붇 자v앗c립t 잇 테 q왯디온",
             "font": "Noto Sans KR",
             "screenshot": "textbox_exemplar_3.png"},
            # A noticeably non-standard font
            {"text": "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question.",
             "font": "Indie Flower",
             "screenshot": "textbox_exemplar_4.png",
            }
        ]
        # Some text which is likely to cause problems if something isn't working
        tykes = [
            # Text which doesn't render properly on Mac (Issue #3203)
            {"text": "कोशिकायें",
             "font": "Noto Sans",
             "screenshot": "textbox_tyke_1.png"},
            # Thai text which old Text component couldn't handle due to Pyglet
            {"text": "ขาว แดง เขียว เหลือง ชมพู ม่วง เทา",
             "font": "Niramit",
             "screenshot": "textbox_tyke_2.png"
             }
        ]
        # Test each case and compare against screenshot
        for case in exemplars + tykes:
            textbox.reset()
            textbox.fontMGR.addGoogleFont(case['font'])
            textbox.font = case['font']
            textbox.text = case['text']
            self.win.flip()
            textbox.draw()
            if case['screenshot']:
                # Uncomment to save current configuration as desired
                #self.win.getMovieFrame(buffer='back').save(Path(utils.TESTS_DATA_PATH) / case['screenshot'])
                utils.compareScreenshot(Path(utils.TESTS_DATA_PATH) / case['screenshot'], self.win)

    def test_colors(self):
        textbox = TextBox2(self.win, "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question.",
                           "Consolas", pos=(0, 0), size=(1, 1), letterHeight=0.1, units='height', colorSpace="rgb")
        # Some exemplar text to test basic colors
        exemplars = [
            # White on black in rgb
            {"color": (1, 1, 1), "fillColor": (-1,-1,-1), "borderColor": (-1,-1,-1), "space": "rgb",
             "screenshot": "textbox_colors_WOB.png"},
            # White on black in named
            {"color": "white", "fillColor": "black", "borderColor": "black", "space": "rgb",
             "screenshot": "textbox_colors_WOB.png"},
            # White on black in hex
            {"color": "#ffffff", "fillColor": "#000000", "borderColor": "#000000", "space": "hex",
             "screenshot": "textbox_colors_WOB.png"},
        ]
        # Some colors which are likely to cause problems if something isn't working
        tykes = [
            # Text only
            {"color": "white", "fillColor": None, "borderColor": None, "space": "rgb",
             "screenshot": "textbox_colors_tyke1.png"},
            # The following will only work when the Color class is implemented (currently opacity is all or nothing)
            # Fill only
            # {"color": None, "fillColor": "white", "borderColor": None, "space": "rgb",
            #  "screenshot": "textbox_colors_tyke2.png"},
            # Border only
            # {"color": None, "fillColor": None, "borderColor": "white", "space": "rgb",
            # "screenshot": "textbox_colors_tyke3.png"},
        ]
        # Test each case and compare against screenshot
        for case in exemplars + tykes:
            # Raise error if case spec does not contain all necessary keys
            if not all(key in case for key in ["color", "fillColor", "borderColor", "space", "screenshot"]):
                raise KeyError(f"Case spec for test_colors in class {self.__class__.__name__} ({__file__}) invalid, test cannot be run.")
            # Apply params from case spec
            textbox.colorSpace = case['space']
            textbox.color = case['color']
            textbox.fillColor = case['fillColor']
            textbox.borderColor = case['borderColor']
            # Temporary measure until the Color class is implemented, at which point pallette will update automatically
            textbox.pallette = {"lineColor": textbox.borderColor,
                                "lineWidth": textbox.borderWidth,
                                "fillColor": textbox.fillColor}
            self.win.flip()
            textbox.draw()
            if case['screenshot']:
                # Uncomment to save current configuration as desired
                # self.win.getMovieFrame(buffer='back').save(Path(utils.TESTS_DATA_PATH) / case['screenshot'])
                utils.compareScreenshot(Path(utils.TESTS_DATA_PATH) / case['screenshot'], self.win)


    def test_basic(self):
        pass

    def test_something(self):
        # to-do: test visual display, char position, etc
        pass
