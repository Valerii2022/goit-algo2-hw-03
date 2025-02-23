import networkx as nx


def build_graph():

    G = nx.DiGraph()

    edges = [
        ("T1", "S1", 10),
        ("T1", "S2", 15),
        ("T2", "S2", 10),
        ("T2", "S3", 10),
        ("S1", "M1", 5),
        ("S1", "M2", 5),
        ("S1", "M3", 5),
        ("S2", "M4", 10),
        ("S2", "M5", 5),
        ("S2", "M6", 5),
        ("S3", "M7", 10),
        ("S3", "M8", 10),
        ("M1", "M14", 5),
        ("M4", "M14", 5),
        ("M7", "M14", 5),
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    return G


def analyze_results(flow_dict, G):
    print("\n🔍 Аналіз результатів:")

    terminal_flows = {}
    for u in G.nodes():
        if u.startswith("T"):
            terminal_flows[u] = sum(flow_dict[u][v] for v in flow_dict[u])

    max_terminal = max(terminal_flows, key=terminal_flows.get, default="Немає потоку")
    print(
        f"Термінал з найбільшим потоком: {max_terminal} ({terminal_flows[max_terminal]} одиниць)"
    )

    min_capacity_edges = sorted(
        [(u, v, d["capacity"]) for u, v, d in G.edges(data=True)], key=lambda x: x[2]
    )[:3]
    print("🔻 Вузькі місця в мережі:")
    for u, v, capacity in min_capacity_edges:
        print(f"  {u} -> {v}: {capacity} одиниць")

    store_flows = {
        v: sum(flow_dict[u][v] for u in flow_dict if v in flow_dict[u])
        for v in G.nodes()
        if v.startswith("M")
    }
    min_store = min(store_flows, key=store_flows.get, default="Немає потоку")
    print(
        f"Магазин з найменшим потоком: {min_store} ({store_flows[min_store]} одиниць)"
    )


def main():
    G = build_graph()
    source, sink = "T1", "M14"

    max_flow_value, flow_dict = nx.maximum_flow(G, source, sink)

    print(f"Максимальний потік з {source} до {sink}: {max_flow_value}")

    print("Термінал  Магазин  Фактичний Потік")
    for u, flows in flow_dict.items():
        for v, flow in flows.items():
            if flow > 0:
                print(f" {u:>6}  -> {v:>6}     {flow}")

    analyze_results(flow_dict, G)


if __name__ == "__main__":
    main()
