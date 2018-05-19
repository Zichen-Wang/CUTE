struct Node {
    char *str;
    double sim;
};

void swap(struct Node **x, struct Node **y) {
    struct Node *t = *x;
    *x = *y;
    *y = t;
}

void pushup(struct Node** cur_heap, int pos) {
    while (pos > 0) {
        int fa = (pos - 1) / 2;
        if (cur_heap[fa] -> sim > cur_heap[pos] -> sim) {
            swap(&cur_heap[fa], &cur_heap[pos]);
            pos = fa;
        }
        else
            break;
    }
}

void pushdown_top(struct Node** cur_heap, int tot) {
    int pos = 0, left, right;
    while (pos < tot) {
        left = (pos * 2 + 1 < tot) ? (pos * 2 + 1) : -1;
        right = (pos * 2 + 2 < tot) ? (pos * 2 + 2) : -1;
        if (left == -1 && right == -1)
            break;
        else if (left != -1 && right == -1) {
            if (cur_heap[pos] -> sim > cur_heap[left] -> sim) {
                swap(&cur_heap[pos], &cur_heap[left]);
                pos = left;
            }
            else
                break;
        }
        else if (left == -1 && right != -1) {
            if (cur_heap[pos] -> sim > cur_heap[right] -> sim) {
                swap(&cur_heap[pos], &cur_heap[right]);
                pos = right;
            }
            else
                break;
        }
        else {
            if (cur_heap[pos] -> sim < cur_heap[left] -> sim && cur_heap[pos] -> sim < cur_heap[right] -> sim)
                break;
            else if (cur_heap[pos] -> sim < cur_heap[left] -> sim && cur_heap[pos] -> sim > cur_heap[right] -> sim) {
                swap(&cur_heap[pos], &cur_heap[right]);
                pos = right;
            }
            else if (cur_heap[pos] -> sim > cur_heap[left] -> sim && cur_heap[pos] -> sim < cur_heap[right] -> sim) {
                swap(&cur_heap[pos], &cur_heap[left]);
                pos = left;
            }
            else {
                if (cur_heap[left] -> sim < cur_heap[right] -> sim) {
                    swap(&cur_heap[pos], &cur_heap[left]);
                    pos = left;
                }
                else {
                    swap(&cur_heap[pos], &cur_heap[right]);
                    pos = right;
                }
            }
        }
    }
}