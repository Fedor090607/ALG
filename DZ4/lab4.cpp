#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <iomanip>
using namespace std;

int partition(vector<int>& a, int low, int high) {
    int pivot = a[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; ++j) {
        if (a[j] <= pivot) {
            ++i;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[high]);
    return i + 1;
}

void quickSort(vector<int>& a, int low, int high) {
    if (low < high) {
        int p = partition(a, low, high);
        quickSort(a, low, p - 1);
        quickSort(a, p + 1, high);
    }
}

void parallelQuickSort(vector<int>& a, int low, int high, int threads) {
    if (threads <= 1) {
        quickSort(a, low, high);
        return;
    }
    int p = partition(a, low, high);
    thread leftThread(parallelQuickSort, ref(a), low, p - 1, threads / 2);
    parallelQuickSort(a, p + 1, high, threads - threads / 2);
    leftThread.join();
}

int main() {
    setlocale(LC_ALL, "Russian");
    vector<int> sizes = { 100, 1000, 10000, 20000, 30000, 40000, 50000 };
    vector<int> ths = { 1, 2, 4, 8 };
    vector<vector<double>> times(sizes.size(), vector<double>(ths.size()));

    const int W = 14;

    cout << fixed << setprecision(6);

    cout << "Таблица 1 вычисление времени в секундах" << endl;
    cout << left << setw(8) << "Размер" << setw(W) << "БС(сек)";
    for (int t = 1; t < ths.size(); ++t)
        cout << setw(W) << (to_string(ths[t]) + " потока");
    cout << endl;

    for (int i = 0; i < sizes.size(); ++i) {
        int sz = sizes[i];
        vector<int> base(sz);
        for (int j = 0; j < sz; ++j) base[j] = rand() % sz;
        cout << left << setw(8) << sz;
        for (int j = 0; j < ths.size(); ++j) {
            vector<int> arr = base;
            auto start = chrono::high_resolution_clock::now();
            if (ths[j] == 1) quickSort(arr, 0, sz - 1);
            else parallelQuickSort(arr, 0, sz - 1, ths[j]);
            auto end = chrono::high_resolution_clock::now();
            chrono::duration<double> diff = end - start;
            times[i][j] = diff.count();
            cout << setw(W) << times[i][j];
        }
        cout << endl;
    }

    cout << "\nТаблица 2 коэффиценты ускорений" << endl;
    cout << left << setw(8) << "Размер"
        << setw(W) << "Ускор.2"
        << setw(W) << "Ускор.4"
        << setw(W) << "Ускор.8" << endl;

    for (int i = 0; i < sizes.size(); ++i) {
        double seq = times[i][0];
        cout << left << setw(8) << sizes[i];
        for (int j = 1; j < ths.size(); ++j) {
            double par = times[i][j];
            double sp = (par > 0) ? seq / par : 0.0;
            cout << setw(W) << sp;
        }
        cout << endl;
    }
    return 0;
}
