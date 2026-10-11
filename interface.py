import random
import pygame

from main import init_word_to_find, display_word, clean_word

screen_width = 1920
screen_height = 1020

pygame.init()

clock = pygame.time.Clock()

sky = 0, 0, 0


def main(word):

    lives = 11
    game_finished = False

    explosion_started = False
    explosion_timer = 0

    nb_mistakes = 0
    given_letters = []
    given_letter = ""

    alphabet_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    windows = pygame.display.set_mode(
        (screen_width, screen_height)
    )

    pygame.display.set_caption("Hangman")

    destroyed_background = create_destroyed_background()

    loop = True

    while loop:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                loop = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if given_letter != "":
                        if given_letter not in given_letters:

                            given_letters.append(given_letter)

                            if given_letter not in word.upper():

                                nb_mistakes += 1
                                lives -= 1

                                print("Erreur :", nb_mistakes)
                                print("Vies :", lives)

                            else:
                                print("Bonne lettre !")

                        given_letter = ""

                else:

                    new_letter = pygame.key.name(event.key)

                    if new_letter in alphabet_letters:
                        given_letter = new_letter.upper()

                if game_finished and event.key == pygame.K_r:

                    new_word = clean_word(
                        init_word_to_find("liste_francais.txt")
                    )

                    main(new_word)

                    return

                if game_finished and event.key == pygame.K_q:

                    pygame.quit()

                    return

        if all(
            letter in given_letters
            for letter in word.upper()
        ):
            game_finished = True

        if lives == 0:
            game_finished = True

        if game_finished and lives == 0:

            if not explosion_started:
                explosion_started = True
                explosion_timer = pygame.time.get_ticks()

            elapsed = pygame.time.get_ticks() - explosion_timer

            if elapsed < 650:

                draw_normal_scene(
                    windows,
                    given_letters,
                    word,
                    nb_mistakes
                )

                draw_explosion(
                    windows,
                    elapsed / 650
                )

            else:

                windows.blit(
                    destroyed_background,
                    (0, 0)
                )

                draw_fire(
                    windows
                )

                draw_destroyed_text(
                    windows
                )

        else:

            draw_normal_scene(
                windows,
                given_letters,
                word,
                nb_mistakes
            )

            if game_finished:

                draw_win_text(
                    windows
                )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def draw_normal_scene(
    windows,
    given_letters,
    word,
    mistakes
):

    windows.fill(
        (143, 231, 255)
    )

    pygame.draw.rect(
        windows,
        (0, 255, 0),
        (
            0,
            550,
            800,
            50
        )
    )

    pygame.draw.rect(
        windows,
        (127, 127, 127),
        (
            0,
            600,
            800,
            screen_height - 600
        )
    )

    pygame.draw.polygon(
        windows,
        (127, 127, 127),
        [
            (799, 671),
            (1086, 506),
            (803, 901),
            (803, 934),
            (929, 904),
            (843, 1009),
            (801, 1009)
        ]
    )

    draw_data(
        windows,
        given_letters,
        word
    )

    draw_hangman(
        windows,
        mistakes
    )


