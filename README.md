# Adastra 17 — Latin, Spanish and English

An unofficial localization of [Adastra by the Echo Project](https://echoproject.itch.io/adastra), including the Windows game, Latin and Spanish translations, and the original English text.

1. Choose **Code → Download ZIP** on this repository.
2. Extract the entire ZIP.
3. Open `Adastra-17-win/Adastra.exe`. Keep the game folder and its contents together.

Compiled game scripts (`.rpyc`) are omitted; their matching `.rpy` sources are included. The first launch may take a few minutes while Ren’Py compiles them.

Each launch starts in **Latin** when it is enabled. Otherwise it starts in Spanish, then English, depending on which languages are enabled.

- **Ctrl+T** cycles Latin → Spanish → English → Latin, skipping disabled languages.
- Open **Optiones / Opciones / Options** to select a language directly.
- In the row marked **Ctrl+T**, click a language to include or exclude it. Gold markers indicate enabled languages. Choices persist between launches.
- At least one language must remain enabled. With only one enabled, Ctrl+T does nothing. Disabling the current language selects the first remaining language.

New dialogue history retains all three versions; older entries may retain their previously captured wording.

The original creator credits, copyright notices, and bundled engine/font licenses are retained. This modification is not an official Echo Project release.

Validation: the bundled engine’s lint and automated shortcut tests passed, including all seven enabled-language combinations. Language buttons were checked in the running game. A physical Ctrl+T keypress has not been independently confirmed; the entire story has not been played through.
