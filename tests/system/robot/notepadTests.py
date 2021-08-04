# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for reading text using NVDA in the notepad text editor.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
import typing

from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from NotepadLib import NotepadLib as _NotepadLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib
from robot.libraries.BuiltIn import BuiltIn

builtIn: BuiltIn = BuiltIn()
_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")

navToNextCharKey = "numpad3"
navToNextWordKey = "numpad6"
navToNextLineKey = "numpad9"


def _pressKeyAndCollectSpeech(key: str, numberOfTimes: int) -> typing.List[str]:
	actual = []
	for _ in range(numberOfTimes):
		spoken = _NvdaLib.getSpeechAfterKey(key)
		# collect all output before asserting to show full picture of behavior
		actual.append(spoken)
	return actual


def test_moveByWord_symbolLevelWord():
	"""Disabled due to revert of PR #11856 is: "Speak all symbols when moving by words (#11779)
	"""
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], True)

	# unlike other symbols used, symbols.dic doesn't preserve quote symbols with SYMPRES_ALWAYS
	_wordsToExpected = {
		'Say': 'Say',
		'(quietly)': 'left paren(quietly right paren)',
		'"Hello,': 'quote Hello comma,',
		'Jim".': 'Jim quote  dot.',
		'➔': 'right-pointing arrow',  # Speech for symbols shouldn't change
		'👕': 't-shirt',  # Speech for symbols shouldn't change
	}

	textStr = ' '.join(_wordsToExpected.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	actual = _pressKeyAndCollectSpeech(navToNextWordKey, numberOfTimes=len(_wordsToExpected))
	builtIn.should_be_equal(actual, list(_wordsToExpected.values()))


def test_moveByWord():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	_wordsToExpected = {
		'Say': 'Say',
		'(quietly)': '(quietly)',
		'"Hello,': 'Hello,',
		'Jim".': 'Jim .',
		'➔': 'right pointing arrow',
		'👕': 't shirt',
	}

	textStr = ' '.join(_wordsToExpected.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	actual = _pressKeyAndCollectSpeech(navToNextWordKey, numberOfTimes=len(_wordsToExpected))
	builtIn.should_be_equal(actual, list(_wordsToExpected.values()))


def test_moveByLine():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	_wordsToExpected = {
		'Say': 'Say',
		'(quietly)': '(quietly)',
		'"Hello,': 'Hello,',
		'Jim".': 'Jim .',
		'➔': 'right-pointing arrow',
		'👕': 't-shirt',
	}

	textStr = '\n'.join(_wordsToExpected.keys())
	_notepad.prepareNotepad(f"Test:\n{textStr}")  # initial new line which isn't spoken
	actual = _pressKeyAndCollectSpeech(navToNextLineKey, numberOfTimes=len(_wordsToExpected))
	builtIn.should_be_equal(actual, list(_wordsToExpected.values()))


def test_moveByChar():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	_text = 'S ()e,➔👕'  # to speed up test, reduce superfluous characters
	_expected = [
		'S',
		'space',
		'left paren',
		'right paren',
		'e',
		'comma',
		'right pointing arrow',
		't shirt',
	]

	_notepad.prepareNotepad(f" {_text}")
	actual = _pressKeyAndCollectSpeech(navToNextCharKey, numberOfTimes=len(_expected))
	builtIn.should_be_equal(actual, _expected)
