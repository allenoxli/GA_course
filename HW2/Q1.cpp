#include<iostream>
#include<cmath>
#include<cstdlib>   // 亂數相關函數
#include<ctime>     // 時間相關函數
#include<vector>
#include<climits>
using namespace std;

struct cell{
    double x1, x2;
    double fitness;
};

class GAFloat{
public:
    int max_iter, population_size;
    float p_mutation, p_crossover;
    vector<cell> population;   // The total number of population.
    vector<cell> pool;
    vector<int> best_gene_list;
    cell best_cell;
    int best_iter, cur_iter=0;
    GAFloat(int max_iter, int population_size, float min_bound, float max_bound, float precision, float p_mutation, float p_crossover);
    void initialize();
    void evaluate();
    void crossover();
    void mutation();
    void select(string mode, int times);
    void run(string mode, int times);
    int find_best(string mode);
    void print_info(int iter_interval);
};

GAFloat::GAFloat(int max_iter, int population_size, float min_bound, float max_bound, float precision, float p_mutation, float p_crossover){

    this->max_iter = max_iter;
    this->population_size = population_size;
    this->p_mutation = p_mutation;
    this->p_crossover = p_crossover;

    this->p_mutation = p_mutation;
    this->p_crossover = p_crossover;

    cout<<"Constructor.\n";
}

void GAFloat::initialize(){
    for(int i=0;i<population_size;i++){
        cell node;
        node.x1 = (double)rand() / RAND_MAX;
        node.x2 = (double)rand() / RAND_MAX;
        population.push_back(node);
    }
}

void GAFloat::evaluate(){
    for(auto& node: population){
        double x1=node.x1, x2=node.x2;
        double left_part = pow(x1*x1 + x2*x2, 0.25),
                right_part = pow(sin(50*pow((x1*x1 + x2*x2), 0.1)), 2.0) + 1;

        node.fitness = left_part * right_part;
    }
}

void GAFloat::select(string mode, int times){
    pool.clear();
    for(int i=0;i<population_size;i++){
        int select_idx = rand() % population_size;
        for(int j=0;j<times;j++){
            int idx = rand() % population_size;
            if(mode == "max"){
                if(population[select_idx].fitness < population[idx].fitness)
                    select_idx = idx;
            }
            if(mode == "min"){
                if(population[select_idx].fitness > population[idx].fitness)
                    select_idx = idx;
            }
        }
        pool.push_back(population[select_idx]);
    }
    population.clear();
    population.assign(pool.begin(), pool.end());
}

void GAFloat::crossover(){
    int idx1, idx2;
    for(int i=0;i<population_size;i++){
        if((double)rand() / RAND_MAX > p_crossover)  // Do not corssover.
            continue;
            idx1 = rand() % population_size;
            idx2 = rand() % population_size;
            while(idx2 == idx1){
                idx2 = rand() % population_size;

            population[idx1].x2 = pool[idx2].x2;
            population[idx2].x1 = pool[idx1].x1;
        }
    }
}

void GAFloat::mutation(){
    for(auto& node: population){
        if((double)rand() / RAND_MAX < p_mutation)
            node.x1 = rand() / RAND_MAX;
        if((double)rand() / RAND_MAX < p_mutation)
            node.x2 = rand() / RAND_MAX;
    }
}

void GAFloat::run(string mode, int times){
    best_cell.fitness = (mode == "max") ? INT_MIN : INT_MAX;
    initialize();
    evaluate();
    for(int iter=0;iter<max_iter;iter++){
        select(mode, times);
        crossover();
        mutation();
        evaluate();
        int best_idx = find_best(mode);
        best_gene_list.push_back(best_idx);
    }
    int iter_interval = 200;
    print_info(iter_interval);
}

int GAFloat::find_best(string mode){
    cur_iter++;
    int idx;
    if(mode == "max"){
        double maximum = INT_MIN;
        for(int i=0;i<population_size;i++){
            if(population[i].fitness > maximum){
                maximum = population[i].fitness;
                idx = i;
                if(best_cell.fitness < maximum){
                    best_cell = population[i];
                    best_iter = cur_iter;
                }
            }
        }
    }
    if(mode == "min"){
        double minimum = INT_MAX;
        for(int i=0;i<population_size;i++){
            if(population[i].fitness < minimum){
                minimum = population[i].fitness;
                idx = i;
                if(best_cell.fitness > minimum){
                    best_cell = population[i];
                    best_iter = cur_iter;
                }
            }
        }
    }
    return idx;
}

void GAFloat::print_info(int iter_interval){
    int iter = 1;
    for(int iter=0;iter<best_gene_list.size();iter+=iter_interval){
        int idx = best_gene_list[iter];
        double x1_val=population[idx].x1,
            x2_val=population[idx].x2;
        cout<<"Iteration: "<<iter<<"\n"
            <<"best fitness: "<<population[idx].fitness<<"\n"
            <<"(x1, x2) = ("<<x1_val<<", "<<x2_val<<")\n";

        cout<<"======\n";
    }
    double x1_val=best_cell.x1, x2_val=best_cell.x2;

    cout<<"All best fitness: "<<best_cell.fitness<<endl;
    cout<<"All best (x1, x2): "<<x1_val<<", "<<x2_val<<endl;
    cout<<"All best iter: "<<best_iter<<endl;
}

int main(){
    srand((unsigned)time(NULL));  // (unsigned)time(NULL)

    int max_iter=10000, population_size=100, min_bound=0, max_bound=1;
    float precision=0.0001, p_mutation=0.01, p_crossover=0.25;
    

    string mode = "max";
    int times = 5;

    // 收集實驗數據用於計算平均和最大最小值範圍
    vector<float> total_fitness, total_iter, total_x1, total_x2;
    // 收集數據之實驗次數
    int exp_num=1;
    for(int exp=0;exp<exp_num;exp++){
        // Construct instance;
        GAFloat ga(
        max_iter,
        population_size,
        min_bound,
        max_bound,
        precision,
        p_mutation,
        p_crossover);

        ga.run(mode, times);

        total_fitness.push_back(ga.best_cell.fitness);
        total_x1.push_back(ga.best_cell.x1);
        total_x2.push_back(ga.best_cell.x2);
        total_iter.push_back(ga.best_iter);
        
    }


    cout<<"===\n";
    cout<<"|name|stats|\n";
    cout<<"|-|-|\n";
    cout<<"|fitness mean| "<<setprecision(6)<<find_sum(total_fitness)/ exp_num<<"|\n";
    cout<<"|iter mean   | "<<find_sum(total_iter) / exp_num<<"|\n";
    cout<<"|x1 mean     | "<<setprecision(4)<<find_sum(total_x1) / exp_num<<"|\n";
    cout<<"|x2 mean     | "<<setprecision(4)<<find_sum(total_x2) / exp_num<<"|\n";

    find_range(total_fitness, "fitness");
    find_range(total_iter, "iter");
    find_range(total_x1, "x1");
    find_range(total_x2, "x2");

    cout<<"\n Now mode: "<<mode<<endl;
    cout<<"GA float string\n";
}
