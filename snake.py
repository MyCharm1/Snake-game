import curses
import random

def main(stdscr):
    # Setup screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Initialize terminal colors
    curses.start_color()
    curses.use_default_colors()

    # Define color pairs: curses.init_pair(PAIR_ID, FOREGROUND, BACKGROUND)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Border

    sh, sw = stdscr.getmaxyx()
    w = stdscr.subwin(sh, sw, 0, 0)

    # Draw border around the playing area
    w.attron(curses.color_pair(3))
    w.border(0, 0, 0, 0, 0, 0, 0, 0)
    w.attroff(curses.color_pair(3))

    # Initial Snake and Food position
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [sh // 2, sw // 2]
    w.addch(int(food[0]), int(food[1]), '*', curses.color_pair(2))

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Check loss condition (hit border or hit self)
        if (snake[0][0] in [0, sh - 1] or 
            snake[0][1] in [0, sw - 1] or 
            snake[0] in snake[1:]):
            msg = f"Game Over! Final Score: {score}"
            w.addstr(sh // 2, (sw - len(msg)) // 2, msg)
            w.refresh()
            curses.napms(2000)
            break

        # Calculate new head location
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # Check eating food
        if snake[0] == food:
            score += 10
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], '*', curses.color_pair(2))
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        # Draw Snake Head/Body using 'O' symbol and Green color
        w.addch(int(snake[0][0]), int(snake[0][1]), 'O', curses.color_pair(1))

if __name__ == "__main__":
    curses.wrapper(main)