
#ifndef mdp_h
#define mdp_h

#include <cstddef>
#include <cmath>
#include <stdlib.h>
#include <vector>
#include <set>
#include <algorithm>
#include <limits>
#include <assert.h> 


using namespace std;


//computes the dot product between two vectors
double dotProduct(double x[], double y[], int length)
{
    double result = 0;
    for(int i=0; i<length; i++)
        result += x[i] * y[i];
    return result;
}

class State {
    public:
        double * features;
        State(double* in_features, unsigned int numFeatures) {
           features = new double[numFeatures];
           for(unsigned int ft=0; ft < numFeatures; ft++) features[ft] = in_features[ft];
        };
};

class MDP { // General continuous MDP

  protected:
    double discount;
    double stepSize;
    vector<State*> initialStates;
    vector<State*> terminalStates;
    double * featureWeights;
    unsigned int numFeatures;
    double beta;

    // 16 different actions each moves 22.5 degrees clockwise from up north
    enum Action {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, NUM_ACTIONS}; 

  public:
    MDP(double gamma, double step_size, unsigned int num_features, double * feature_weights): discount(gamma), stepSize(step_size), numFeatures(num_features){ 
        featureWeights = new double[numFeatures];
        for(unsigned int ft=0; ft < numFeatures; ft++) featureWeights[ft] = feature_weights[ft];
        beta = M_PI/NUM_ACTIONS;
    };
    ~MDP(){ delete [] featureWeights; };
    MDP* deepcopy(){
        MDP* copy = new MDP(discount, stepSize, numFeatures, featureWeights);
        return copy;
    };

    void addTerminalState(State* terminal){ 
      terminalStates.push_back(terminal);         
    };
    void addInitialState(State* initial){ 
      initialStates.push_back(initial); };

    vector<State*> getInitialStates(){return initialStates;};
    vector<State*> getTerminalStates(){return terminalStates;};

    void valueIteration(double eps);

    double getDiscount(){return discount;};
    double getReward(State* s){ return dotProduct(featureWeights,s->features,numFeatures);};
    State* getTransition(State* s, unsigned int action);

    double getValue(State* state){ return 0; }; //TODO
    double getQValue(State* state,unsigned int action){ return 0;};//TODO

    friend bool operator== (MDP & lhs, MDP & rhs);
    bool isOptimalAction(State* state, unsigned int action);
    void getOptimalActions(State* state, vector<unsigned int> & actions);
    double * getFeatureWeights(){ return featureWeights; }
    unsigned int getNumFeatures(){ return numFeatures; }

};


State* MDP::getTransition(State* s, unsigned int action){
    // assuming State features[0:1] denotes 2D position (x,y)
    State* next_s = new State(s->features,numFeatures); 
    next_s->features[0] += stepSize*sin(beta*action);
    next_s->features[1] += stepSize*cos(beta*action);
    return next_s;
}

bool MDP::isOptimalAction(State* state, unsigned int action)
{
  double max_q = numeric_limits<double>::lowest();
  for(unsigned int a = A0; a < NUM_ACTIONS; a++)
  {
    if( getQValue(state,a) > max_q )
    {
      max_q  = getQValue(state,a);
    }
  }
  if( getQValue(state,action) == max_q) return true;
  return false;

}

void MDP::getOptimalActions(State* state, vector<unsigned int> & actions)
{
    double max_q = numeric_limits<double>::lowest();
    for(unsigned int a = A0; a < NUM_ACTIONS; a++)
    {
      if( getQValue(state,a) > max_q )
      {
        max_q  = getQValue(state,a);
      }
    }
    for(unsigned int a = A0; a < NUM_ACTIONS; a++)
    {
      if( getQValue(state,a) == max_q ) actions.push_back(a);
    }
      
}


bool operator== (MDP & lhs, MDP & rhs)
{
  double* F1 = lhs.getFeatureWeights();
  double* F2 = rhs.getFeatureWeights();
  for(unsigned int s = 0; s < lhs.getNumFeatures(); s++){
    if(F1[s] != F2[s]) return false;
  }
  return true;

}

#endif
