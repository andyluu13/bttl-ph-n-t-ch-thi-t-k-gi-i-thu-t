import pygame
import random
import math

# Khởi tạo Pygame
pygame.init()

class DrawInformation:
    """
    Lớp lưu trữ tất cả thông tin quan trọng cho việc vẽ và trạng thái
    """
    # Định nghĩa màu sắc
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

    # Các màu nền cho thanh (bars)
    GRADIENTS = [
        (128, 128, 128),  # Xám
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Phông chữ
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # Đệm (padding)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Thiết lập cửa sổ Pygame
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        """
        Thiết lập danh sách và tính toán chiều rộng, chiều cao của mỗi thanh
        """
        self.list = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # Tính toán chiều rộng của mỗi thanh
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        
        # Tính toán chiều cao của mỗi thanh dựa trên tỷ lệ
        self.block_height_unit = (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        
        # Điểm bắt đầu vẽ
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    """
    Hàm vẽ chính - vẽ mọi thứ lên màn hình
    """
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Hiển thị tên thuật toán và thứ tự
    title_text = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title_text, (draw_info.width / 2 - title_text.get_width() / 2, 5))

    # Hiển thị điều khiển
    controls_text = draw_info.FONT.render(
        "R - Reset | SPACE - Start/Pause | A - Ascending | D - Descending", 1, draw_info.BLACK
    )
    draw_info.window.blit(controls_text, (draw_info.width / 2 - controls_text.get_width() / 2, 45))

    sorting_controls_text = draw_info.FONT.render(
        "B - Bubble Sort | Q - Quick Sort | M - Merge Sort", 1, draw_info.BLACK
    )
    draw_info.window.blit(sorting_controls_text, (draw_info.width / 2 - sorting_controls_text.get_width() / 2, 75))

    # Vẽ danh sách các thanh
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    """
    Vẽ các thanh đại diện cho danh sách
    color_positions là một dict để tô màu các thanh cụ thể
    """
    lst = draw_info.list

    if clear_bg:
        # Xóa chỉ khu vực vẽ danh sách
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Vẽ từng thanh
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        
        # Tính toán chiều cao
        height = (val - draw_info.min_val) * draw_info.block_height_unit
        
        # y là đỉnh của thanh (Pygame vẽ từ trên xuống)
        y = draw_info.height - height

        # Chọn màu
        color = draw_info.GRADIENTS[i % 3]  # Màu mặc định
        if i in color_positions:
            color = color_positions[i]  # Màu đặc biệt (so sánh, hoán đổi)

        # Vẽ hình chữ nhật
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    """
    Tạo một danh sách ngẫu nhiên
    """
    return [random.randint(min_val, max_val) for _ in range(n)]

#
# CÁC THUẬT TOÁN SẮP XẾP
# Các hàm này là 'generators' (sử dụng 'yield') để chúng có thể tạm dừng 
# và cho phép Pygame vẽ lại màn hình sau mỗi bước.
#

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.list
    n = len(lst)

    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            # Tô màu 2 phần tử đang so sánh
            draw_info.color_positions = {j: draw_info.RED, j + 1: draw_info.RED}
            draw_list(draw_info, draw_info.color_positions, True)
            yield True  # Tạm dừng để vẽ

            condition = (lst[j] > lst[j + 1]) if ascending else (lst[j] < lst[j + 1])
            
            if condition:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True
                # Tô màu 2 phần tử vừa hoán đổi
                draw_info.color_positions = {j: draw_info.GREEN, j + 1: draw_info.GREEN}
                draw_list(draw_info, draw_info.color_positions, True)
                yield True  # Tạm dừng để vẽ

        # Tô màu phần tử đã ở đúng vị trí
        draw_info.color_positions[n - i - 1] = draw_info.GREEN
        
        if not swapped:
            break

    # Tô màu toàn bộ danh sách khi hoàn thành
    draw_info.color_positions = {i: draw_info.GREEN for i in range(n)}
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

def quick_sort(draw_info, ascending=True):
    lst = draw_info.list
    
    # Sử dụng 'yield from' để ủy quyền cho hàm đệ quy
    yield from quick_sort_recursive(draw_info, 0, len(lst) - 1, ascending)
    
    # Tô màu toàn bộ danh sách khi hoàn thành
    draw_info.color_positions = {i: draw_info.GREEN for i in range(len(lst))}
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

def quick_sort_recursive(draw_info, low, high, ascending):
    if low < high:
        # 'partition' cũng là một generator
        pivot_index_generator = partition(draw_info, low, high, ascending)
        pivot_index = yield from pivot_index_generator
        
        yield from quick_sort_recursive(draw_info, low, pivot_index - 1, ascending)
        yield from quick_sort_recursive(draw_info, pivot_index + 1, high, ascending)

def partition(draw_info, low, high, ascending):
    lst = draw_info.list
    pivot = lst[high]
    i = low - 1  # Chỉ số của phần tử nhỏ hơn (hoặc lớn hơn)

    # Tô màu pivot
    draw_info.color_positions = {high: draw_info.BLUE}
    for k in range(low, high):
        draw_info.color_positions[k] = draw_info.GREY
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

    for j in range(low, high):
        # Tô màu phần tử đang xét
        draw_info.color_positions[j] = draw_info.RED
        draw_list(draw_info, draw_info.color_positions, True)
        yield True

        condition = (lst[j] < pivot) if ascending else (lst[j] > pivot)
        
        if condition:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            # Tô màu 2 phần tử vừa hoán đổi
            draw_info.color_positions[i] = draw_info.GREEN
            draw_info.color_positions[j] = draw_info.GREEN
            draw_list(draw_info, draw_info.color_positions, True)
            yield True
        
        # Đặt lại màu
        draw_info.color_positions[j] = draw_info.GREY
        if i >= low:
            draw_info.color_positions[i] = draw_info.GREEN

    # Đưa pivot về đúng vị trí
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    pivot_index = i + 1
    
    # Tô màu vị trí cuối cùng của pivot
    draw_info.color_positions = {k: draw_info.GREY for k in range(low, high + 1)}
    draw_info.color_positions[pivot_index] = draw_info.GREEN
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

    # Trả về chỉ số của pivot
    return pivot_index

def merge_sort(draw_info, ascending=True):
    yield from merge_sort_recursive(draw_info, 0, len(draw_info.list) - 1, ascending)
    
    # Tô màu toàn bộ danh sách khi hoàn thành
    draw_info.color_positions = {i: draw_info.GREEN for i in range(len(draw_info.list))}
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

def merge_sort_recursive(draw_info, left, right, ascending):
    if left < right:
        mid = (left + right) // 2
        yield from merge_sort_recursive(draw_info, left, mid, ascending)
        yield from merge_sort_recursive(draw_info, mid + 1, right, ascending)
        yield from merge(draw_info, left, mid, right, ascending)

def merge(draw_info, left, mid, right, ascending):
    lst = draw_info.list
    
    # Tô màu 2 mảng con đang được trộn
    for i in range(left, right + 1):
        draw_info.color_positions[i] = draw_info.BLUE
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

    left_copy = lst[left : mid + 1]
    right_copy = lst[mid + 1 : right + 1]

    i = 0  # con trỏ cho mảng con trái
    j = 0  # con trỏ cho mảng con phải
    k = left # con trỏ cho mảng chính

    while i < len(left_copy) and j < len(right_copy):
        # Tô màu 2 phần tử đang so sánh
        draw_info.color_positions[k] = draw_info.RED
        draw_list(draw_info, draw_info.color_positions, True)
        yield True

        condition = (left_copy[i] <= right_copy[j]) if ascending else (left_copy[i] >= right_copy[j])

        if condition:
            lst[k] = left_copy[i]
            i += 1
        else:
            lst[k] = right_copy[j]
            j += 1
        
        # Tô màu phần tử đã được đặt đúng vị trí
        draw_info.color_positions[k] = draw_info.GREEN
        k += 1
        draw_list(draw_info, draw_info.color_positions, True)
        yield True

    # Sao chép phần còn lại của mảng con trái (nếu có)
    while i < len(left_copy):
        lst[k] = left_copy[i]
        draw_info.color_positions[k] = draw_info.GREEN
        i += 1
        k += 1
        draw_list(draw_info, draw_info.color_positions, True)
        yield True

    # Sao chép phần còn lại của mảng con phải (nếu có)
    while j < len(right_copy):
        lst[k] = right_copy[j]
        draw_info.color_positions[k] = draw_info.GREEN
        j += 1
        k += 1
        draw_list(draw_info, draw_info.color_positions, True)
        yield True
    
    # Tô màu xanh lá cho toàn bộ phần đã trộn
    for i in range(left, right + 1):
        draw_info.color_positions[i] = draw_info.GREEN
    draw_list(draw_info, draw_info.color_positions, True)
    yield True

#
# HÀM MAIN
#
def main():
    run = True
    clock = pygame.time.Clock()

    # Cấu hình ban đầu
    n = 50
    min_val = 1
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(900, 600, lst)
    
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        # Điều chỉnh tốc độ (FPS) - Giảm số này để chạy chậm hơn
        clock.tick(60)

        if sorting:
            try:
                # Chạy bước tiếp theo của thuật toán
                next(sorting_algorithm_generator)
            except StopIteration:
                # Thuật toán đã chạy xong
                sorting = False
        else:
            # Vẽ trạng thái hiện tại khi không sắp xếp
            draw(draw_info, sorting_algo_name, ascending)

        # Xử lý sự kiện (nhấn phím, v.v.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # R - Reset
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                draw_info.color_positions = {}
            
            # SPACE - Start/Pause
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                # Tạo một generator mới cho thuật toán được chọn
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_SPACE and sorting:
                sorting = False # Tạm dừng

            # A - Ascending
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            
            # D - Descending
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            # B - Bubble Sort
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            # Q - Quick Sort
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            # M - Merge Sort
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":
    main()