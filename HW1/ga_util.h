#include<iostream>
#include<cmath>
#include<cstdlib>   // 亂數相關函數
#include<ctime>     // 時間相關函數
#include<vector>
#include<climits>
#include <numeric> 
#include <bits/stdc++.h>
#include<iomanip>
using namespace std;

float find_sum(vector<float> a){
    return std::accumulate(a.begin(), a.end(), 0.0);
}
void find_range(vector<float> a, string tar){
    cout<<"|"<<tar<<" range ";
    double max = *max_element(a.begin(), a.end());
    double min = *min_element(a.begin(), a.end());
    cout<<"(min, max) | ("<<setprecision(4)<<min<<", "<<max<<")|\n";
}


