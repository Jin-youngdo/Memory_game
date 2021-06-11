import pygame
from random import *

# 레벨 설정
def setup(level):
    # 얼마동안 숫자를 보여줄지
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)

    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # 최대수 20 제한

    # 실제 화면에 grid 형태의 숫자를 랜덤으로 배치
    shuffle_grid(number_count)

# 숫자 셔플
def shuffle_grid(number_count):
    rows = 5
    cols = 9
    cell_size = 130 # 각 grid cell 별 세로, 가로 크기
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    grid = [[0 for col in range(cols)] for row in range(rows)] # 5x9

    number = 1 # 1 ~ number_count 까지 숫자 랜덤 배치
    while number <= number_count:
        row_idx = randrange(0, rows) # 0 ~ 4
        col_idx = randrange(0, cols) # 0 ~ 8

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            # 현재 grid cell 위치 기준으로 x, y 값 구함
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)

# 시작 화면 시각화
def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)

    screen.blit(msg, msg_rect)

# 게임 시작 문구 보여주기
def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> sec
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):

        if hidden : #숨김 처리
            # 버튼 사각형 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # 실제 숫자 텍스트
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

# pos에 해당하는 버튼 확인
def check_buttons(pos):
    global start, start_ticks

    if start : # 게임이 시작했다면
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()

def check_number_buttons(pos):
    global hidden, start, curr_level

    for button in number_buttons :
        if button.collidepoint(pos):
            if button == number_buttons[0] : # 올바른 숫자 클릭
                del number_buttons[0]
                if not hidden :
                    hidden = True
            else: # 잘못된 숫자 클릭
                game_over()
            break
    # 모든 숫자를 다 맞췄을 시 다음 레벨 전환
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# 게임 종료 처리
def game_over():
    global running

    running = False
    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=((screen_width/2), screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

# 초기화
pygame.init()
screen_width = 1280 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory_Test Game")
game_font = pygame.font.Font(None, 120) # 폰트 정의

# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# 색 지정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = [] # 플레이어가 눌러야 하는 버튼들
curr_level = 1 # 현재 레벨
display_time = None # 숫자를 보여주는 시간
start_ticks = None # 시간 계산(현재 시간 정보 저장)

# 시작 여부 지정
start = False
# 숫자 숨김 여부
hidden = False

# 게임 시작 전 게임 설정 함수 수행
setup(curr_level)

# 게임 루프
running = True

while running:
    click_pos = None

    # 이벤트 루프
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가
        if event.type == pygame.QUIT: # 만약 창이 닫히는 이벤트라면
            running = False          # 게임이 더이상 실행중이 아님
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos() # 마우스 클릭 좌표 값 저장

    # 화면 전체 검은색 칠해주기
    screen.fill(BLACK)

    if start:
        display_game_screen()
    else:
        display_start_screen()

    # 사용자가 클릭한 좌표값이 존재할 경우
    if click_pos:
        check_buttons(click_pos)

    # 화면 업데이트
    pygame.display.update()

# 5초 정도 딜레이
pygame.time.delay(5000)

# 게임 종료
pygame.quit()