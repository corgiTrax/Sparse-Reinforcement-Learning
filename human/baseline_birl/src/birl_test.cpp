#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdlib.h>
#include <ctime>
#include "../include/mdp.hpp"
#include "../include/birl.hpp"

#define GRID_WIDTH 20
#define GRID_HEIGHT 20

#define MIN_R -5
#define MAX_R 5

#define CHAIN_LENGTH 3200

#define NUM_EXP 5

using namespace std;

double policyLoss(vector<unsigned int> policy, GridMDP * mdp)
{
  unsigned int count = 0;
  mdp -> calculateQValues();

  for(unsigned int i=0; i < policy.size(); i++)
  {
    if(! mdp->isOptimalAction(i,policy[i])) {
      count++;
    }
  }
  return (double)count/(double)policy.size()*100;
}

int main( ) {

  double total_loss = 0;

  for(unsigned int itr = 0; itr < NUM_EXP; itr++)
  { 

          GridMDP mdp(GRID_WIDTH,GRID_HEIGHT); //ground truth mdp
          
          unsigned int terminal_state = rand()%mdp.getNumStates();//GRID_WIDTH - 1;
          srand (time(NULL));
          mdp.addTerminalState(terminal_state);

          cout << "\nInitializing gridworld task of size " << GRID_WIDTH << endl;
          cout << "    Num states: " << mdp.getNumStates() << endl;
          cout << "    Num actions: " << mdp.getNumActions() << endl;

          double* rewards = new double[mdp.getNumStates()]; //random reward function
          
          for(unsigned int s=0; s<mdp.getNumStates(); s++)
          {
            rewards[s] = pow(-1,rand())*(rand()%100)/100.0; 
          }
          //rewards[terminal_state] = MAX_R;
          mdp.setRewards(rewards);
          cout << "\n-- True Rewards --" << endl;
          mdp.displayRewards();

          //solve for the optimal policy
          vector<unsigned int> opt_policy (mdp.getNumStates());
          mdp.valueIteration(0.001);
          mdp.deterministicPolicyIteration(opt_policy);
          cout << "-- optimal policy --" << endl;
          mdp.displayPolicy(opt_policy);

          //initializing birl with reward ranges, BIRL chain length and reward step size

          vector<unsigned int> policy (mdp.getNumStates());
          BIRL birl(&mdp, MIN_R, MAX_R, CHAIN_LENGTH, 0.05);
          birl.mdp->addTerminalState(terminal_state);

          vector<pair<unsigned int,unsigned int> > good_demos;
          vector<pair<unsigned int,unsigned int> > bad_demos;
          mdp.calculateQValues();

          for(unsigned int s=0; s < mdp.getNumStates(); s++)
          {
            //int rand_state = rand() % mdp.getNumStates();
            //good_demos.push_back(make_pair(idx, opt_policy[idx])); //ground truth policy as input
            for (unsigned int a=0; a < mdp.getNumActions(); a++)
            {
              if(mdp.isOptimalAction(s,a) ) good_demos.push_back(make_pair(s,a));
              else bad_demos.push_back(make_pair(s, a));

            }
          }

          birl.addPositiveDemos(good_demos);
          birl.addNegativeDemos(bad_demos);
          birl.displayDemos();

          clock_t c_start = clock();
          birl.run();
          clock_t c_end = clock();
          cout << "\n[Timing] Time passed: "
            << (c_end-c_start)*1.0 / CLOCKS_PER_SEC << " s\n";

          /*if( mdp == birl.getMDP() ) cout << "Two rewards are equal!" << endl;
            else cout << "Two rewards are not equal!" << endl;*/

          cout << "\n-- Fianl Recovered Rewards --" << endl;
          birl.getMAPmdp()->displayRewards(GRID_WIDTH);

          cout << "\n-- Final Policy --" << endl;
          birl.getMAPmdp()->deterministicPolicyIteration(policy);

          mdp.displayPolicy(policy);
          birl.getMAPmdp()->calculateQValues();
          cout << endl;
          for(unsigned int s=0; s < mdp.getNumStates(); s++)
          {
            for (unsigned int a=0; a < mdp.getNumActions(); a++)
            {
              if(birl.getMAPmdp()->isOptimalAction(s,a)) cout << "{" << s << "," << a << "},";
            }
          }
          cout << endl;

          cout.precision(12);
          cout << "\nPosterior Probability: " << birl.getMAPposterior() << endl;
          cout.precision(2);

          double base_loss = policyLoss(policy, &mdp);
          cout << "Current policy loss: " << base_loss << "%" << endl;
          total_loss += base_loss;

          delete [] rewards;
  }
  cout << "Ave policy loss: " << total_loss / NUM_EXP << "%" << endl;
  
  return 0;
}
