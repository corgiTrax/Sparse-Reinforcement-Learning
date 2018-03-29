#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdlib.h>
#include <ctime>
#include <string>
#include <map>

#include "../include/mdp.hpp"
#include "../include/feature_birl.hpp"
#include "../include/grid_domain.hpp"


enum actions {UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT};

using namespace std;


int main(int argc, char** argv) {

	if (argc < 8) {
		cout << " Usage: birl_test <subj> <trial> <task> <test_weight1> <test_weight2> <test_weight3> <test_weight4>" << endl;
		return 0;
	}
	unsigned int subj = atoi(argv[1]);
	unsigned int trial = atoi(argv[2]);
	unsigned int task = atoi(argv[3]);
	float weight1 = atof(argv[4]);
	float weight2 = atof(argv[5]);
	float weight3 = atof(argv[6]);
	float weight4 = atof(argv[7]);

	cout << "arguments: " << subj << " " << trial << " " << task << " " << weight1 << " " << weight2 << " " << weight3 << " " <<  weight4 << endl;
	string feature_file_name = "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_domain_features.txt";
	string demo_file_name    =  "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_demonstrations.txt";

	srand (time(NULL) + rand());

	map<unsigned int, float> angle_map;
	angle_map.insert(pair<unsigned int,float>(UP,0.0));
	angle_map.insert(pair<unsigned int,float>(UP_RIGHT,45.0));
	angle_map.insert(pair<unsigned int,float>(RIGHT,90.0));
	angle_map.insert(pair<unsigned int,float>(DOWN_RIGHT,135.0));
	angle_map.insert(pair<unsigned int,float>(DOWN,180.0));
	angle_map.insert(pair<unsigned int,float>(DOWN_LEFT,225.0));
	angle_map.insert(pair<unsigned int,float>(LEFT,270.0));
	angle_map.insert(pair<unsigned int,float>(UP_LEFT,315.0));

	const unsigned int grid_width = 32;
	const unsigned int grid_height = 24;

	//test arrays to get features
	const int numFeatures = 4; // target, obstacle, pathpoint, None (to introduce negative living reward)
	const int numStates = grid_width * grid_height;

	double gamma = 0.7;
	double featureWeights[numFeatures];

	featureWeights[0] = weight1;
	featureWeights[1] = weight2;
	featureWeights[2] = weight3;
	featureWeights[3] = weight4;

	double** stateFeatures = initFeaturesDiscreteDomain(numStates, numFeatures, feature_file_name);

	vector<unsigned int> initStates = {};
	vector<unsigned int> termStates = {};

	FeatureGridMDP mdp(grid_width, grid_height, initStates, termStates, numFeatures, featureWeights, stateFeatures, gamma);
	 cout << "\nInitializing gridworld of size " << grid_width << " by " << grid_height << ".." << endl;
	 cout << "    Num states: " << mdp.getNumStates() << endl;
	 cout << "    Num actions: " << mdp.getNumActions() << endl;

	srand (time(NULL));

	//read in human data
	vector<pair<unsigned int,unsigned int> > good_demos;
	ifstream demo_file (demo_file_name);

	unsigned int demo_ct = 0;
	//mdp.displayRewards();
	vector<unsigned int> opt_policy (mdp.getNumStates());
	mdp.valueIteration(0.0005);
	mdp.calculateQValues();
	mdp.deterministicPolicyIteration(opt_policy);

	// cout << "-- optimal policy --" << endl;
	// mdp.displayPolicy(opt_policy);

	unsigned int correct_actions = 0;
	unsigned int total_actions = 0;
	double angle_diffs = 0.0;
	map<unsigned int, unsigned int> demo_freq;
	for(unsigned int s = 0; s < grid_width*grid_height; s++)  demo_freq.insert(pair<unsigned int,unsigned int>(s,0));

	if(demo_file.is_open())
	{
		string line;
		while(getline(demo_file,line))
		{
			demo_ct += 1;
			if(demo_ct > 5) // skip first 5
			{
				vector<string> results;
				split(line,',', results);
				unsigned int state = stoi(results[0]);
				unsigned int action = stoi(results[1]);
				good_demos.push_back(make_pair(state,action));
				demo_freq[state] += 1;
			}
		}
		demo_file.close();
	}
	else{
		return 1;
	}   

	// cout << "BIRL Actions:";
	for(unsigned int i=0; i < good_demos.size(); i++)
	{
		unsigned int state = good_demos[i].first;
		unsigned int action = good_demos[i].second;
		if( demo_freq[state] < 2)
		{
			total_actions += 1;
			// cout << "(" << state << "," ;
			if(  mdp.isOptimalAction(state,action) )  {
				correct_actions += 1;
				// cout << action << "), ";
			}
			else{
				vector<unsigned int> actions;
				mdp.getOptimalActions(state, actions);
				double min_diff = 180;
				unsigned int min_action = action;
				//cout << "optimal actions : ";
				for(unsigned int a: actions)
				{
					//cout << a << ", " ;
					float angle1 = angle_map[a];
					float angle2 = angle_map[action];
					float angle = 0;
					if( angle1 > angle2) angle = angle1 - angle2;
					else angle = angle2 - angle1;
					if (angle > 180) angle = 360 - angle;
					if (angle < min_diff){
						min_diff = angle;
						min_action = a;
					}
				}
				// cout << min_action << "), ";
				angle_diffs += min_diff;
			}
		}
	}
	cout << endl;
	// cout << "BIRL Trajectories:" << endl;
        double visited_features[4] = {0.0,0.0,0.0,1.0}; 
	for(unsigned int traj_ct = 0; traj_ct < 200; traj_ct++)
	{
                FeatureGridMDP* fmdp = mdp.deepcopy();
                
		cout << "[" ;
		unsigned int curr_state = good_demos[rand()%20].first;
		unsigned int prev_state;
		for(unsigned int i=0; i < good_demos.size(); i++)
		{
                        fmdp->valueIteration(0.0005);
	                fmdp->calculateQValues();
			prev_state = curr_state;
			vector<unsigned int> curr_actions = fmdp->getValidActions(curr_state);
			double total_q = 0.0;
			for(unsigned int a: curr_actions) total_q += 0.1*exp(10*fmdp->getQValue(curr_state,a));
			vector<double> probabilities;
			for(unsigned int a: curr_actions) 
			{
				if(probabilities.size() > 0)
					probabilities.push_back(0.1*exp(10*fmdp->getQValue(curr_state,a))/total_q + probabilities.back());
				else
					probabilities.push_back(0.1*exp(10*fmdp->getQValue(curr_state,a))/total_q );
				// cout << a << ":" << probabilities.back() << endl;
			}
			double rand_num = rand()%1000/1000.0;
			unsigned int selected_idx = 0;
			for(unsigned int idx=0; idx < probabilities.size(); idx++)
			{
				if(rand_num < probabilities[idx]) 
				{
					selected_idx = idx;
					break;
				}
			}
			cout << "(" << curr_state;
			cout << "," << curr_actions[selected_idx] << "),";
			fmdp->setFeatureAtState(curr_state, visited_features);
                        if(curr_state%grid_width < grid_width - 1){
                               fmdp->setFeatureAtState(curr_state+1, visited_features);
                               if(curr_state - grid_width > 0) fmdp->setFeatureAtState(curr_state - grid_width + 1, visited_features);
                               if(curr_state + grid_width + 1 < numStates) fmdp->setFeatureAtState(curr_state + grid_width + 1, visited_features);
                        }
                        if(curr_state%grid_width > 1){
                               fmdp->setFeatureAtState(curr_state-1, visited_features);
                               if(curr_state - grid_width - 1> 0) fmdp->setFeatureAtState(curr_state - grid_width - 1, visited_features);
                               if(curr_state + grid_width - 1< numStates) fmdp->setFeatureAtState(curr_state + grid_width - 1, visited_features);
                        }
                        if(curr_state - grid_width > 0) fmdp->setFeatureAtState(curr_state - grid_width, visited_features);
                        if(curr_state + grid_width < numStates) fmdp->setFeatureAtState(curr_state + grid_width, visited_features);
                        fmdp->computeCachedRewards();

                        curr_state = fmdp->getNextState(curr_state, curr_actions[selected_idx]);
                        
			//if(curr_state == prev_state) break;
		}
		cout << "]" << endl;
	}
	float policy_overlap = float(correct_actions) / total_actions * 100;
	float avg_ang_err = angle_diffs / total_actions;
	 cout << "Total actions tested : " << total_actions << endl;
	 cout << "Correct actions (%) : " << policy_overlap << endl;
	 cout << "Avg angular diffs   : " << avg_ang_err << endl;

	//clean up memory
	for(unsigned int s1 = 0; s1 < numStates; s1++)
	{
		delete[] stateFeatures[s1];
	}
	delete[] stateFeatures;

	return 0;
}




