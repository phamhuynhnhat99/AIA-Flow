class Flow:

    def __init__(self):
        self.vertices = []
        self.arrows = []


    def update_graph(self, vertices, arrows):
        self.vertices = vertices
        self.arrows = arrows
        self.m = len(self.arrows)
    

    def build_graph(self):
        self.num_prev = [0] * len(self.vertices)
        self.num_next = [0] * len(self.vertices)

        self.head = [-1] * len(self.vertices)
        self.before = [None] * self.m
        self.adj = [None] * self.m

        for i, ar in enumerate(self.arrows):
            u, v = ar[0], ar[1]
            self.num_next[u] += 1
            self.num_prev[v] += 1
            self.adj[i] = v
            self.before[i] = self.head[u]
            self.head[u] = i
    

    def toposort(self):
        
        if not self.vertices:
            return []

        self.build_graph()

        self.end_vertices = [u for u in self.vertices if self.num_next[u] == 0]
        
        topo_queue = []
        for ver in self.vertices:
            if self.num_prev[ver] == 0:
                topo_queue.append(ver)
        
        # toposort
        self.order = []
        b_ind, e_ind = 0, 0
        while b_ind <= e_ind:
            if len(topo_queue) > 0:
                u = topo_queue[0]
                topo_queue = topo_queue[1:]
                e_ind += 1
                self.order.append(u)
                pos = self.head[u]
                while pos != -1:
                    v = self.adj[pos]
                    self.num_prev[v] -= 1
                    if self.num_prev[v] == 0:
                        topo_queue.append(v)
                    pos = self.before[pos]
                b_ind += 1
            else:
                break
        
        if e_ind < len(self.vertices): # This is not a DAG
            self.order = []
            self.end_vertices = []

        # decode
        decode_toposort = [self.decode_vertices[_] for _ in self.order]
        decode_end_vertices = [self.decode_vertices[_] for _ in self.end_vertices]
        
        return decode_toposort

    
    def sub_toposort_from(self, vertex): # Get all vertex's descendants (include vertex)
        if vertex not in self.decode_vertices:
            return []
        
        encode_vertext = self.decode_vertices.index(vertex)
        
        self.build_graph()

        # bfs from vertexend_vertices
        bfs_queue = [encode_vertext]
        b_ind, e_ind = 0, 0
        while b_ind <= e_ind:
            u = bfs_queue[b_ind]
            b_ind += 1
            pos = self.head[u]
            while pos != -1:
                v = self.adj[pos]
                if v not in bfs_queue:
                    bfs_queue.append(v)
                    e_ind += 1
                pos = self.before[pos]

        genealogy_of_vertex = [self.decode_vertices[_] for _ in self.order if _ in bfs_queue]
        
        return genealogy_of_vertex

  
vertices = [1, 4, 5, 8]
arrows = [[1, 5], [5, 4], [8, 4]]
flow = Flow()
flow.update_graph(vertices=vertices, arrows=arrows)
order = flow.toposort()
print(order)