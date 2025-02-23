import networkx as nx
import pandas as pd


def build_graph():
    G = nx.DiGraph()

    edges = [
        ("T1", "S1", 25),
        ("T1", "S2", 20),
        ("T1", "S3", 15),
        ("T2", "S3", 15),
        ("T2", "S4", 30),
        ("T2", "S2", 10),
        ("S1", "M1", 15),
        ("S1", "M2", 10),
        ("S1", "M3", 20),
        ("S2", "M4", 15),
        ("S2", "M5", 10),
        ("S2", "M6", 25),
        ("S3", "M7", 20),
        ("S3", "M8", 15),
        ("S3", "M9", 10),
        ("S4", "M10", 20),
        ("S4", "M11", 10),
        ("S4", "M12", 15),
        ("S4", "M13", 5),
        ("S4", "M14", 10),
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    G.add_edge("Source", "T1", capacity=float("inf"))
    G.add_edge("Source", "T2", capacity=float("inf"))
    for m in [
        "M1",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "M7",
        "M8",
        "M9",
        "M10",
        "M11",
        "M12",
        "M13",
        "M14",
    ]:
        G.add_edge(m, "Sink", capacity=float("inf"))

    return G


def compute_max_flow(G):
    flow_value, flow_dict = nx.maximum_flow(G, "Source", "Sink")
    return flow_value, flow_dict


def extract_terminal_flows(flow_dict):
    terminal_flows = []
    for terminal in ["T1", "T2"]:
        for store, flow in flow_dict[terminal].items():
            if flow > 0:
                terminal_flows.append([terminal, store, flow])
    return pd.DataFrame(
        terminal_flows, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"]
    )


def analyze_results(flow_dict):
    print("\nАНАЛІЗ РЕЗУЛЬТАТІВ:")
    total_flows = {
        terminal: sum(flow_dict[terminal].values()) for terminal in ["T1", "T2"]
    }
    max_terminal = max(total_flows, key=total_flows.get)
    print(
        f"Найбільший потік йде через {max_terminal} ({total_flows[max_terminal]} одиниць)"
    )

    min_capacity = min(
        (cap for u, v, cap in G.edges(data="capacity") if cap != float("inf")),
        default=0,
    )
    print(
        f"Маршрути з найменшою пропускною здатністю мають {min_capacity} одиниць, що може бути вузьким місцем."
    )

    store_flows = {
        store: sum(flow_dict[store].values())
        for store in G.nodes
        if store.startswith("M")
    }
    min_store = min(store_flows, key=store_flows.get)
    print(
        f"Магазин, який отримав найменше товарів: {min_store} ({store_flows[min_store]} одиниць). Можливо, варто збільшити постачання."
    )


if __name__ == "__main__":
    G = build_graph()
    max_flow, flow_dict = compute_max_flow(G)
    print(f"Максимальний потік: {max_flow}")
    df_results = extract_terminal_flows(flow_dict)
    print(df_results)
    analyze_results(flow_dict)
