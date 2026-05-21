#include <iostream>
#include <vector>
using namespace std;

void insertionSort(vector<int>& massive) {
	int n = massive.size();
	for (int i = 1; i < n; i++) {
		int current = massive[i];
		int j = i - 1;
		while (j >= 0 && massive[j] > current) {
			massive[j + 1] = massive[j];
			j = j - 1;
		}
		massive[j + 1] = current;
	}
}

int main() {
	int n;
	if (!(cin >> n)) return 0;
	vector<int> massive(n);
	for (int i = 0; i < n; i++) {
		cin >> massive[i];
	}
	insertionSort(massive);
	for (int i = 0; i < n; i++) {
		cout << massive[i] << " ";
	}
	cout << endl;
	return 0;
}
