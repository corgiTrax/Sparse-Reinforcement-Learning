
#ifndef birl_h
#define birl_h

#include <cmath>
#include <stdlib.h>
#include <vector>
#include <numeric>
#include <math.h>
#include "mdp.hpp"

#define ALPHA 200

using namespace std;

class BIRL { // BIRL process

  protected:

    double r_min, r_max, step_size;
    unsigned int chain_length = 0;
    unsigned int iteration = 0;
    unsigned int numStates = 0;
    unsigned int numActions = 0;

    void initializeMDP();
    vector<pair<unsigned int,unsigned int> > positive_demonstration;
    vector<pair<unsigned int,unsigned int> > negative_demonstration;

    vector<pair<unsigned int,unsigned int> > unknown_demonstration;
    vector<double> unknown_probabilities;
    
    void modifyRewardRandomly(MDP * gmdp, double step_size);

    double* posteriors = nullptr;
    MDP* MAPmdp = nullptr;
    double MAPposterior;
    double gamma = 0.95;


  public:

    MDP* mdp = nullptr; //original MDP 
    MDP** R_chain = nullptr; //storing the rewards along the way

    ~BIRL(){
    
      if(iteration == 0){
        delete mdp;
        mdp = nullptr;
      } 
      
      if(R_chain != nullptr) {
        for(unsigned int i=0; i<chain_length; i++) {
            if(R_chain[i] != nullptr && R_chain[i] != MAPmdp){
                delete R_chain[i];
                R_chain[i] = nullptr;
             }
        }
        delete [] R_chain;
      }
      
       if(MAPmdp != nullptr)  delete MAPmdp;
      
      if(posteriors != nullptr) delete []posteriors;

      
    }


    BIRL(MDP* input, double min_reward, double max_reward, unsigned int chain, double step):  numStates(input->getNumStates()), numActions(input->getNumActions()), r_min(min_reward), r_max(max_reward), step_size(step), chain_length(chain){ 

      mdp = new MDP(gamma,numStates,numActions);
      mdp->setTransitions(input->getTransitions());
      initializeMDP(); 

      MAPmdp = new MDP(gamma,numStates,numActions);

      MAPmdp->setTerminalStates(mdp->getTerminalStates());
      MAPmdp->setRewards(mdp->getRewards());
      MAPmdp->setTransitions(input->getTransitions());
      MAPposterior = 0;

      R_chain = new MDP*[chain_length];
      fill_n(R_chain, chain_length, nullptr);
      
      posteriors = new double[chain_length];    
      
    }; 

    MDP* getMAPmdp(){return MAPmdp;}
    double getMAPposterior(){return MAPposterior;}
    void addPositiveDemo(pair<unsigned int,unsigned int> demo) { positive_demonstration.push_back(demo); }; // (state,action) pair
    void addNegativeDemo(pair<unsigned int,unsigned int> demo) { negative_demonstration.push_back(demo); };
    void addPositiveDemos(vector<pair<unsigned int,unsigned int> > demos);
    void addNegativeDemos(vector<pair<unsigned int,unsigned int> > demos);
    void run();
    void displayPositiveDemos();
    void displayNegativeDemos();
    void displayDemos();
    double getMinReward(){return r_min;};
    double getMaxReward(){return r_max;};
    double getStepSize(){return step_size;};
    unsigned int getChainLength(){return chain_length;};
    vector<pair<unsigned int,unsigned int> >& getPositiveDemos(){ return positive_demonstration; };
    vector<pair<unsigned int,unsigned int> >& getNegativeDemos(){ return negative_demonstration; };
    MDP** getRewardChain(){ return R_chain; };
    double* getPosteriorChain(){ return posteriors; };
    MDP* getMDP(){ return mdp;};
    double calculatePosterior(MDP* gmdp, double alpha=ALPHA);
    double logsumexp(double* nums, unsigned int size);
    bool isDemonstration(pair<unsigned int,unsigned int> s_a);
    void removeDemonstration(pair<unsigned int,unsigned int> s_a);
    void removeAllDemostrations();

    void addUnknownDemonstration(pair<unsigned int, unsigned int> s_a, double p_good)
    {
      unknown_demonstration.push_back(s_a);
      unknown_probabilities.push_back(p_good);
    };
    void removeAllUnknownDemonstrations()
    {
      unknown_demonstration.clear();
      unknown_probabilities.clear();
    };

};



