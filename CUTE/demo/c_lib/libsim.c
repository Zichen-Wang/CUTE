#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "heap.h"

#define MAX_LINE 4000000
#define MAX_LEN 2000
#define MAX_THREAD 32


struct Input {
    char *given;
    char **all_entity;
    int *all_entity_len;
    int begin, end;
    int top_k;
};


int min(int x, int y) {
    return x < y ? x : y;
}

int max(int x, int y) {
    return x > y ? x : y;
}

int is_equal(char x, char y) {
    if (x == y)
        return 1;
    if ('A' <= x && x <= 'Z')
        x = x - 'A' + 'a';
    if ('A' <= y && y <= 'Z')
        y = y - 'A' + 'a';
    if (x == y)
        return 1;
    if ((x == ' ' && y == '_' ) || (x == '_' && y == ' '))
        return 1;
    return 0;
}

double calc_similarity(
    char* given, unsigned n, int *match_given, char* candidate, unsigned m, int *match_candidate) {

    int i, j;

    int r = max(n, m) / 2 - 1, p = 0, matched = 0, t = 0;
    for (i = 0; i < min(n, m) && p < 4; i++)
        if (is_equal(given[i], candidate[i])) p++;
        else break;

    matched = p;
    for (i = p; i < n; i++)
        for (j = max(p, i - r); j <= min(m - 1, i + r); j++)
            if (!match_candidate[j] && is_equal(given[i], candidate[j])) {
                match_given[i] = match_candidate[j] = 1;
                matched++;
                break;
            }
    double w;
    if (matched == 0) w = 0;
    else {
        for(i = p, j = p; i < n; i++)
            if(match_given[i]) {
                while(j < m && !is_equal(given[i], candidate[j]))
                    j++;
                if(j < m && !is_equal(given[i], candidate[j]))
                    t++;
                j++;
            }

        t >>= 1;
        double ret = (1.0 * matched / n + 1.0 * matched / m + 1.0 * (matched - t) / matched) / 3;
        w = ret + p * 0.1 * (1 - ret);
    }
    return w;
}

void* work(void *ptr) {
    struct Input *data = (struct Input *)ptr;
    int i, j;

    struct Node **res_heap = (struct Node **)malloc((data -> top_k) * sizeof(struct Node *));
    int cnt = 0;
    for (i = 0; i < data -> top_k; i++)
        res_heap[i] = NULL;

    unsigned n = strlen(data -> given), m;

    int *match_given = (int *)malloc(n * sizeof(int));
    int *match_candidate = (int *)malloc(MAX_LEN * sizeof(int));

    for (i = data -> begin; i != data -> end; i++) {
        m = (data -> all_entity_len)[i];

        for (j = 0; j < n; j++)
            match_given[j] = 0;
        for (j = 0; j < m; j++)
            match_candidate[j] = 0;
        double cur_sim = calc_similarity(data -> given, n, match_given, (data -> all_entity)[i], m, match_candidate);
        
        if (cnt < data -> top_k) {
            res_heap[cnt] = (struct Node *)malloc(1 * sizeof(struct Node));
            res_heap[cnt] -> str = (char *)malloc((m + 1) * sizeof(char));
            strcpy(res_heap[cnt] -> str, (data -> all_entity)[i]);
            res_heap[cnt] -> sim = cur_sim;
            pushup(res_heap, cnt);
            cnt++;
        }
        else {
            if (cur_sim > res_heap[0] -> sim) {
                cnt--;
                swap(&res_heap[0], &res_heap[cnt]);
                free(res_heap[cnt] -> str);
                free(res_heap[cnt]);
                pushdown_top(res_heap, cnt);

                res_heap[cnt] = (struct Node *)malloc(1 * sizeof(struct Node));
                res_heap[cnt] -> str = (char *)malloc((m + 1) * sizeof(char));
                strcpy(res_heap[cnt] -> str, (data -> all_entity)[i]);
                res_heap[cnt] -> sim = cur_sim;
                pushup(res_heap, cnt);
                cnt++;
            }
        }
        
    }
    
    free(match_given);
    free(match_candidate);

    pthread_exit((void *)res_heap);
}

