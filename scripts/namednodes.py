import json

def replace_blank_nodes(jsonld_data):
    # Create a dictionary to store elements with their @id as key
    element_dict = {}
    for element in jsonld_data:
        if '@id' in element:
            element_dict[element['@id']] = element
    
    # Function to recursively replace blank nodes
    def replace_blank_node(node, visited=None):
        if visited is None:
            visited = set()
        
        if isinstance(node, list):
            return [replace_blank_node(item, visited) for item in node]
        elif isinstance(node, dict):
            node_id = node.get('@id')
            if node_id and node_id in element_dict and node_id.startswith('_:'):
                if node_id in visited:
                    return node  # Circular reference detected, return node as-is
                visited.add(node_id)
                return replace_blank_node(element_dict[node_id], visited)
            return {key: replace_blank_node(value, visited) for key, value in node.items()}
        else:
            return node
    
    # Replace all blank nodes in the JSON-LD data
    replaced_data = [replace_blank_node(element) for element in jsonld_data]
    
    return replaced_data

# Example usage
if __name__ == "__main__":
    input_file_path = '../resources/Datavoorbeelden/datavoorbeeld_expanded.jsonld'
    output_file_path = '../resources/Datavoorbeelden/output_namednodes.jsonld'
    
    # Read JSON-LD data from file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        jsonld_data = json.load(f)
    
    # Replace blank nodes
    replaced_data = replace_blank_nodes(jsonld_data)
    
    # Write the output JSON-LD data to a new file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(replaced_data, f, indent=2, ensure_ascii=False)

    print(f"Output written to {output_file_path}")

    
    
