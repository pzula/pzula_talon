# Adapated from https://github.com/pokey/pokey_talon/blob/900b6ae2ab7b978efa7605371fd43ad353ae8d2e/code/parse_phrase.py
from talon import Module, speech_system, scope, actions
from talon.grammar import Phrase
from typing import Union
import logging

phrase_stack = []
def on_pre_phrase(d): phrase_stack.append(d)
def on_post_phrase(d): phrase_stack.pop()
speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)

mod = Module()
@mod.action_class
class Actions:
    def rerun_phrase(phrase: Union[str,Phrase]):
        """Rerun phrase"""
        # this is a quite unstable API
        if not phrase: return
        current_phrase = phrase_stack[-1]
        ts = current_phrase["_ts"]
        start = phrase.words[0].start - ts
        end = phrase.words[-1].end - ts
        samples = current_phrase["samples"]
        pstart = int(start * 16_000)
        pend = int(end * 16_000)
        samples = samples[pstart:pend]
        speech_system._on_audio_frame(samples)

    def momentary(phrase: Phrase):
        """Run the given phrase as if in command mode."""
        checked_modes = list(scope.get('mode').intersection({'command', 'sleep', 'dictation'}))
        if 1 != len(checked_modes):
            logging.info(f"momentary command ignored, modes: {checked_modes}")
            return
        mode = checked_modes[0]
        actions.mode.disable(mode)
        actions.mode.enable('command')
        try:
            logging.info(f"rerunning phrase: {phrase}")
            actions.user.rerun_phrase(phrase)
        finally:
            actions.mode.disable('command')
            actions.mode.enable(mode)
