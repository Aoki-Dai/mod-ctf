/*
 * Triangle Pattern Generator
 *
 * このプログラムは三角形パターンを生成します。
 * しかし、正しく動作していません。
 * デバッグして修正し、正しいパターンを生成してください。
 *
 * 期待される出力は問題文の画像を参照してください。
 */

#include <stdio.h>

int triangle[64][64];

void generate_pattern() {
    // すべて0で初期化
    for(int i = 0; i < 64; i++) {
        for(int j = 0; j < 64; j++) {
            triangle[i][j] = 0;
        }
    }

    // 最初の要素
    triangle[0][0] = 1;

    // パターンを生成
    for(int i = 1; i < 64; i++) {
        triangle[i][0] = 1;  // 左辺は常に1
        triangle[i][i] = 1;  // 右辺は常に1

        for(int j = 1; j < i; j++) {
            triangle[i][j] = (triangle[i-1][j-1] + triangle[i-1][j]) % 2;
        }
    }
}

void print_pattern() {
    printf("Triangle Pattern:\n");
    printf("(*=1, space=0)\n\n");

    for(int i = 0; i < 64; i++) {
        // 左側のスペースで中央揃え
        for(int space = 0; space < 63 - i; space++) {
            printf(" ");
        }

        // パターンを表示
        for(int j = 0; j <= i; j++) {
            if(triangle[i][j] == 1) {
                printf("* ");
            } else {
                printf("  ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int count_stars_in_row(int row) {
    int count = 0;
    // 配列のインデックスは0から始まるため、row-1を使用
    int row_index = row - 1;
    
    // Bounds check
    if (row_index < 0 || row_index >= 64) {
        return 0; 
    }

    for(int j = 0; j <= row_index; j++) {
        if(triangle[row_index][j] == 1) {
            count++;
        }
    }
    return count;
}

int main() {
    printf("=== Triangle Pattern Challenge ===\n\n");

    generate_pattern();
    print_pattern();

    // 32行目と64行目の*の数を数える
    int stars_row32 = count_stars_in_row(32);
    int stars_row64 = count_stars_in_row(64);

    printf("Statistics:\n");
    printf("32行目: %d stars\n", stars_row32);
    printf("64行目: %d stars\n", stars_row64);
    printf("\n");

    // 答えを計算（32行目 × 1000 + 64行目）
    int result = stars_row32 * 1000 + stars_row64;
    printf("Result: %d\n", result);
    printf("Flag: flag{%d}\n", result);

    return 0;
}