void BIRL::run()
{

  //cout.precision(10);
  //cout << "itr: " << iteration << endl;
  if(iteration > 0) for(unsigned int i=0; i<chain_length; i++) 
  {
      if(R_chain[i] != nullptr){
            delete R_chain[i];  
            R_chain[i] = nullptr;
      }
  }
  
  iteration++;
  MAPposterior = 0;
  R_chain[0] = mdp->deepcopy(); // so that it can be deleted ?

  R_chain[0] ->valueIteration(0.001);//deterministicPolicyIteration(policy);
  R_chain[0] ->calculateQValues();
  double posterior = calculatePosterior(R_chain[0]);
  posteriors[0] = exp(posterior); 
  unsigned int total_steps = 0 ;
  unsigned int rejects = 0;
  //BIRL iterations 
  for(unsigned int itr = 1; itr < chain_length; itr++)
  {
    // deepcopy ?
    total_steps++;

    MDP* temp_mdp = mdp->deepcopy(); //mdp->getGridWidth(),mdp->getGridHeight());
    //temp_mdp->setTransitions(mdp->getTransitions());
    //temp_mdp->setTerminalStates(mdp->getTerminalStates());
    //temp_mdp->setRewards(mdp->getRewards());

    
    if( (rejects/(double)(itr+2)) <= 0.4 ) step_size *= 1.05;
    else if ( (rejects/(double)(itr+2)) >= 0.5 ) step_size /= 1.05;
    //else cout << "#iteration reached optimal acceptance rate: " << itr << endl;
    modifyRewardRandomly(temp_mdp,step_size);

    temp_mdp->valueIteration(0.001, mdp->getValues());
    //temp_mdp->deterministicPolicyIteration(policy);//valueIteration(0.05);
    temp_mdp->calculateQValues();

    double new_posterior = calculatePosterior(temp_mdp);
    //cout << "posterior: " << new_posterior << endl;
    double probability = min((double)1.0, exp(new_posterior - posterior));

    if ( ((double) rand() / (RAND_MAX)) < probability ) //policy_changed && 
    {
      delete mdp;
      mdp = temp_mdp->deepcopy();
      
      posterior = new_posterior;
      R_chain[itr] = temp_mdp;
      posteriors[itr] = exp(new_posterior);
      
      if(posteriors[itr] > MAPposterior)
      {
        MAPposterior = posteriors[itr];
        
        delete MAPmdp;
        MAPmdp = mdp->deepcopy();
      }
    }else {
      itr--;
      rejects++;
      delete temp_mdp;
    }
    //cout << "rejection rate: " << rejects / (double)(itr+2) << endl;
  }

  //cout << "chain_length:" << chain_length << ", rejects: " << rejects << endl;

}

void BIRL::removeAllDemostrations()
{
  positive_demonstration.clear();
  negative_demonstration.clear();
}


void BIRL::removeDemonstration(pair<unsigned int,unsigned int> s_a)
{
  positive_demonstration.erase(std::remove(positive_demonstration.begin(), positive_demonstration.end(), s_a), positive_demonstration.end());
  negative_demonstration.erase(std::remove(negative_demonstration.begin(), negative_demonstration.end(), s_a), negative_demonstration.end());
}

double BIRL::logsumexp(double* nums, unsigned int size) {
  double max_exp = nums[0];
  double sum = 0.0;
  unsigned int i;

  for (i = 1 ; i < size ; i++)
  {
    if (nums[i] > max_exp)
      max_exp = nums[i];
  }

  for (i = 0; i < size ; i++)
    sum += exp(nums[i] - max_exp);

  return log(sum) + max_exp;
}

