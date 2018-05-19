#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_NODE 4000000

struct GraphEdge {
    int to, relation;
    double weight;
    int direction;
};

struct GraphEdgeSet {
    struct GraphEdge *edges;
    int total;
};

struct Edge {
    int s, o, p;
};
struct Path {
    struct Edge *edges;
    int length;
};

void build_path(
    struct Path *path, int S, int T, struct GraphEdgeSet* graph,
    int *que, int *dis, double* dis_w, int *from_n, struct GraphEdge **from_r,
    int *forbidden
) {

    int head = 0, tail = 1;
    int sta, i;
    que[head] = S;
    dis[S] = 0;
    dis_w[S] = 0.0;

    while (head < tail) {
        sta = que[head++];
        if (sta == T)
            break;

        for (i = 0; i < graph[sta].total; i++) {
            if (forbidden[graph[sta].edges[i].to] == 1)
                continue;
            if (dis[graph[sta].edges[i].to] > dis[sta] + 1) {
                dis[graph[sta].edges[i].to] = dis[sta] + 1;
                dis_w[graph[sta].edges[i].to] = dis_w[sta] + graph[sta].edges[i].weight;
                from_n[graph[sta].edges[i].to] = sta;
                from_r[graph[sta].edges[i].to] = &graph[sta].edges[i];
                que[tail++] = graph[sta].edges[i].to;
            }

            else if (dis[graph[sta].edges[i].to] == dis[sta] + 1 && 
                    dis_w[graph[sta].edges[i].to] < dis_w[sta] + graph[sta].edges[i].weight) {

                dis_w[graph[sta].edges[i].to] = dis_w[sta] + graph[sta].edges[i].weight;
                from_n[graph[sta].edges[i].to] = sta;
                from_r[graph[sta].edges[i].to] = &graph[sta].edges[i];
            }
            
        }

    }


    if (dis[T] == MAX_NODE + 1) {
        path -> edges = NULL;
        path -> length = 0;
        return;
    }

    for (i = 0; i < tail; i++)
        dis[que[i]] = MAX_NODE + 1;

    path -> length = 0;
    for (i = T; i != S; i = from_n[i])
        path -> length++;


    path -> edges = (struct Edge *)malloc(path -> length * sizeof(struct Edge));

    int counter = path -> length - 1;
    for (i = T; i != S; i = from_n[i]) {
        struct GraphEdge *e = from_r[i];
        path -> edges[counter].p = e -> relation;
        if (e -> direction == 0) {
            path -> edges[counter].s = from_n[i];
            path -> edges[counter].o = i;
        }
        else {
            path -> edges[counter].s = i;
            path -> edges[counter].o = from_n[i];
        }
        counter--;
    }

}

struct Path *find(int* entities, int n, struct GraphEdgeSet* graph) {

    struct Path *pattern = (struct Path *)malloc(n * (n - 1) / 2 * sizeof(struct Path));
    int *que = (int *)malloc(MAX_NODE * sizeof(int));
    int *dis = (int *)malloc(MAX_NODE * sizeof(int));
    double *dis_w = (double *)malloc(MAX_NODE * sizeof(double));
    int *from_n = (int *)malloc(MAX_NODE * sizeof(int));
    struct GraphEdge **from_r = (struct GraphEdge **)malloc(MAX_NODE * sizeof(struct GraphEdge *));

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

            build_path(&pattern[counter], entities[i], entities[j], graph, que, dis, dis_w, from_n, from_r, forbidden);
            counter++;

            for (k = 0; k < n; k++)
                if (k != i && k != j)
                    forbidden[entities[k]] = 0;

        }

    free(que);
    free(dis);
    free(dis_w);
    free(from_n);
    free(from_r);

    return pattern;
}
