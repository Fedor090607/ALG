#include <iostream>
#include <vector>
using namespace std;
void shellSort(vector<int>& arr) {
	int n = arr.size();
	int gap = n / 2;
	while (gap > 0) {
		for (int i = gap; i < n; i++) {
			int temp = arr[i];
			int j = i;
			while (j >= gap && arr[j - gap] > temp) {
				arr[j] = arr[j - gap];
				j = j - gap;
			}
			arr[j] = temp;
		}
		gap = gap / 2;
	}
}
int main() {
	int n;
	if (!(cin >> n)) return 0;
	vector<int> arr(n);
	for (int i = 0; i < n; i++) {
		cin >> arr[i];
	}
	shellSort(arr);
	for (int i = 0; i < n; i++) {
		cout << arr[i] << " ";
	}
	cout << endl;
	return 0;
}
