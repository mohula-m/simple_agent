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

    # Drawing points(cities)
    plt.scatter(x_coords, y_coords, color="red", marker="o", s=200)

    for i in range(len(cities)):
        for j in range(len(cities)):
            plt.plot([cities[i].x, cities[j].x],
                     [cities[i].y, cities[j].y], color="blue", linewidth=0.5)

        # Anotate every city
        plt.annotate(
            cities[i].name,  # City name
            (cities[i].x, cities[i].y),  # City coordinates
            fontsize=30  # Font size
        )

    plt.show()


def draw_route(cities, route, bad_routes, map_size, title):
    plt.figure(figsize=(9, 9))
    plt.title(title)
    plt.xlim(-5, map_size + 5)
    plt.ylim(-5, map_size + 5)
    plt.grid(True, alpha=0.3)

    # Bad routws(i was not drawing good routes, because it doessent give any sense)
    # Every city is connected to each other, that's why it's making sense only to connect cities
    # with bad roads between them
    for road in bad_routes:
        a = road[0]
        b = road[1]
        plt.plot([cities[a].x, cities[b].x],
                 [cities[a].y, cities[b].y], color="red", linestyle="--", linewidth=1, alpha=0.4)

    # Our route
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        plt.plot([cities[a].x, cities[b].x],
                 [cities[a].y, cities[b].y], color="blue", linewidth=2.5)

        # trip number in the middle of the segment, to show the order
        middle_x = (cities[a].x + cities[b].x) / 2
        middle_y = (cities[a].y + cities[b].y) / 2
        plt.annotate(str(i + 1), (middle_x, middle_y), fontsize=8, color="blue")

    # Cities
    for city in cities:
        if city.idx == 0:
            plt.scatter(city.x, city.y, color="green", marker="s", s=150, zorder=3)
        else:
            plt.scatter(city.x, city.y, color="black", s=50, zorder=3)
        plt.annotate(f"{city.idx} {city.name}", (city.x, city.y),
                     fontsize=9, xytext=(4, 4), textcoords="offset points")
