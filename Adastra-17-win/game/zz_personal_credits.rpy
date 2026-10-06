# Native personal localization of the two end-credit images and Computer name.
# Original artwork is preserved on disk. Text overlays are selected at every
# interaction, so Ctrl+T also changes the credits currently on screen.

init 200 python:
    def personal_credit_line(text, width, size, color="#c9af8f"):
        return Text(text, font="RobotoSlab-ExtraBold.ttf", size=size,
            color=color, text_align=0.5, xminimum=width, xmaximum=width,
            outlines=[], substitute=False)

    def personal_credit_strip(text, top, width, height, size, color="#c9af8f"):
        left = (1920 - width) // 2
        return [
            (left, top), Solid("#131222", xsize=width, ysize=height),
            (left, top + 4), personal_credit_line(text, width, size, color),
        ]

    def personal_make_credits(language, second=False):
        filename = "images/backgrounds/credits2.png" if second else "images/backgrounds/credits.png"
        pieces = [(0, 0), filename]

        if second:
            if language == "spanish":
                thanks = u"Adastra ha sido posible gracias al generoso apoyo de nuestros mecenas en Patreon."
                copyright_line = u"Adastra ©2020 Echo Project. Todos los derechos reservados."
            else:
                thanks = u"Adastra auxilio liberalium fautorum nostrorum in Patreon fieri potuit."
                copyright_line = u"Adastra ©2020 Echo Project. Omnia iura reservata."

            pieces.extend(personal_credit_strip(thanks, 802, 1600, 54, 32, "#ffffff"))
            pieces.extend(personal_credit_strip(copyright_line, 1008, 1420, 49, 28, "#ffffff"))
        else:
            if language == "spanish":
                labels = [u"Guion", u"Arte de personajes e ilustraciones", u"Arte de fondos", u"Diseño de interfaz"]
            else:
                labels = ["Scriptum ab", "Imagines personarum et illustrationes", "Imagines locorum", "Interfacies usoris"]

            # Only the English headings are covered. The Adastra title art,
            # creators' names, their URLs and the cosmic background remain.
            for label, top, width, size in zip(labels,
                    [212, 398, 632, 862], [900, 1360, 1020, 1060], [48, 43, 48, 48]):
                pieces.extend(personal_credit_strip(label, top, width, 69, size))

        return LiveComposite((1920, 1080), *pieces)

    personal_credits_images = {
        ("latin", False): personal_make_credits("latin", False),
        ("latin", True): personal_make_credits("latin", True),
        ("spanish", False): personal_make_credits("spanish", False),
        ("spanish", True): personal_make_credits("spanish", True),
    }

    def personal_current_credits(st, at, second=False):
        language = _preferences.language
        if language in ("latin", "spanish"):
            return personal_credits_images[(language, second)], None
        return ("images/backgrounds/credits2.png" if second else "images/backgrounds/credits.png"), None

    renpy.image("bg credits", DynamicDisplayable(personal_current_credits, False))
    renpy.image("bg credits2", DynamicDisplayable(personal_current_credits, True))

    def personal_computer_name():
        return {"latin": "Computatrum", "spanish": "Ordenador"}.get(_preferences.language, "Computer")

    # Inherit the existing character so its color, dialogue style, callbacks,
    # screen, voice configuration and history behavior stay the same.
    com = Character("personal_computer_name()", kind=com, dynamic=True)
