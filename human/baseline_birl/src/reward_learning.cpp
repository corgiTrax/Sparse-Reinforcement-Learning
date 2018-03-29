#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdlib.h>
#include <ctime>
#include <string>
#include <map>
#include <set>

#include "../include/mdp.hpp"
#include "../include/feature_birl.hpp"
#include "../include/grid_domain.hpp"

enum actions {UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT};
using namespace std;

int main(int argc, char** argv) {

	if (argc < 4) {
		cout << " Usage: reward_learning <subj> <trial> <task>" << endl;
		return 0;
	}
	unsigned int subj = atoi(argv[1]);
	unsigned int trial = atoi(argv[2]);
	unsigned int task = atoi(argv[3]);

	string feature_file_name = "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_domain_features.txt";
	string demo_file_name    =  "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_demonstrations.txt";

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
	const double min_r = -1.0;
	const double max_r = 1.0;
	const double step  = 0.00025;
	const double alpha = 100;
	const unsigned int chain_length = 3000 ; 

	//test arrays to get features
	const int numFeatures = 4;  // target, obstacle, pathpoint, None
	const int numStates = grid_width * grid_height;
	double gamma = 0.3;

	double featureWeights[numFeatures] = {0,0,0,-0.1};
	double** stateFeatures = initFeaturesDiscreteDomain(numStates, numFeatures, feature_file_name);

	vector<unsigned int> initStates = {};
	vector<unsigned int> termStates = {};

	FeatureGridMDP mdp(grid_width, grid_height, initStates, termStates, numFeatures, featureWeights, stateFeatures, gamma);
	cout << "\nInitializing gridworld of size " << grid_width << " by " << grid_height << ".." << endl;
	cout << "    Num states: " << mdp.getNumStates() << endl;
	cout << "    Num actions: " << mdp.getNumActions() << endl;
	srand (time(NULL));
	//read in demos
	vector<pair<unsigned int,unsigned int> > demos;
	vector<pair<unsigned int,unsigned int> > good_demos;
	map<unsigned int, unsigned int> demo_freq;
	for(unsigned int s = 0; s < grid_width*grid_height; s++) demo_freq.insert(pair<unsigned int,unsigned int>(s,0));

	ifstream demo_file (demo_file_name);
	unsigned int demo_ct = 0;

	if(demo_file.is_open())
	{
		string line;
		while(getline(demo_file,line))
		{
			demo_ct += 1;
			if(demo_ct > 10)
			{
				vector<string> results;
				split(line,',', results);
				unsigned int state = stoi(results[0]);
				unsigned int action = stoi(results[1]);
				demos.push_back(make_pair(state,action));
				demo_freq[state] += 1;
			}
		}
		demo_file.close();
	}
	else{
		return 1;
	}   
	for(unsigned int d = 0; d < demos.size(); d++) 
	{
		if(demo_freq[demos[d].first] < 3) good_demos.push_back(demos[d]);
	}
	cout << "\nTotal number of demos: " << good_demos.size() << endl;

	double posterior = -1000;
	FeatureGridMDP* mapMDP;
	FeatureGridMDP* bestMDP = mdp.deepcopy();
	FeatureBIRL birl(&mdp, min_r, max_r, chain_length, step, alpha);
	unsigned int num_itr = 0;
	//double best_posterior = -1000;
	double err = 180;

	while( posterior < -50 && num_itr < 50 )
	{
		// randomly sample a subset of the original demonstrations
		vector<pair<unsigned int,unsigned int> > selected_demos;
		unsigned int skip = 1 + rand()%6;
		for(unsigned int d = rand()%skip; d < good_demos.size(); d += (1 + rand()%skip)) selected_demos.push_back(good_demos[d]);
		cout << "\nSelected number of demos: " << selected_demos.size() << endl;
		birl.addPositiveDemos(selected_demos);
		birl.displayDemos();

		//run birl MCMC
		clock_t c_start = clock();
		birl.run();
		clock_t c_end = clock();
		cout << "\n[Timing] Time passed: "
			<< (c_end-c_start)*1.0 / CLOCKS_PER_SEC << " s\n";
		mapMDP = birl.getMAPmdp();

		cout.precision(10);
		cout << "\nPosterior Probability: " << birl.getMAPposterior() << endl;
		cout.precision(2);
		posterior = birl.getMAPposterior();
		birl.removeAllDemostrations();

		vector<unsigned int> map_policy (mdp.getNumStates());
		mapMDP->valueIteration(0.0005);
		mapMDP->deterministicPolicyIteration(map_policy);
		unsigned int correct_actions = 0;
		double angle_diffs = 0.0;
		for(unsigned int si = 0; si < demos.size(); si++)
		{
			if(map_policy[demos[si].first] == demos[si].second) correct_actions += 1;
			else
			{
				float angle1 = angle_map[demos[si].second];
				float angle2 = angle_map[map_policy[demos[si].first]];
				float angle = 0;
				if( angle1 > angle2) angle = angle1 - angle2;
				else angle = angle2 - angle1;
				if (angle > 180) angle = 360 - angle;
				angle_diffs += angle;
			}
		}
		float agreement = float(correct_actions)/demos.size()*100;
		float curr_err = float(angle_diffs)/demos.size();
		cout << "Agreement with demo: " << agreement << "%" << endl;
		cout << "Current angular diffs: " << curr_err << "'" << endl;
		if(curr_err < err) 
		{
			err = curr_err;
			delete bestMDP;
			bestMDP = mapMDP->deepcopy();
		}
		num_itr++;
	}
	cout << "\n-----------------------------" << endl;
	cout << "Avg angular diffs: " << err << "'" << endl;
	cout << "-- learned weights --" << endl;
	bestMDP->displayFeatureWeights();
	delete bestMDP;

	//clean up memory
	for(unsigned int s1 = 0; s1 < numStates; s1++)
	{
		delete[] stateFeatures[s1];
	}
	delete[] stateFeatures;

	return 0;
}




