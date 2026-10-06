# Store the original English and both personal languages when a line is read.
# This preserves the player's name and other substitutions when Ctrl+T is used
# in the history menu, without changing the language preference temporarily.

init 110 python:
    def personal_history_speaker_template(node):
        if node.who == "com":
            return "Computer"
        if not node.who:
            return None
        character = renpy.python.py_eval(node.who)
        if isinstance(character, basestring):
            return character
        # Computer's dynamic name is handled above. Other dynamic expressions
        # cannot be evaluated safely to reconstruct an old captured name.
        if getattr(character, "dynamic", False):
            return None
        name = getattr(character, "name", None)
        return name if isinstance(name, basestring) else None

    def personal_record_history_languages(entry):
        identifier = renpy.game.context().translate_identifier
        if not identifier:
            return
        identifier = identifier.replace(".", "_")
        translator = renpy.game.script.translator
        original = translator.default_translates.get(identifier)
        if _preferences.language is None:
            active = original
        else:
            active = translator.language_translates.get((identifier, _preferences.language))
        if active is None:
            active = translator.default_translates.get(identifier)
        if active is None:
            return
        active_says = [node for node in active.block if isinstance(node, renpy.ast.Say)]
        raw = getattr(renpy.store, "_last_raw_what", None)
        positions = [index for index, node in enumerate(active_says) if node.what == raw]
        if not positions:
            return
        position = positions[-1]
        values = {}
        names = {}
        for language in (None, "latin", "spanish"):
            if language is None:
                translated = original
            else:
                translated = translator.language_translates.get((identifier, language), original)
            if translated is None:
                continue
            says = [node for node in translated.block if isinstance(node, renpy.ast.Say)]
            if position >= len(says):
                continue
            node = says[position]
            values[language] = renpy.substitutions.substitute(node.what, translate=False)[0]
            name = personal_history_speaker_template(node)
            if node.who and name is None:
                name = entry.who
            if name:
                name = renpy.translation.translate_string(name, language=language)
                names[language] = renpy.substitutions.substitute(name, translate=False)[0]
            else:
                names[language] = None
        entry.personal_language_text = values
        entry.personal_language_name = names

    def personal_history_english_index():
        # Cache on the function, outside saved/rollback store variables.
        index = getattr(personal_history_english_index, "cache", None)
        if index is not None:
            return index
        index = {}
        translator = renpy.game.script.translator
        for identifier, original in translator.default_translates.items():
            blocks = [translator.language_translates.get((identifier, language))
                for language in ("latin", "spanish")]
            if any(block is None for block in blocks):
                continue
            originals = [node for node in original.block if isinstance(node, renpy.ast.Say)]
            translations = [[node for node in block.block if isinstance(node, renpy.ast.Say)]
                for block in blocks]
            for position, node in enumerate(originals):
                if any(position >= len(says) for says in translations):
                    continue
                pair = tuple(says[position].what for says in translations)
                # Old entries do not retain raw values for substitutions. Do
                # not re-evaluate them with today's player name or variables.
                if any("[" in text for text in (node.what,) + pair):
                    continue
                name = personal_history_speaker_template(node)
                if node.who and name is None:
                    continue
                if name and "[" in name and name != "[mc]":
                    continue
                names = tuple(renpy.translation.translate_string(name, language=language)
                    if name else None for language in ("latin", "spanish"))
                candidate = (node.what, name, names)
                index.setdefault(pair, set()).add(candidate)
        personal_history_english_index.cache = index
        return index

    def personal_recover_history_english(entry):
        values = getattr(entry, "personal_language_text", {})
        names = getattr(entry, "personal_language_name", {})
        if None in values or not all(language in values and language in names
                for language in ("latin", "spanish")):
            return
        pair = (values["latin"], values["spanish"])
        captured_names = (names["latin"], names["spanish"])
        matches = set()
        for text, name, translated_names in personal_history_english_index().get(pair, ()):
            if name == "[mc]":
                # The player speaker's captured name is already identical in
                # both languages; copy it verbatim without substituting again.
                if captured_names[0] != captured_names[1] or not isinstance(captured_names[0], basestring):
                    continue
                english_name = captured_names[0]
            elif captured_names == translated_names:
                english_name = renpy.translation.translate_string(name, language=None) if name else None
            else:
                continue
            matches.add((text, english_name))
        if len(matches) == 1:
            text, name = matches.pop()
            # Copy the mappings so existing captured values remain untouched.
            entry.personal_language_text = dict(values)
            entry.personal_language_name = dict(names)
            entry.personal_language_text[None] = text
            entry.personal_language_name[None] = name

    def personal_history_text(entry):
        if _preferences.language is None:
            personal_recover_history_english(entry)
        return getattr(entry, "personal_language_text", {}).get(_preferences.language, entry.what)

    def personal_history_name(entry):
        if _preferences.language is None:
            personal_recover_history_english(entry)
        return getattr(entry, "personal_language_name", {}).get(_preferences.language, entry.who)

    config.history_callbacks.append(personal_record_history_languages)


# Match the game's existing history layout and styling.
screen history():
    tag menu
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):
        style_prefix "history"

        for h in _history_list:
            window:
                has fixed:
                    yfit True

                if personal_history_name(h):
                    label personal_history_name(h):
                        style "history_name"
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text personal_history_text(h) substitute False

        if not _history_list:
            label _("The dialogue history is empty.")