double BIRL::calculatePosterior(MDP* gmdp, double alpha) //assuming uniform prior
{

  double posterior = 0;
  unsigned int state, action;
  unsigned int numActions = gmdp->getNumActions();

  // "-- Positive Demos --" 
  for(unsigned int i=0; i < positive_demonstration.size(); i++)
  {
    pair<unsigned int,unsigned int> demo = positive_demonstration[i];
    state =  demo.first;
    action = demo.second; 

    double Z [numActions]; //
    for(unsigned int a = 0; a < numActions; a++) Z[a] = alpha*(gmdp->getQValue(state,a));
    posterior += alpha*(gmdp->getQValue(state,action)) - logsumexp(Z, numActions);
    //cout << state << "," << action << ": " << posterior << endl;
  }

  // "-- Negative Demos --" 
  for(unsigned int i=0; i < negative_demonstration.size(); i++)
  {
    pair<unsigned int,unsigned int> demo = negative_demonstration[i];
    state =  demo.first;
    action = demo.second;
    double Z [numActions]; //
    for(unsigned int a = 0; a < numActions; a++)  Z[a] = alpha*(gmdp->getQValue(state,a));

    unsigned int ct = 0;
    double Z2 [numActions - 1]; 
    for(unsigned int a = 0; a < numActions; a++) 
    {
      if(a != action) Z2[ct++] = alpha*(gmdp->getQValue(state,a));
    }

    posterior += logsumexp(Z2, numActions-1) - logsumexp(Z, numActions);
  }
  //cout << "posterior" << posterior << endl;
  for(unsigned int i=0; i < unknown_demonstration.size(); i++)
  {
    pair<unsigned int,unsigned int> demo = unknown_demonstration[i];
    state =  demo.first;
    action = demo.second;

    double Z [numActions]; //
    for(unsigned int a = 0; a < numActions; a++)  Z[a] = alpha*(gmdp->getQValue(state,a));

    unsigned int ct = 0;
    double Z2 [numActions - 1]; 
    for(unsigned int a = 0; a < numActions; a++) 
    {
      if(a != action) Z2[ct++] = alpha*(gmdp->getQValue(state,a));
    }

    if( (rand() % 1000) / 1000 > unknown_probabilities[i] ) posterior += logsumexp(Z2, numActions-1) - logsumexp(Z, numActions);
    else  posterior += alpha*(gmdp->getQValue(state,action)) - logsumexp(Z, numActions);
  }
  return posterior;
}

void BIRL::modifyRewardRandomly(MDP * gmdp, double step)
{
  unsigned int state = rand() % gmdp->getNumStates();
  double change = pow(-1,rand()%2)*step;
  //cout << "before " << gmdp->getReward(state) << endl;
  //cout << "change " << change << endl;
  double reward = max(min(gmdp->getReward(state) + change, r_max), r_min);
  //if(gmdp->isTerminalState(state)) reward = max(min(gmdp->getReward(state) + change, r_max), 0.0);
  //else reward = max(min(gmdp->getReward(state) + change, 0.0), r_min); 
  //cout << "after " << reward << endl;
  gmdp->setReward(state,reward);
}

void BIRL::addPositiveDemos(vector<pair<unsigned int,unsigned int> > demos)
{
  for(unsigned int i=0; i < demos.size(); i++)  positive_demonstration.push_back(demos[i]);
  //positive_demonstration.insert(positive_demonstration.end(), demos.begin(), demos.end());
}
void BIRL::addNegativeDemos(vector<pair<unsigned int,unsigned int> > demos)
{
  for(unsigned int i=0; i < demos.size(); i++)  negative_demonstration.push_back(demos[i]);
  //negative_demonstration.insert(negative_demonstration.end(), demos.begin(), demos.end());
}

void BIRL::displayDemos()
{
  displayPositiveDemos();
  displayNegativeDemos();
}

void BIRL::displayPositiveDemos()
{
  if(positive_demonstration.size() !=0 ) cout << "\n-- Positive Demos --" << endl;
  for(unsigned int i=0; i < positive_demonstration.size(); i++)
  {
    pair<unsigned int,unsigned int> demo = positive_demonstration[i];
    cout << " {" << demo.first << "," << demo.second << "}, "; 

  }
  cout << endl;
}
void BIRL::displayNegativeDemos()
{
  if(negative_demonstration.size() != 0) cout << "\n-- Negative Demos --" << endl;
  for(unsigned int i=0; i < negative_demonstration.size(); i++)
  {
    pair<unsigned int,unsigned int> demo = negative_demonstration[i];
    cout << " {" << demo.first << "," << demo.second << "}, "; 

  }
  cout << endl;
}
void BIRL::initializeMDP()
{
  double* rewards = new double[mdp->getNumStates()];
  for(unsigned int s=0; s<mdp->getNumStates(); s++)
  {
    rewards[s] = (r_min+r_max)/2;
  }
  mdp->setRewards(rewards);
  delete []rewards;


}

bool BIRL::isDemonstration(pair<unsigned int,unsigned int> s_a)
{
  for(unsigned int i=0; i < positive_demonstration.size(); i++)
  {
    if(positive_demonstration[i].first == s_a.first && positive_demonstration[i].second == s_a.second) return true;
  }
  for(unsigned int i=0; i < negative_demonstration.size(); i++)
  {
    if(negative_demonstration[i].first == s_a.first && negative_demonstration[i].second == s_a.second) return true;
  }
  return false;

}


#endif
