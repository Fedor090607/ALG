#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int partition(vector<int>& massive, int low, int high) {
	int pivot = massive[high];
	int i = (low - 1);
	for (int j = low; j <= high - 1; j++) {
		if (massive[j] < pivot) {
			i++;
			swap(massive[i], massive[j]);
		}
	}
	swap(massive[i + 1], massive[high]);
	return (i + 1);
}
void quickSort(vector<int>& massive, int low, int high) {
	if (low < high) {
		int pi = partition(massive, low, high);
		quickSort(massive, low, pi - 1);
		quickSort(massive, pi + 1, high);
	}
}
int main() {
	int n;
	if (!(cin >> n)) return 0;
	vector<int> massive(n);
	for (int i = 0; i < n; i++) {
		cin >> massive[i];
	}
	if (n > 0) {
		quickSort(massive, 0, n - 1);
	}
	for (int i = 0; i < n; i++) {
		cout << massive[i] << " ";
	}
	cout << endl;
	return 0;
}
