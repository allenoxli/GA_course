// #include"ga_util.h"
#include<iostream>
#include<cmath>
#include<cstdlib>   // 亂數相關函數
#include<ctime>     // 時間相關函數
#include<vector>
#include<array>
#include<cstring>
#include<climits>
#include<limits>
#include <tuple>
#include <typeinfo>
#include<algorithm>
#include<random>

using namespace std;

tuple<int, int> pp(){
    return make_tuple(1,3);
}

void tmp(){
     double x1 = 0.87494,
            x2 = 0.81244;
            double interval = 6.10352e-05;

        double left_part = pow(x1*x1 + x2*x2, 0.25),
                right_part = pow(sin(50*pow((x1*x1 + x2*x2), 0.1)), 2.0) + 1;
    cout<<"Ans: "<<left_part * right_part ;
}
float randfloat(float max, float min){
    return (max - min) * rand() / RAND_MAX + min;
}

int main(){


    srand((unsigned)time(NULL));

    for(int i=0;i<10;i++){
        cout<<randfloat(0.0001, 0.0)<<endl;
    }
    /*
    int nrolls = 20000;
    const int nintervals=10; // number of intervals

  std::default_random_engine generator;
  std::uniform_real_distribution<double> distribution(0.0, 1.0);

  int p[nintervals]={};

    for (int i=0; i<nrolls; ++i) {
        double x = distribution(generator);
        double a = (double)rand() / RAND_MAX;
        cout<<x<<endl;
        if(x==1)
            cout<<"========";
    }
*/

}