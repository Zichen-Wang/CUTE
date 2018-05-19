#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_NODE 2000000

struct GraphEdge {
    int to, direction;
};

struct GraphEdgeSet {
    struct GraphEdge *edges;
    int total;
};

struct Path {
    int *directions, length;
};

void build_path(
    struct Path *path, int S, int T, struct GraphEdgeSet* graph,
    int *que, int *dis, int *from_n, int *from_d,
    int *forbidden
) {

    int head = 0, tail = 1;
    int sta, i;
    que[head] = S;
    dis[S] = 0;

    while (head < tail) {
        sta = que[head++];
        if (sta == T)
            break;

        for (i = 0; i < graph[sta].total; i++) {
            if (forbidden[graph[sta].edges[i].to] == 1)
                continue;

            if (dis[graph[sta].edges[i].to] > dis[sta] + 1) {
                dis[graph[sta].edges[i].to] = dis[sta] + 1;
                from_n[graph[sta].edges[i].to] = sta;
                from_d[graph[sta].edges[i].to] = graph[sta].edges[i].direction;
                que[tail++] = graph[sta].edges[i].to;
            }
            
        }

    }


    if (dis[T] == MAX_NODE + 1) {
        path -> directions = NULL;
        path -> length = 0;
        return;
    }

    for (i = 0; i < tail; i++)
        dis[que[i]] = MAX_NODE + 1;

    path -> length = 0;
    for (i = T; i != S; i = from_n[i])
        path -> length++;


    path -> directions = (int *)malloc(path -> length * sizeof(int));

    int counter = path -> length - 1;
    for (i = T; i != S; i = from_n[i]) {
        path -> directions[counter] = from_d[i];
        counter--;
    }

}

struct Path *find(int* entities, int n, struct GraphEdgeSet* graph) {

    struct Path *pattern = (struct Path *)malloc(n * (n - 1) / 2 * sizeof(struct Path));
    int *que = (int *)malloc(MAX_NODE * sizeof(int));
    int *dis = (int *)malloc(MAX_NODE * sizeof(int));
    int *from_n = (int *)malloc(MAX_NODE * sizeof(int));
    int *from_d = (int *)malloc(MAX_NODE * sizeof(int));

    int *forbidden = (int *)malloc(MAX_NODE * sizeof(int));
    int i, j, k;

    for (i = 0; i < MAX_NODE; i++) {
        dis[i] = MAX_NODE + 1;
        forbidden[i] = 0;
    }

    int counter = 0;
    for (i = 0; i < n; i++)
        for (j = i + 1; j < n; j++) {

            for (k = 0; k < n; k++)
                if (k != i && k != j)
                    forbidden[entities[k]] = 1;

            build_path(&pattern[counter], entities[i], entities[j], graph, que, dis, from_n, from_d, forbidden);
            counter++;

            for (k = 0; k < n; k++)
                if (k != i && k != j)
                    forbidden[entities[k]] = 0;

        }

    free(que);
    free(dis);
    free(from_n);
    free(from_d);

    return pattern;
}
