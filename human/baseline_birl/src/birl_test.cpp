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

double policyLoss(vector<unsigned int> policy, GridMDP * mdp)
{
	unsigned int count = 0;
	mdp -> calculateQValues();

	for(unsigned int i=0; i < policy.size(); i++)
	{
		if(! mdp->isOptimalAction(i,policy[i])) {
			//cout <<"incorect?" << i << " " << policy[i] << endl;
			count++;
		}
	} 
	return (double)count/(double)policy.size()*100; 
}


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

	srand (time(NULL));

	map<unsigned int, float> angle_map;
	angle_map.insert(pair<unsigned int,float>(UP,0.0));
	angle_map.insert(pair<unsigned int,float>(UP_RIGHT,45.0));
	angle_map.insert(pair<unsigned int,float>(RIGHT,90.0));
	angle_map.insert(pair<unsigned int,float>(DOWN_RIGHT,135.0));
	angle_map.insert(pair<unsigned int,float>(DOWN,180.0));
	angle_map.insert(pair<unsigned int,float>(DOWN_LEFT,225.0));
	angle_map.insert(pair<unsigned int,float>(LEFT,270.0));
	angle_map.insert(pair<unsigned int,float>(UP_LEFT,315.0));

	const unsigned int grid_width = 28;
	const unsigned int grid_height = 22;
	const double min_r = -1.0;
	const double max_r = 1.0;
	const double step = 0.001;
	const double alpha = 20;
	const unsigned int chain_length = 20000; // 4002 must be a multiple of 3!

	const unsigned int interactions = 0; 

	//test arrays to get features
	const int numFeatures = 4; // target, obstacle, pathpoint, None
	const int numStates = grid_width * grid_height;

	double losses[interactions+1] = {0}; 
	double gamma = 0.25;

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

	//generate demos
	vector<pair<unsigned int,unsigned int> > good_demos;
	ifstream demo_file (demo_file_name);


	cout << "recovered reward" << endl;
	mdp.displayRewards();

	vector<unsigned int> map_policy (mdp.getNumStates());
	mdp.valueIteration(0.0005);
	mdp.deterministicPolicyIteration(map_policy);

	cout << "-- optimal policy --" << endl;
	mdp.displayPolicy(map_policy);

	unsigned int correct_actions = 0;
	unsigned int total_actions = 0;
	double angle_diffs = 0.0;
	if(demo_file.is_open())
	{
		string line;
		while(getline(demo_file,line))
		{
			vector<string> results;
			split(line,',', results);
			unsigned int state = stoi(results[0]);
			unsigned int action = stoi(results[1]);
			good_demos.push_back(make_pair(state,map_policy[state]));
			//cout << "state: " << state << ", action predicted: " << map_policy[state] <<", action took: " << action  << endl;
			total_actions += 1;
			if( action == map_policy[state] ) correct_actions += 1;
			else
			{
				float angle1 = angle_map[action];
				float angle2 = angle_map[map_policy[state]];
				float angle = 0;
				if( angle1 > angle2) angle = angle1 - angle2;
				else angle = angle2 - angle1;
				if (angle > 180) angle = 360 - angle;
				angle_diffs += angle;
			}

		}
		demo_file.close();
	}
	else{
		return 1;
	}   

	float policy_overlap = float(correct_actions) / total_actions * 100;
	float avg_ang_err = angle_diffs / total_actions;
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




