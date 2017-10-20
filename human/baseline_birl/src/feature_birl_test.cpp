#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdlib.h>
#include <ctime>
#include <string>

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

	if (argc < 4) {
		cout << " Usage: feature_birl_test <subj> <trial> <task>" << endl;
		return 0;
	}
	unsigned int subj = atoi(argv[1]);
	unsigned int trial = atoi(argv[2]);
	unsigned int task = atoi(argv[3]);

	string feature_file_name = "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_domain_features.txt";
	string demo_file_name    =  "../birl_data/" + string(argv[1]) + "_" + string(argv[2]) + "_" + string(argv[3]) + "_demonstrations.txt";

	srand (time(NULL));

	const unsigned int grid_width = 28;
	const unsigned int grid_height = 22;
	const double min_r = -1.0;
	const double max_r = 1.0;
	const double step = 0.001;
	const double alpha = 50;
	const unsigned int chain_length = 15000; // 4002 must be a multiple of 3!

	const unsigned int interactions = 0; 

	//test arrays to get features
	const int numFeatures = 4; // target, obstacle, pathpoint, None
	const int numStates = grid_width * grid_height;

	double losses[interactions+1] = {0}; 
	double gamma = 0.25;

	double featureWeights[numFeatures] = {0,0,1,-0.1};

	//double** stateFeatures = initRandomFeaturesRandomDomain(numStates, numFeatures);
	double** stateFeatures = initFeaturesDiscreteDomain(numStates, numFeatures, feature_file_name);

	vector<unsigned int> initStates = {};
	vector<unsigned int> termStates = {};

	//unsigned int initial_state = initStates[0];

	FeatureGridMDP mdp(grid_width, grid_height, initStates, termStates, numFeatures, featureWeights, stateFeatures, gamma);

	cout << "\nInitializing gridworld of size " << grid_width << " by " << grid_height << ".." << endl;
	cout << "    Num states: " << mdp.getNumStates() << endl;
	cout << "    Num actions: " << mdp.getNumActions() << endl;

	srand (time(NULL));

	//generate demos
	vector<pair<unsigned int,unsigned int> > good_demos;
	ifstream demo_file (demo_file_name);

	if(demo_file.is_open())
	{
		string line;
		while(getline(demo_file,line))
		{
			vector<string> results;
			split(line,',', results);
			unsigned int state = stoi(results[0]);
			unsigned int action = stoi(results[1]);
			good_demos.push_back(make_pair(state,action));
		}
		demo_file.close();
	}
	else{
		return 1;
	}   

	//create feature birl and initialize with demos
	FeatureBIRL birl(&mdp, min_r, max_r, chain_length, step, alpha);
	birl.addPositiveDemos(good_demos);
	birl.displayDemos();

	//run birl MCMC
	clock_t c_start = clock();
	birl.run();
	clock_t c_end = clock();
	cout << "\n[Timing] Time passed: "
		<< (c_end-c_start)*1.0 / CLOCKS_PER_SEC << " s\n";
	FeatureGridMDP* mapMDP = birl.getMAPmdp();

	//cout << "recovered reward" << endl;
	//mapMDP->displayRewards();

	//vector<unsigned int> map_policy (mapMDP->getNumStates());
	//mapMDP->valueIteration(0.001);

	//cout << "-- value function --" << endl;
	//mapMDP->displayValues();
	//mapMDP->deterministicPolicyIteration(map_policy);

	//cout << "-- optimal policy --" << endl;
	//mapMDP->displayPolicy(map_policy);


	cout.precision(10);
	cout << "\nPosterior Probability: " << birl.getMAPposterior() << endl;
	cout.precision(2);

	cout << "-- learned weights --" << endl;
	mapMDP->displayFeatureWeights();

	//clean up memory
	for(unsigned int s1 = 0; s1 < numStates; s1++)
	{
		delete[] stateFeatures[s1];
	}
	delete[] stateFeatures;

	return 0;
}




