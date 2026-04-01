from pyvis.network import Network

def create_knowledge_graph(entities):
    # --- ADD THIS LINE BELOW ---
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    # ---------------------------

    for item in entities:
        source = item.get("source")
        target = item.get("target")
        relation = item.get("relation")
        
        # Pyvis handles duplicate nodes automatically, but we check to be safe
        if source and target:
            net.add_node(source, label=source, color="#76b900") 
            net.add_node(target, label=target, color="#0071c5") 
            net.add_edge(source, target, title=relation, label=relation)

    output_path = "graph.html"
    net.save_graph(output_path)
    return output_path