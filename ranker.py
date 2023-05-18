import sys
import matplotlib.pyplot as plt

# Funkcja do wczytywania danych z pliku tekstowego
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Wczytanie liczby wierszy macierzy danych M i liczby kolumn macierzy danych N
    M = int(lines[0])
    N = int(lines[1])

    # Inicjalizacja listy kryteriów
    criteria = []

    # Wczytanie opisów kryteriów
    for i in range(2, 2 + N):
        line = lines[i].split()
        criterion_type = line[0]
        criterion_id = line[1]
        criterion_weight = float(line[2])
        criterion_points = []
        for j in range(3, len(line)):
            point = tuple(map(float, line[j].strip('()').split(',')))
            criterion_points.append(point)
        criteria.append((criterion_type, criterion_id, criterion_weight, criterion_points))

    # Inicjalizacja macierzy wariantów
    variants = []

    # Wczytanie opisów wariantów
    for i in range(2 + N, len(lines)):
        line = lines[i].split()
        variant_id = line[0]
        variant_values = list(map(float, line[1:]))
        variants.append((variant_id, variant_values))

    return M, N, criteria, variants

# Funkcja do obliczania użyteczności dla danego kryterium i wartości
def calculate_criterion_utility(criterion_points, value):
    for i in range(len(criterion_points) - 1):
        x1, y1 = criterion_points[i]
        x2, y2 = criterion_points[i + 1]
        if x1 <= value <= x2:
            return y1 + ((y2 - y1) / (x2 - x1)) * (value - x1)

    return criterion_points[-1][1]

# Funkcja do obliczania użyteczności dla danego wariantu
def calculate_utility(criteria, variant_values):
    utilities = []

    for criterion in criteria:
        criterion_type, _, criterion_weight, criterion_points = criterion
        criterion_value = variant_values[criteria.index(criterion)]
        criterion_utility = calculate_criterion_utility(criterion_points, criterion_value)
        utilities.append(criterion_weight * criterion_utility)

    return utilities

# Funkcja do obliczania użyteczności globalnej dla danego wariantu
def calculate_global_utility(criteria, variant_values):
    utilities = calculate_utility(criteria, variant_values)
    global_utility = sum(utilities)
    return global_utility

# Funkcja do generowania i wyświetlania ranking wariantów
# Funkcja do generowania i wyświetlania ranking wariantów
def generate_ranking(M, N, criteria, variants):
    ranking = []

    for variant in variants:
        variant_id, variant_values = variant
        global_utility = calculate_global_utility(criteria, variant_values)
        ranking.append((variant_id, global_utility))

    ranking = sorted(ranking, key=lambda x: x[1], reverse=True) # Sortowanie w kolejności malejącej

    current_rank = 1
    current_utility = ranking[0][1]

    for rank, (variant_id, global_utility) in enumerate(ranking, start=1):
        if global_utility < current_utility:
            current_rank = rank
            current_utility = global_utility
        print(f'Rank {current_rank}: Variant {variant_id}, Global Utility: {global_utility:.3f}')

    # Wygenerowanie i wyświetlenie wykresów użyteczności dla poszczególnych kryteriów
    num_criteria = len(criteria)
    num_rows = int(num_criteria / 2) + num_criteria % 2
    num_cols = 2

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10, 10))
    fig.tight_layout(pad=3.0)

    for i, criterion in enumerate(criteria):
        criterion_type, criterion_id, _, criterion_points = criterion
        row = int(i / num_cols)
        col = i % num_cols
        ax = axs[row, col]

        x_values = [point[0] for point in criterion_points]
        y_values = [point[1] for point in criterion_points]
        ax.plot(x_values, y_values)
        ax.set_xlabel('Domain')
        ax.set_ylabel('Utility')
        ax.set_title(f'Utility Graph for Criterion {criterion_id}')

    plt.show()


# Wczytanie nazwy pliku tekstowego z danymi jako argument wywołania programu
if len(sys.argv) != 2:
    print('Usage: python program.py input_file.txt')
    sys.exit(1)

input_file_path = sys.argv[1]

# Wczytanie danych z pliku
M, N, criteria, variants = read_input_file(input_file_path)

# Wygenerowanie i wyświetlenie ranking wariantów
generate_ranking(M, N, criteria, variants)
