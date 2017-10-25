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
	const double step = 0.00025;
	const double alpha = 25;
	const unsigned int chain_length = 5000 ; // 4002 must be a multiple of 3!

	const unsigned int interactions = 0; 

	//test arrays to get features
	const int numFeatures = 4; // target, obstacle, pathpoint, None
	const int numStates = grid_width * grid_height;

	double losses[interactions+1] = {0}; 
	double gamma = 0.25;

	double featureWeights[numFeatures] = {0,0,0,-0.1};

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
    
    double posterior = -1000;
    FeatureGridMDP* mapMDP;
    FeatureGridMDP* bestMDP = mdp.deepcopy();
    FeatureBIRL birl(&mdp, min_r, max_r, chain_length, step, alpha);
    unsigned int num_itr = 0;
    //double best_posterior = -1000;
    double err = 180;
    
    while(posterior < -50 && num_itr < 50)
    {
	    //create feature birl and initialize with demos
	    
	    birl.addPositiveDemos(good_demos);
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
        for(unsigned int si = 0; si < good_demos.size(); si++)
        {
            if(map_policy[good_demos[si].first] == good_demos[si].second) correct_actions += 1;
            else
			{
				float angle1 = angle_map[good_demos[si].second];
				float angle2 = angle_map[map_policy[good_demos[si].first]];
				float angle = 0;
				if( angle1 > angle2) angle = angle1 - angle2;
				else angle = angle2 - angle1;
				if (angle > 180) angle = 360 - angle;
				angle_diffs += angle;
			}
        }
        float agreement = float(correct_actions)/good_demos.size()*100;
	float curr_err = float(angle_diffs)/good_demos.size();

        cout << "Agreement with demo: " << agreement << "%" << endl;
        cout << "Avg angular diffs: " << curr_err << "'" << endl;
        if(curr_err < err)  //(posterior > best_posterior) 
        {
            //best_posterior = posterior;
            err = curr_err;
            delete bestMDP;
            bestMDP = mapMDP->deepcopy();
        }
        num_itr++;
    }
    
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