def create_destroyed_background():

    surface = pygame.Surface(
        (screen_width, screen_height)
    )

    surface.fill(
        (35, 12, 8)
    )

    random.seed(123)

    for y in range(0, 600):

        darkness = int(
            30 + y * 0.08
        )

        pygame.draw.line(
            surface,
            (
                darkness,
                max(5, darkness // 3),
                3
            ),
            (0, y),
            (screen_width, y)
        )

    draw_city(
        surface
    )

    draw_ground(
        surface
    )

    draw_debris(
        surface
    )

    draw_smoke(
        surface
    )

    draw_fire_static(
        surface
    )

    random.seed()

    return surface


def draw_city(surface):

    buildings = [
        (0, 230, 250, 470),
        (180, 310, 210, 390),
        (360, 180, 300, 520),
        (620, 280, 220, 420),
        (810, 140, 270, 560),
        (1040, 250, 260, 450),
        (1280, 170, 310, 530),
        (1560, 300, 250, 400),
        (1750, 210, 170, 490)
    ]

    for x, y, width, height in buildings:

        color = random.choice(
            [
                (45, 35, 32),
                (55, 42, 38),
                (65, 48, 42),
                (38, 32, 30)
            ]
        )

        pygame.draw.rect(
            surface,
            color,
            (
                x,
                y,
                width,
                height
            )
        )

        destroyed_top = random.randint(
            20,
            100
        )

        for i in range(8):

            px = x + random.randint(
                0,
                max(1, width - 20)
            )

            py = y + random.randint(
                0,
                min(height, 150)
            )

            pygame.draw.polygon(
                surface,
                (20, 15, 13),
                [
                    (px, py),
                    (
                        px + random.randint(20, 70),
                        py + random.randint(-40, 30)
                    ),
                    (
                        px + random.randint(40, 90),
                        py + random.randint(20, 70)
                    )
                ]
            )

        for wx in range(
            x + 25,
            x + width - 25,
            55
        ):

            for wy in range(
                y + 45,
                y + height - 40,
                70
            ):

                if random.random() < 0.35:

                    pygame.draw.rect(
                        surface,
                        (255, 90, 15),
                        (
                            wx,
                            wy,
                            28,
                            38
                        )
                    )

                    pygame.draw.rect(
                        surface,
                        (255, 210, 50),
                        (
                            wx + 6,
                            wy + 5,
                            16,
                            25
                        )
                    )

                else:

                    pygame.draw.rect(
                        surface,
                        (12, 12, 12),
                        (
                            wx,
                            wy,
                            28,
                            38
                        )
                    )

        for i in range(5):

            rx = x + random.randint(
                0,
                max(1, width - 50)
            )

            ry = y + random.randint(
                0,
                max(1, height - 40)
            )

            pygame.draw.line(
                surface,
                (15, 12, 10),
                (rx, ry),
                (
                    rx + random.randint(-60, 60),
                    ry + random.randint(30, 100)
                ),
                random.randint(5, 12)
            )

        pygame.draw.polygon(
            surface,
            (30, 22, 19),
            [
                (x - 20, y),
                (
                    x + width // 3,
                    y - destroyed_top
                ),
                (
                    x + width // 2,
                    y - destroyed_top // 2
                ),
                (
                    x + width,
                    y - destroyed_top
                ),
                (
                    x + width,
                    y + 20
                )
            ]
        )


def draw_ground(surface):

    pygame.draw.rect(
        surface,
        (28, 22, 20),
        (
            0,
            690,
            screen_width,
            330
        )
    )

    pygame.draw.rect(
        surface,
        (18, 15, 14),
        (
            0,
            820,
            screen_width,
            200
        )
    )

    for i in range(70):

        x = random.randint(
            0,
            screen_width
        )

        y = random.randint(
            700,
            1000
        )

        length = random.randint(
            30,
            180
        )

        pygame.draw.line(
            surface,
            random.choice(
                [
                    (45, 38, 34),
                    (65, 45, 35),
                    (80, 50, 30),
                    (35, 30, 28)
                ]
            ),
            (x, y),
            (
                x + length,
                y + random.randint(-20, 20)
            ),
            random.randint(3, 10)
        )


def draw_debris(surface):

    for i in range(1800):

        x = random.randint(
            0,
            screen_width
        )

        y = random.randint(
            600,
            screen_height
        )

        size = random.randint(
            5,
            35
        )

        points = [
            (x, y),
            (
                x + random.randint(
                    -size,
                    size
                ),
                y + random.randint(
                    -size,
                    size
                )
            ),
            (
                x + random.randint(
                    5,
                    size * 2
                ),
                y + random.randint(
                    5,
                    size * 2
                )
            )
        ]

        pygame.draw.polygon(
            surface,
            random.choice(
                [
                    (45, 40, 38),
                    (65, 55, 48),
                    (85, 65, 50),
                    (30, 28, 27)
                ]
            ),
            points
        )


def draw_smoke(surface):

    smoke = pygame.Surface(
        (screen_width, screen_height),
        pygame.SRCALPHA
    )

    for i in range(750):

        x = random.randint(
            0,
            screen_width
        )

        y = random.randint(
            50,
            700
        )

        radius = random.randint(
            35,
            130
        )

        pygame.draw.circle(
            smoke,
            (
                5,
                5,
                5,
                random.randint(80, 180)
            ),
            (x, y),
            radius
        )

    surface.blit(
        smoke,
        (0, 0)
    )


def draw_fire_static(surface):

    fire_positions = [
        (130, 610),
        (430, 580),
        (700, 650),
        (930, 600),
        (1190, 640),
        (1450, 590),
        (1710, 640),
        (1850, 560)
    ]

    for x, y in fire_positions:

        draw_flame(
            surface,
            x,
            y,
            random.randint(90, 160)
        )


def draw_fire(surface):

    current_time = pygame.time.get_ticks()

    random.seed(
        current_time // 90
    )

    fire_positions = [
        (130, 610),
        (430, 580),
        (700, 650),
        (930, 600),
        (1190, 640),
        (1450, 590),
        (1710, 640),
        (1850, 560)
    ]

    for x, y in fire_positions:

        size = random.randint(
            100,
            180
        )

        draw_flame(
            surface,
            x,
            y,
            size
        )

    random.seed()


def draw_flame(
    surface,
    x,
    y,
    size
):

    pygame.draw.ellipse(
        surface,
        (180, 30, 0),
        (
            x - size // 2,
            y - size,
            size,
            size
        )
    )

    pygame.draw.polygon(
        surface,
        (255, 70, 0),
        [
            (
                x,
                y - size * 2
            ),
            (
                x - size // 2,
                y - size // 2
            ),
            (
                x - size // 3,
                y
            ),
            (
                x + size // 3,
                y
            ),
            (
                x + size // 2,
                y - size // 2
            )
        ]
    )

    pygame.draw.polygon(
        surface,
        (255, 170, 0),
        [
            (
                x,
                y - int(size * 1.45)
            ),
            (
                x - int(size * 0.28),
                y - int(size * 0.35)
            ),
            (
                x,
                y
            ),
            (
                x + int(size * 0.28),
                y - int(size * 0.35)
            )
        ]
    )

    pygame.draw.polygon(
        surface,
        (255, 240, 120),
        [
            (
                x,
                y - int(size * 0.9)
            ),
            (
                x - int(size * 0.12),
                y - int(size * 0.25)
            ),
            (
                x + int(size * 0.12),
                y - int(size * 0.25)
            )
        ]
    )


def draw_data(
    windows,
    letters,
    word
):

    police_50 = pygame.font.SysFont(
        "Arial",
        50
    )

    police_40 = pygame.font.SysFont(
        "Arial",
        40
    )

    write_color = (0, 0, 0)

    text = police_50.render(
        "Tu es pendu pendu",
        True,
        write_color
    )

    windows.blit(
        text,
        (1200, 200)
    )

    nb_letters_per_line = 8
    current_letter_per_line = 0
    current_displayed_letters = ""
    nb_lines_written = 0

    for letter in letters:

        if current_letter_per_line == nb_letters_per_line:

            windows.blit(
                police_40.render(
                    current_displayed_letters,
                    True,
                    (0, 0, 0)
                ),
                (
                    1200,
                    300 + 50 * nb_lines_written
                )
            )

            current_letter_per_line = 0
            current_displayed_letters = ""
            nb_lines_written += 1

        current_displayed_letters += letter
        current_letter_per_line += 1

    if current_displayed_letters != "":

        windows.blit(
            police_40.render(
                current_displayed_letters,
                True,
                (0, 0, 0)
            ),
            (
                1200,
                300 + 50 * nb_lines_written
            )
        )

    windows.blit(
        police_40.render(
            "Tries : " + str(len(letters)),
            True,
            (0, 0, 0)
        ),
        (1200, 450)
    )

    windows.blit(
        police_40.render(
            "Word : " + display_word(
                word,
                letters
            ),
            True,
            (0, 0, 0)
        ),
        (1200, 500)
    )


def draw_hangman(
    windows,
    mistakes
):

    if mistakes >= 1:

        pygame.draw.line(
            windows,
            (139, 69, 19),
            (50, 540),
            (450, 540),
            20
        )

    if mistakes >= 2:

        pygame.draw.line(
            windows,
            (139, 69, 19),
            (250, 550),
            (250, 100),
            20
        )

    if mistakes >= 3:

        pygame.draw.line(
            windows,
            (139, 69, 19),
            (346, 97),
            (250, 205),
            20
        )

    if mistakes >= 4:

        pygame.draw.line(
            windows,
            (139, 69, 19),
            (241, 95),
            (510, 95),
            20
        )

    if mistakes >= 5:

        pygame.draw.line(
            windows,
            (255, 255, 255),
            (500, 95),
            (500, 175),
            5
        )

    if mistakes >= 6:

        pygame.draw.circle(
            windows,
            (0, 0, 0),
            (500, 220),
            45,
            5
        )

    if mistakes >= 7:

        pygame.draw.line(
            windows,
            (0, 0, 0),
            (500, 265),
            (500, 350),
            5
        )

    if mistakes >= 8:

        pygame.draw.line(
            windows,
            (0, 0, 0),
            (500, 300),
            (450, 300),
            5
        )

    if mistakes >= 9:

        pygame.draw.line(
            windows,
            (0, 0, 0),
            (500, 300),
            (550, 300),
            5
        )

    if mistakes >= 10:

        pygame.draw.line(
            windows,
            (0, 0, 0),
            (500, 350),
            (450, 420),
            5
        )

    if mistakes >= 11:

        pygame.draw.line(
            windows,
            (0, 0, 0),
            (500, 350),
            (550, 420),
            5
        )


def draw_explosion(
    windows,
    progress
):

    cx = 960 + random.randint(-20, 20)
    cy = 480 + random.randint(-20, 20)

    scale = 1.7 + progress * 1.5

    pygame.draw.circle(
        windows,
        (245, 245, 245),
        (
            cx,
            cy
        ),
        int(230 * scale)
    )

    pygame.draw.rect(
        windows,
        (245, 245, 245),
        (
            cx - int(190 * scale),
            cy + int(100 * scale),
            int(380 * scale),
            int(190 * scale)
        )
    )

    pygame.draw.ellipse(
        windows,
        (0, 0, 0),
        (
            cx - int(165 * scale),
            cy - int(115 * scale),
            int(105 * scale),
            int(140 * scale)
        )
    )

    pygame.draw.ellipse(
        windows,
        (0, 0, 0),
        (
            cx + int(60 * scale),
            cy - int(115 * scale),
            int(105 * scale),
            int(140 * scale)
        )
    )

    pygame.draw.polygon(
        windows,
        (0, 0, 0),
        [
            (
                cx,
                cy
            ),
            (
                cx - int(55 * scale),
                cy + int(110 * scale)
            ),
            (
                cx + int(55 * scale),
                cy + int(110 * scale)
            )
        ]
    )

    for i in range(9):

        pygame.draw.rect(
            windows,
            (0, 0, 0),
            (
                cx - int(165 * scale) + i * int(40 * scale),
                cy + int(145 * scale),
                int(22 * scale),
                int(85 * scale)
            )
        )

    if progress < 0.7:

        pygame.draw.circle(
            windows,
            (255, 0, 0),
            (
                cx - int(110 * scale),
                cy - int(50 * scale)
            ),
            int(22 * scale)
        )

        pygame.draw.circle(
            windows,
            (255, 0, 0),
            (
                cx + int(110 * scale),
                cy - int(50 * scale)
            ),
            int(22 * scale)
        )

    for i in range(35):

        angle = random.uniform(
            0,
            6.283185
        )

        distance = (
            progress
            * random.randint(
                300,
                900
            )
        )

        x = int(
            cx
            + pygame.math.Vector2(
                1,
                0
            ).rotate(
                -angle * 57.2958
            ).x
            * distance
        )

        y = int(
            cy
            + pygame.math.Vector2(
                1,
                0
            ).rotate(
                -angle * 57.2958
            ).y
            * distance
        )

        pygame.draw.circle(
            windows,
            random.choice(
                [
                    (255, 40, 0),
                    (255, 100, 0),
                    (255, 220, 0),
                    (255, 255, 255)
                ]
            ),
            (
                x,
                y
            ),
            random.randint(
                5,
                30
            )
        )


def draw_destroyed_text(
    windows
):

    font = pygame.font.SysFont(
        "Arial",
        100,
        bold=True
    )

    font2 = pygame.font.SysFont(
        "Arial",
        50,
        bold=True
    )

    text = font.render(
        "LOOSE",
        True,
        (255, 40, 0)
    )

    retry = font2.render(
        "R to retry",
        True,
        (255, 255, 255)
    )

    quit_text = font2.render(
        "Q to quit",
        True,
        (255, 255, 255)
    )

    shadow = font.render(
        "LOOSE",
        True,
        (0, 0, 0)
    )

    windows.blit(
        shadow,
        (856, 306)
    )

    windows.blit(
        text,
        (850, 300)
    )

    windows.blit(
        retry,
        (850, 450)
    )

    windows.blit(
        quit_text,
        (850, 520)
    )


def draw_win_text(
    windows
):

    font = pygame.font.SysFont(
        "Arial",
        100
    )

    font2 = pygame.font.SysFont(
        "Arial",
        50
    )

    text = font.render(
        "WIN",
        True,
        (0, 255, 0)
    )

    retry = font2.render(
        "R to retry",
        True,
        (0, 0, 0)
    )

    quit_text = font2.render(
        "Q to quit",
        True,
        (0, 0, 0)
    )

    windows.blit(
        text,
        (850, 300)
    )

    windows.blit(
        retry,
        (850, 450)
    )

    windows.blit(
        quit_text,
        (850, 520)
    )


if __name__ == "__main__":

    random_word = init_word_to_find(
        "liste_francais.txt"
    )

    random_word = clean_word(
        random_word
    )

    main(random_word)