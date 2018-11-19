import os

maxlen = 50

def process_dataset(data_dir, dataset):
    node_set = set()
    filename = os.path.join(data_dir, dataset + '.txt')
    with open(filename, 'r') as f:
        for line in f:
            query, cascade = line.strip().split(' ', 1)
            sequence = [query] + cascade.split(' ')[::2]
            if maxlen is not None:
                sequence = sequence[:maxlen]
            node_set.update(sequence)
    return node_set

def preprocess_dataset(data_dir):
    train_nodes = process_dataset(data_dir, 'train')
    test_nodes = process_dataset(data_dir, 'test')
    seen_nodes = train_nodes | test_nodes

    print(('%d seen nodes.' % len(seen_nodes)))

    filename = os.path.join(data_dir, 'seen_nodes.txt')
    with open(filename, 'w') as f:
        for v in seen_nodes:
            f.write('%s\n' % v)

    graph_file = os.path.join(data_dir, 'graph.txt')
    output_file = os.path.join(data_dir, 'subgraph.txt')
    edge_set = set()
    with open(graph_file, 'r') as f, open(output_file, 'w') as fo:
        next(f)
        for line in f:
            u, v = line.strip().split()
            if u in seen_nodes and v in seen_nodes:
                if (u, v) not in edge_set:
                    fo.write('%s %s\n' % (u, v))
                    edge_set.add((u, v))

if __name__ == "__main__":
    # process all
    preprocess_dataset('data/twitter')
    preprocess_dataset('data/digg')
    preprocess_dataset('data/memes')
