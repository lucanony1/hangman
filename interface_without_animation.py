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

    nb_mistakes = 0
    given_letters = []
    given_letter = ""
    alphabet_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    windows = pygame.display.set_mode((screen_width, screen_height))
    loop = True
    background = pygame.Surface(windows.get_size())

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
                    main(clean_word(init_word_to_find("liste_francais.txt")))
                    return

                if game_finished and event.key == pygame.K_q:
                    pygame.quit()
                    return

        if all(letter in given_letters for letter in word.upper()):
            game_finished = True

        if lives == 0:
            game_finished = True

        background.fill(sky)
        windows.blit(background, (0, 0))

        pygame.draw.rect(
            windows,
            (143, 231, 255),
            (0, 0, screen_width, screen_height),
            0
        )

        pygame.draw.rect(
            windows,
            (0, 255, 0),
            (0, 550, 800, 50),
            0
        )

        pygame.draw.rect(
            windows,
            (127, 127, 127),
            (0, 600, 800, screen_height - 600),
            0
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

        draw_data(windows, given_letters, word)
        draw_hangman(windows, nb_mistakes)

        if game_finished:

            font = pygame.font.SysFont("Arial", 100)
            font2 = pygame.font.SysFont("Arial", 50)

            if lives == 0:
                text = font.render(
                    "LOOSE",
                    True,
                    (255, 0, 0)
                )
            else:
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

            windows.blit(text, (850, 300))
            windows.blit(retry, (850, 450))
            windows.blit(quit_text, (850, 520))

        pygame.display.flip()
        clock.tick(10)


def draw_data(windows: pygame.Surface, letters, word):
    police_50 = pygame.font.SysFont("Arial", 50)
    police_40 = pygame.font.SysFont("Arial", 40)

    write_color = (0, 0, 0)

    text = police_50.render("Tu es pendu pendu", True, write_color)
    windows.blit(text, (1200, 200))

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
                (1200, 300 + 50 * nb_lines_written)
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
            (1200, 300 + 50 * nb_lines_written)
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
            "Word : " + display_word(word, letters),
            True,
            (0, 0, 0)
        ),
        (1200, 500)
    )


def draw_hangman(windows, mistakes):

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


if __name__ == "__main__":
    random_word = init_word_to_find("liste_francais.txt")
    random_word = clean_word(random_word)
    main(random_word)