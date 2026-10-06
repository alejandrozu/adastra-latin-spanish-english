# Personal Latin / Spanish / original English controls for Adastra 17.
# Compatible with the bundled Ren'Py 6.99.12.3 engine.
# Translation content lives separately in game/tl/latin and game/tl/spanish.

init 100 python:
    config.default_language = "latin"

    # The engine checks this binding before any screen receives a key event.
    # Removing Ctrl here prevents a press of Ctrl+T from skipping dialogue.
    # Tab still toggles skipping through the separate toggle_skip binding.
    config.keymap["skip"] = [
        key for key in config.keymap.get("skip", [])
        if key not in ("K_LCTRL", "K_RCTRL")
    ]
    config.keymap["personal_toggle_language"] = ["ctrl_K_t"]

    def personal_enabled_language_ids():
        order = ("latin", "spanish", "english")
        saved = persistent._personal_enabled_languages
        if not isinstance(saved, (list, tuple)):
            return order
        enabled = tuple(language for language in order if language in saved)
        return enabled or order

    def personal_current_language_id():
        return "english" if _preferences.language is None else _preferences.language

    def personal_engine_language(identifier):
        return None if identifier == "english" else identifier

    def personal_language_label(identifier):
        if _preferences.language == "spanish":
            labels = {"latin": u"Latín", "spanish": u"Español", "english": u"Inglés"}
        elif _preferences.language is None:
            labels = {"latin": "Latin", "spanish": "Spanish", "english": "English"}
        else:
            labels = {"latin": "Latina", "spanish": "Hispanica", "english": "Anglica"}
        return labels[identifier]

    def personal_language_cycle_caption():
        return u"Ctrl+T: " + u" / ".join(personal_language_label(language)
            for language in personal_enabled_language_ids())

    def personal_language_help():
        if _preferences.language == "spanish":
            return u"Alterna entre los idiomas activados. Elígelos en Opciones."
        if _preferences.language is None:
            return "Cycles enabled languages. Choose them in Options."
        return "Linguas activas vicissim eligit. In Optionibus eas delige."

    def personal_set_language(language):
        if language not in ("latin", "spanish", None):
            return
        identifier = "english" if language is None else language
        if identifier not in personal_enabled_language_ids():
            return

        # A language change interrupts active Tab skipping and redraws the
        # current translation unit. It does not dismiss the dialogue/menu.
        config.skipping = None
        # None selects Ren'Py's original English text.
        persistent._personal_english_selected = (language is None)
        renpy.change_language(language)
        renpy.save_persistent()

    def personal_toggle_language():
        enabled = personal_enabled_language_ids()
        current = personal_current_language_id()
        if current in enabled:
            identifier = enabled[(enabled.index(current) + 1) % len(enabled)]
        else:
            identifier = enabled[0]
        if identifier != current:
            personal_set_language(personal_engine_language(identifier))

    def personal_toggle_language_enabled(identifier):
        if identifier not in ("latin", "spanish", "english"):
            return
        enabled = list(personal_enabled_language_ids())
        if identifier in enabled:
            if len(enabled) == 1:
                return
            enabled.remove(identifier)
        else:
            enabled.append(identifier)
        persistent._personal_enabled_languages = [language
            for language in ("latin", "spanish", "english") if language in enabled]
        if personal_current_language_id() not in enabled:
            personal_set_language(personal_engine_language(personal_enabled_language_ids()[0]))
        else:
            renpy.save_persistent()
            renpy.restart_interaction()

    def personal_ensure_language_controls():
        # Menus suppress normal overlay screens. This callback runs after
        # overlay suppression and before the scene layers are assembled, so
        # direct placement on screens keeps Ctrl+T available in all contexts.
        # Existing screens update naturally at the next interaction; never
        # restart an interaction from this callback.
        if renpy.get_screen("personal_language_controls", layer="screens") is None:
            renpy.show_screen("personal_language_controls", _layer="screens")

    config.interact_callbacks.append(personal_ensure_language_controls)

init 1600 python:
    # Remember which languages participate, but start each launch in Latin
    # whenever it is enabled. Otherwise use Spanish, then original English.
    persistent._personal_enabled_languages = list(personal_enabled_language_ids())
    _preferences.language = personal_engine_language(personal_enabled_language_ids()[0])
    persistent._personal_english_selected = (_preferences.language is None)
    persistent._personal_languages_initialized = True


screen personal_language_controls():
    zorder 1000

    key "ctrl_K_t" action Function(personal_toggle_language, _update_screens=False)

    # Keep the story and other menus visually unchanged. Language selection
    # is available at the bottom right of the existing preferences screen.
    if renpy.get_screen("preferences"):
        $ enabled_languages = personal_enabled_language_ids()
        frame:
            background Solid("#12151cdd")
            xalign 1.0
            yalign 1.0
            xoffset -54
            yoffset -180
            padding (22, 14)

            vbox:
                spacing 7

                hbox:
                    spacing 22

                    text ("Idioma" if _preferences.language == "spanish" else "Language" if _preferences.language is None else "Lingua"):
                        size 26
                        color gui.accent_color

                    textbutton personal_language_label("latin"):
                        text_size 26
                        selected (_preferences.language == "latin")
                        sensitive ("latin" in enabled_languages)
                        action Function(personal_set_language, "latin")

                    textbutton personal_language_label("spanish"):
                        text_size 26
                        selected (_preferences.language == "spanish")
                        sensitive ("spanish" in enabled_languages)
                        action Function(personal_set_language, "spanish")

                    textbutton personal_language_label("english"):
                        text_size 26
                        selected (_preferences.language is None)
                        sensitive ("english" in enabled_languages)
                        action Function(personal_set_language, None)

                hbox:
                    spacing 18

                    text "Ctrl+T":
                        size 22
                        color gui.accent_color
                        yalign 0.5

                    for identifier in ("latin", "spanish", "english"):
                        textbutton personal_language_label(identifier):
                            style "check_button"
                            text_style "check_button_text"
                            text_size 22
                            selected (identifier in enabled_languages)
                            sensitive (identifier not in enabled_languages or len(enabled_languages) > 1)
                            action Function(personal_toggle_language_enabled, identifier, _update_screens=False)

                text personal_language_cycle_caption():
                    size 21
                    color "#dddddd"

                text ("Mantén al menos un idioma activado." if _preferences.language == "spanish" else "Keep at least one language enabled." if _preferences.language is None else "Saltem una lingua activa maneat."):
                    size 19
                    color "#bbbbbb"
