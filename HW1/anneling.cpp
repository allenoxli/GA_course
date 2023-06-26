#include<iostream>
#include<cmath>
#include<cstdlib>   // 亂數相關函數
#include<ctime>     // 時間相關函數
#include<vector>
#include<climits>
#include"ga_util.h"
using namespace std;

struct cell{
    double x1, x2;
    double fitness;
};

class Anneling{
public:
    int max_iter, best_iter=0;
    float min_bound, max_bound;
    float precision, temperature;
    cell cur_node, best_node;   // 目前的 node, 記錄下分數最好的 node
    vector<cell> best_node_list;    // 記錄每一個 iteration 裡面最佳的 cell.
    vector<cell> next_nodes;
    Anneling(int max_iter, float min_bound, float max_bound, float precision, float temperature);
    void initialize();
    void evaluate(cell &node);
    void move();
    cell run(string mode);
    void find_best(string mode);
    void print_info(int iter_interval);
    double randfloat(float min, float max);
    void check_bound(cell &node);
};

Anneling::Anneling(int max_iter, float min_bound, float max_bound, float precision, float temperature){
    this->max_iter = max_iter;
    this->min_bound = min_bound;
    this->max_bound = max_bound;
    this->precision = precision;
    this->temperature = temperature;
}

double Anneling::randfloat(float min, float max){
    return (max - min) * rand() / RAND_MAX + min;
}

void Anneling::initialize(){
    cur_node.x1 = randfloat(min_bound, max_bound);
    cur_node.x2 = randfloat(min_bound, max_bound);
    check_bound(cur_node);
}

void Anneling::evaluate(cell &node){
    double x1 = node.x1, x2 = node.x2;
    double left_part = pow(x1 * x1 + x2 * x2, 0.25),
            right_part = pow(sin(50 * pow((x1 * x1 + x2 * x2), 0.1)), 2.0) + 1;

    node.fitness = left_part * right_part;
}
void Anneling::check_bound(cell &node){
    if(node.x1 < min_bound) node.x1 = min_bound;
    if(node.x1 > max_bound) node.x1 = max_bound;
    if(node.x2 < min_bound) node.x2 = min_bound;
    if(node.x2 > max_bound) node.x2 = max_bound;
}

void Anneling::move(){
    next_nodes.clear();
    for(int i=0;i<30;i++){
        cell node;
        node.x1 = cur_node.x1 + randfloat(-1*precision, precision);
        node.x2 = cur_node.x2 + randfloat(-1*precision, precision);
        check_bound(node);
        evaluate(node);
        next_nodes.push_back(node);
    }
}

void Anneling::find_best(string mode){
    int idx;
    if(mode == "max"){
        double maximum = INT_MIN;
        for(int i=0;i<next_nodes.size();i++){
            if(next_nodes[i].fitness > maximum){
                maximum = next_nodes[i].fitness;
                idx = i;
            }
        }
    }
    if(mode == "min"){
        double minimum = INT_MAX;
        for(int i=0;i<next_nodes.size();i++){
            if(next_nodes[i].fitness < minimum){
                minimum = next_nodes[i].fitness;
                idx = i;
            }
        }
    }
    // cout<<"in find best: "<<(cur_node.fitness==next_nodes[idx].fitness)<<endl;
    // cout<<"in find best: "<<next_nodes.size()<<endl;
    cur_node = next_nodes[idx];
}


cell Anneling::run(string mode){
    initialize();
    evaluate(cur_node);
    best_node.fitness = cur_node.fitness;
    for(int iter=0;iter<max_iter;iter++){
        // Move the posoition of node.
        move();

        double prev_fitness = cur_node.fitness;
        double best_fitness = best_node.fitness;

        find_best(mode);
        best_node_list.push_back(cur_node);

        if(mode == "max"){
            if(best_node.fitness < cur_node.fitness){
                best_node = cur_node;
                best_iter = iter+1;
            }
            else if(randfloat(0.0, 1.0) > exp((cur_node.fitness - best_fitness) / temperature))
                return best_node;
        }
        if(mode == "min"){
            // cout<<"iteraaaa: "<<iter<<" exp: "<<(cur_node.fitness - prev_fitness)<<endl;
            if(best_node.fitness > cur_node.fitness){
                best_node = cur_node;
                best_iter = iter+1;
            }
            else if(randfloat(0.0, 1.0) > exp((cur_node.fitness - best_fitness) / temperature)){
                cout<<"Enter\n";
                return best_node;
            }
        }
    }
    return best_node;
}

int main(){
    srand((unsigned)time(NULL));  // (unsigned)time(NULL) 1617968974
    int max_iter=1000, min_bound=0, max_bound=1;
    float precision=0.01;

    string mode = "min";

    // 收集實驗數據用於計算平均和最大最小值範圍
    vector<float> total_fitness, total_iter, total_x1, total_x2;
    vector<float> real_total_iter;
    // 收集數據之實驗次數
    int exp_num=1;
    for(int exp=0;exp<exp_num;exp++){
        int iter = 0;
        cell best_one;
        float temperature = 100;
        for(;temperature>1;temperature*=0.2){
            // temperature = 1e-5;
            Anneling ga(
                max_iter,
                min_bound,
                max_bound,
                precision,
                temperature);

            cout<<exp<<" temperature: "<<temperature<<"\n";

            for(int i=0;i<100;i++){
                //  Start to run.
                cell node = ga.run(mode);
                if(iter == 0)
                    best_one = node;

                if(mode == "max" && best_one.fitness < node.fitness)
                    best_one = node;
                if(mode == "min" && best_one.fitness > node.fitness)
                    best_one = node;

                // cout<<"best iter: "<<ga.best_iter<<"\n";
                // cout<<"x1: "<<ga.best_node.x1<<"\n";
                // cout<<"x2: "<<ga.best_node.x2<<"\n";
                // cout<<"fitness: "<<ga.best_node.fitness<<"\n";
                // cout<<"=====\n";
                total_iter.push_back(ga.best_iter);
                iter++;
            }
            // cout<<iter<<"\n";
        }
        total_fitness.push_back(best_one.fitness);
        total_x1.push_back(best_one.x1);
        total_x2.push_back(best_one.x2);
        real_total_iter.push_back(find_sum(total_iter)/iter);
        total_iter.clear();
    }
    cout<<"===\n";
    cout<<"|name|stats|\n";
    cout<<"|-|-|\n";
    cout<<"|fitness mean| "<<setprecision(6)<<find_sum(total_fitness)/ exp_num<<"|\n";
    cout<<"|iter mean   | "<<find_sum(real_total_iter) / exp_num<<"|\n";
    cout<<"|x1 mean     | "<<setprecision(4)<<find_sum(total_x1) / exp_num<<"|\n";
    cout<<"|x2 mean     | "<<setprecision(4)<<find_sum(total_x2) / exp_num<<"|\n";

    // 計算 range (min, max).
    find_range(total_fitness, "fitness");
    find_range(real_total_iter, "iter");
    find_range(total_x1, "x1");
    find_range(total_x2, "x2");

}