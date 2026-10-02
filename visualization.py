import matplotlib.pyplot as plt


def draw_map(cities, map_size):
    plt.figure(figsize=(20, 20))
    plt.tick_params(axis="both", labelsize=4)

    plt.xlim(0, map_size)
    plt.ylim(0, map_size)

    plt.grid(True)
    plt.xticks(range(0, map_size + 1, 1))
    plt.yticks(range(0, map_size + 1, 1))

    x_coords = [c.x for c in cities]
    y_coords = [c.y for c in cities]

    # Рисуем точки
    plt.scatter(x_coords, y_coords, color="red", marker="o", s=200)

    for i in range(len(cities)):
        for j in range(len(cities)):
            plt.plot([cities[i].x, cities[j].x],
                     [cities[i].y, cities[j].y], color="blue", linewidth=0.5)

        # Аннотация для каждого города
        plt.annotate(
            cities[i].name,  # Имя города
            (cities[i].x, cities[i].y),  # Координаты города
            fontsize=30  # Размер шрифта
        )

    plt.show()