struct Node* find(char* given, int tot, char** all_entity, int* all_entity_len, int top_k) {

    int i, j;

    /* read file */
    /*
    char **all_entity = (char **)malloc(MAX_LINE * sizeof(char *));
    int *all_entity_len = (int *)malloc(MAX_LINE * sizeof(int));
    int tot = 0;

    int fd = open(file_path, O_RDONLY);
    struct stat stat;
    fstat(fd, &stat);
    int tot_len = stat.st_size, cur_len = 0;

    // Use mmap to enhance the performance
    char *bufp = (char *)mmap(NULL, tot_len, PROT_READ, MAP_SHARED, fd, 0);
    for (i = 0; i < tot_len; i++) {
        if (*(bufp + i) == '\n') {
            all_entity_len[tot] = cur_len;
            all_entity[tot++] = bufp + i - cur_len;
            cur_len = 0;
        }
        else {
            cur_len++;
        }
    }
    
    close(fd);
    all_entity[tot] = NULL;
    */

    /* end read file */
    
    


    /* thread */
    
    int per_thread_num = tot / MAX_THREAD + (int)(tot % MAX_THREAD != 0);
    
    pthread_t thread[MAX_THREAD];

    struct Input arg[MAX_THREAD];
    void *retVal[MAX_THREAD];

    for (i = 0; i < MAX_THREAD; i++) {
        arg[i].given = given;
        arg[i].all_entity = all_entity;
        arg[i].all_entity_len = all_entity_len;
        arg[i].begin = per_thread_num * i;
        arg[i].end = min(per_thread_num * (i + 1), tot);
        arg[i].top_k = top_k;
        pthread_create(thread + i, NULL, (void *)&work, (void *)(arg + i));
    }


    for (i = 0; i < MAX_THREAD; i++)
        pthread_join(thread[i], retVal + i);
    
    /* end thread */
    


    /* final ans */
    
    struct Node **final_heap = (struct Node **)malloc(top_k * sizeof(struct Node *));
    int cnt = 0;
    for (i = 0; i < top_k; i++)
        final_heap[i] = NULL;

    for (i = 0; i < MAX_THREAD; i++) {
        struct Node **candidate = (struct Node **)retVal[i];
        for (j = 0; j < top_k && candidate[j] != NULL; j++) {
            if (cnt < top_k) {
                final_heap[cnt] = (struct Node *)malloc(1 * sizeof(struct Node));
                final_heap[cnt] -> str = (char *)malloc(MAX_LEN * sizeof(char));
                strcpy(final_heap[cnt] -> str, candidate[j] -> str);
                final_heap[cnt] -> sim = candidate[j] -> sim;
                pushup(final_heap, cnt);
                cnt++;
            }
            else {
                if (candidate[j] -> sim > final_heap[0] -> sim) {
                    cnt--;
                    swap(&final_heap[0], &final_heap[cnt]);
                    free(final_heap[cnt] -> str);
                    free(final_heap[cnt]);
                    pushdown_top(final_heap, cnt);

                    final_heap[cnt] = (struct Node *)malloc(1 * sizeof(struct Node));
                    final_heap[cnt] -> str = (char *)malloc(MAX_LEN * sizeof(char));
                    strcpy(final_heap[cnt] -> str, candidate[j] -> str);
                    final_heap[cnt] -> sim = candidate[j] -> sim;
                    pushup(final_heap, cnt);
                    cnt++;
                }
            }
        }
    }

    struct Node *ans = (struct Node *)malloc(cnt * sizeof(struct Node));

    for (i = cnt - 1; i >= 0; i--) {
        ans[i].str = (char *)malloc(MAX_LEN * sizeof(char));
        strcpy(ans[i].str, final_heap[0] -> str);
        ans[i].sim = final_heap[0] -> sim;

        cnt--;
        swap(&final_heap[0], &final_heap[cnt]);
        free(final_heap[cnt] -> str);
        free(final_heap[cnt]);
        pushdown_top(final_heap, cnt);

    }

    return ans;

}

