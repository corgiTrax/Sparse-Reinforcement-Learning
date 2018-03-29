
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


class MDP { // General MDP

  protected:
    unsigned int numActions;
    unsigned int numStates;
    double discount;
    bool* initialStates = nullptr;
    bool* terminalStates = nullptr;

    double* R = nullptr; 
    double* V = nullptr;
    double** Q = nullptr;

    double*** T = nullptr;
    enum actions {UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT};


  public:
    MDP(double gamma, int states, int actions): numActions(actions), numStates(states), discount(gamma){

      initialStates = new bool [numStates];
      fill_n(initialStates, numStates, false);

      terminalStates = new bool [numStates];
      fill_n(terminalStates, numStates, false);

      //initialize to all zeros
      // cout << "initializing T" <<endl;
      
      T = new double**[numStates];
      for(unsigned int s1 = 0; s1 < numStates; s1++)
      {
        T[s1] = new double*[numActions];
        for(unsigned int a = 0; a < numActions; a++)
        {
          T[s1][a] = new double[numStates];
          for(unsigned int p = 0; p < numStates; p++) T[s1][a][p] = 0;
        }
      }
      
      R = new double[numStates];
      fill_n(R, numStates, 0.0);
      //cout << R << endl;
      
      Q = new double*[numStates];
      for(unsigned int s = 0; s < numStates; s++) Q[s] = new double[numActions];
      
      V = new double[numStates];
      fill_n(V, numStates, 0.0);
      

    };

    ~MDP(){
      //cout << R << endl;

      if(R != nullptr) delete[] R;
      if(V != nullptr) delete[] V;

      if(Q != nullptr){
        for(unsigned int s = 0; s < numStates; s++) delete[] Q[s];
        delete[] Q;
      }

      if(T != nullptr){
          for(unsigned int s1 = 0; s1 < numStates; s1++)
          {
            for(unsigned int a = 0; a < numActions; a++)
            {
              delete[] T[s1][a];
            }
            delete[] T[s1];
          }
          delete[] T;
      }
      
      if(initialStates != nullptr) delete [] initialStates;

      if(terminalStates != nullptr) delete [] terminalStates;
    };
    
    MDP* deepcopy(){
        MDP* copy = new MDP(discount, numStates, numActions);
        copy -> setInitialStates(initialStates);
        copy -> setTerminalStates(terminalStates);
        copy -> setRewards(R);
        copy -> setTransitions(T);
        return copy;
    };

    void setInitialStates(bool* initials){ 
      if(initials == nullptr) return;
      for(unsigned int s = 0; s < numStates; s++) initialStates[s] = initials[s];
    };

    void setTerminalStates(bool* terminals){ 
      if(terminals == nullptr) return;
      for(unsigned int s = 0; s < numStates; s++){
        terminalStates[s] = terminals[s];
      }
    };

    void addTerminalState(unsigned int terminal){ 
      terminalStates[terminal] = true;         
    };

    void addInitialState(unsigned int initial){ 
      initialStates[initial] = true; };



    bool* getInitialStates(){return initialStates;};
    bool* getTerminalStates(){return terminalStates;};

    bool isInitialState(unsigned int s){ return initialStates[s];}
    bool isTerminalState(unsigned int s){ return terminalStates[s];}

    void setNumActions(unsigned int actions){ numActions = actions; };
    unsigned int getNumActions() { return numActions; };
    void setNumStates(unsigned int states){ numStates = states; };
    unsigned int getNumStates(){ return numStates; };

    void displayRewards(){};
    void displayRewards(unsigned int width);
    void displayPolicy(vector<unsigned int> & policy, int width);
    void deterministicPolicyIteration(vector<unsigned int> & policy);
    void deterministicPolicyEvaluation(vector<unsigned int> & policy, int k=20); //Default argument
    void initRandDeterministicPolicy(vector<unsigned int> & policy);
    void valueIteration(double eps, double* input_v); //warm start
    void valueIteration(double eps);

    void setReward(int state, double reward){ R[state] = reward;};
    void setRewards(double*  rewards) { 
      for(unsigned int s = 0; s < numStates; s++) R[s] = rewards[s];
    };
    double* getRewards(){ return R; };
    double getDiscount(){return discount;};
    double getReward(unsigned int state) 
    { 
      if(R != nullptr) return R[state];
      else {
        cout << "Reward for state not defined!" << endl;
        return 0.0;
      }
    };

    //void setTransitions(vector<vector<list<pair<int,double> > > > transitions){ T = transitions; }
    //list<pair<int,double> > getTransitions(int state, int action) {return T[state][action];}
    void setTransitions(double*** transitions){ 
      for(unsigned int s1 = 0; s1 < numStates; s1++)
      {
        for(unsigned int a = 0; a < numActions; a++)
        {
          for(unsigned int p = 0; p < numStates; p++) T[s1][a][p] = transitions[s1][a][p] ;
        }
      }
    };

    double *** getTransitions(){return T;}

    void calculateQValues();

    double* getValues(){ return V; };
    double getValue(unsigned int state){ return V[state]; };
    double getQValue(unsigned int state,unsigned int action){ return Q[state][action];};

    double** getQValues() { return Q;};
    
    void setVValues(double* in_V){
        for(unsigned int s1 = 0; s1 < numStates; s1++)
        {
            V[s1] = in_V[s1];
        }
    }
    
    void setQValues(double** in_Q){
        for(unsigned int s1 = 0; s1 < numStates; s1++)
        {
            for(unsigned int a = 0; a < numActions; a++)
            {
              Q[s1][a] = in_Q[s1][a];
            }
        }
    }

    friend bool operator== (MDP & lhs, MDP & rhs);
    bool isOptimalAction(unsigned int state, unsigned int action);
    void getOptimalPolicy(vector<unsigned int> & opt);
    void getOptimalActions(unsigned int state, vector<unsigned int> & actions);

};


class GridMDP: public MDP{ // 2D Grid MDP - defined by width*height

  protected:
    unsigned int gridWidth;
    unsigned int gridHeight;
    const static unsigned int NUM_ACTIONS=8;
    enum actions {UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT};

  public:
    GridMDP(unsigned int width, unsigned int height, double gamma=0.95): MDP(gamma,width*height,NUM_ACTIONS), gridWidth(width), gridHeight(height){ 
      setDeterministicGridTransitions();
    };
    
    GridMDP(unsigned int width, unsigned int height, vector<unsigned int> initStates, vector<unsigned int> termStates, double gamma=0.95): MDP(gamma,width*height,NUM_ACTIONS), gridWidth(width), gridHeight(height){ 
            for(unsigned int i=0; i<initStates.size(); i++)
            {
                int idx = initStates[i];
                initialStates[idx] = true;
            }
            for(unsigned int i=0; i<termStates.size(); i++)
            {
                int idx = termStates[i];
                terminalStates[idx] = true; 
            }
            setDeterministicGridTransitions();
};

     GridMDP(unsigned int width, unsigned int height, bool* initStates, bool* termStates, double gamma=0.95): MDP(gamma,width*height,NUM_ACTIONS), gridWidth(width), gridHeight(height){ 
            for(unsigned int i=0; i<numStates; i++)
            {
                initialStates[i] = initStates[i];
            }
            for(unsigned int i=0; i<numStates; i++)
            {
                terminalStates[i] = termStates[i]; 
            }
            setDeterministicGridTransitions();
    };
    
    int getGridWidth() { return gridWidth;};
    int getGridHeight(){ return gridHeight;};
    void displayRewards();
    void setDeterministicGridTransitions();
    void displayTransitions();
    void displayPolicy(vector<unsigned int> & policy);

    vector<unsigned int> getValidActions(unsigned int s){
      vector<unsigned int> actions;
      //actions.push_back(STAY);
      if(terminalStates[s]) return actions;
      if(s >= gridWidth) {
        actions.push_back(UP);
        if(s % gridWidth > 0) actions.push_back(UP_LEFT);
        if(s % gridWidth < gridWidth - 1) actions.push_back(UP_RIGHT);
        }
      if(s < (gridHeight - 1) * gridWidth){
        actions.push_back(DOWN);
        if(s % gridWidth > 0) actions.push_back(DOWN_LEFT);
        if(s % gridWidth < gridWidth - 1) actions.push_back(DOWN_RIGHT);
        }
      if(s % gridWidth > 0) actions.push_back(LEFT);
      if(s % gridWidth < gridWidth - 1) actions.push_back(RIGHT);
      return actions;
    };

    unsigned int getNextState(unsigned int s, unsigned int a){
      if(terminalStates[s]) return s;
      if(a == UP && s >= gridWidth) return s - gridWidth;
      else if(a == DOWN && s < (gridHeight - 1) * gridWidth) return s + gridWidth;
      else if(a == LEFT && s % gridWidth > 0) return s - 1;
      else if(a == RIGHT && s % gridWidth < gridWidth - 1) return s + 1;
      else if(a == UP_LEFT && s >= gridWidth  && s % gridWidth > 0 ) return s - gridWidth - 1;
      else if(a == UP_RIGHT && s >= gridWidth  && s % gridWidth < gridWidth - 1 ) return s - gridWidth + 1;
      else if(a == DOWN_LEFT && s < (gridHeight - 1) * gridWidth && s % gridWidth > 0) return s + gridWidth - 1;
      else if(a == DOWN_RIGHT && s < (gridHeight - 1) * gridWidth && s % gridWidth < gridWidth - 1) return s + gridWidth + 1;
      else return s;
    }           

    void setTerminalStates(bool* terminals){ 
      if(terminals == nullptr) return;
      for(unsigned int s = 0; s < numStates; s++){
        terminalStates[s] = terminals[s];

        if(terminalStates[s])
        {
          if(s >= gridWidth) T[s][UP][s - gridWidth] = 0.0;
          if(s < (gridHeight - 1) * gridWidth) T[s][DOWN][s + gridWidth] = 0.0;
          if(s % gridWidth > 0) T[s][LEFT][s - 1] = 0.0;
          if(s % gridWidth < gridWidth - 1) T[s][RIGHT][s + 1] = 0.0;
          T[s][UP][s] = 0.0;
          T[s][DOWN][s] = 0.0;
          T[s][LEFT][s] = 0.0; 
          T[s][RIGHT][s] = 0.0;
        }
      }
    };

    void addTerminalState(unsigned int terminal){ 
      terminalStates[terminal] = true; 
      unsigned int s = terminal;
      if(s >= gridWidth) T[s][UP][s - gridWidth] = 0.0;
      if(s < (gridHeight - 1) * gridWidth) T[s][DOWN][s + gridWidth] = 0.0;
      if(s % gridWidth > 0) T[s][LEFT][s - 1] = 0.0;
      if(s % gridWidth < gridWidth - 1) T[s][RIGHT][s + 1] = 0.0;
      T[s][UP][s] = 0.0;
      T[s][DOWN][s] = 0.0;
      T[s][LEFT][s] = 0.0; 
      T[s][RIGHT][s] = 0.0;

    };        
    
    void displayValues()
    {
        assert(R != nullptr);
    //    if (R == nullptr){
    //      cout << "ERROR: no values!" << endl;
    //      return;
    //     }
        for(unsigned int r = 0; r < gridHeight; r++)
        {
            for(unsigned int c = 0; c < gridWidth; c++)
            {
                unsigned int state = r*gridWidth + c;
                cout << setiosflags(ios::fixed)
                << setprecision(3)
                << V[state] << "  ";
            }
            cout << endl;
        }
    }

};


//Extension of GridMDP to allow state rewards to be linear combo of features
class FeatureGridMDP: public GridMDP{
   
    private:
        int numFeatures;
        double* featureWeights = nullptr;  //keeps a local copy of weights
        double** stateFeatures = nullptr;  //just a pointer to where they are defined initially...
           
   
    public:
        FeatureGridMDP(unsigned int width, unsigned int height, vector<unsigned int> initStates, vector<unsigned int> termStates, unsigned int nFeatures, double* fWeights, double** sFeatures, double gamma=0.95): GridMDP(width, height, initStates, termStates, gamma), numFeatures(nFeatures)
        {
            featureWeights = new double[numFeatures];
            stateFeatures = new double* [width*height];
            for(unsigned int i=0; i<numFeatures; i++)
                featureWeights[i] = fWeights[i];
            for(unsigned int i=0; i<width*height; i++)
             {   stateFeatures[i] = new double[numFeatures];
                for(unsigned int f=0; f<numFeatures;f++) stateFeatures[i][f] = sFeatures[i][f];
               }
            //compute cached rewards
            computeCachedRewards();
                        
        };
        
        FeatureGridMDP(unsigned int width, unsigned int height, bool* initStates, bool* termStates, unsigned int nFeatures, double* fWeights, double** sFeatures, double gamma=0.95): GridMDP(width, height, initStates, termStates, gamma), numFeatures(nFeatures)
        {
            featureWeights = new double[numFeatures];
            for(int i=0; i<numFeatures; i++)
                featureWeights[i] = fWeights[i];
            stateFeatures = new double* [width*height];
            for(unsigned int i=0; i<numFeatures; i++)
                featureWeights[i] = fWeights[i];
            for(unsigned int i=0; i<width*height; i++)
             {   stateFeatures[i] = new double[numFeatures];
                for(unsigned int f=0; f<numFeatures;f++) stateFeatures[i][f] = sFeatures[i][f];
               }
            computeCachedRewards();
        };
        
        FeatureGridMDP* deepcopy(){
                FeatureGridMDP* copy = new FeatureGridMDP(gridWidth, gridHeight, initialStates, terminalStates, numFeatures, featureWeights, stateFeatures, discount);
                //copy -> setVValues(V);
                //copy -> setQValues(Q);
                return copy;
         };
         
        void setFeatureAtState(unsigned int s, double * features){
             //cout << "Setting features for state " << s << endl;
             for(unsigned int f=0; f<numFeatures;f++) stateFeatures[s][f] = features[f];
        };

        long double L2_distance(FeatureGridMDP* in_mdp)
        {
            long double dist = 0;
            for(unsigned int i = 0; i < numStates; i++)
            {
               //cout << R[i] <<";" << in_mdp->R[i] << endl;
               dist += pow(R[i] - in_mdp->R[i], 2); 
            }
            if(dist > 10000)
            {
                cout << " ????!!!!! ------> " << endl;
                displayRewards();
                in_mdp->displayRewards();
            }
            return sqrt(dist);
        }
         
        void computeCachedRewards()
        {
            //cout << "precomputing rewards" << endl;
            for(unsigned int s = 0; s < numStates; s++) 
                R[s] = dotProduct(stateFeatures[s], featureWeights, numFeatures);
            //displayRewards();
        };
        
        //delete featureWeights
        //stateFeatures should be deleted in main function somewhere in test script
        ~FeatureGridMDP()
        {
            delete[] featureWeights;
             for(unsigned int i=0; i<gridWidth*gridHeight; i++)
                delete[] stateFeatures[i];
            delete[] stateFeatures;
        
        };
        unsigned int getNumFeatures(){return numFeatures;};
        double* getFeatureWeights(){ return featureWeights; };
        void displayFeatureWeights(){
           cout << "Feature Weights: " ;
           cout.precision(10);
           for(int i=0; i < numFeatures; i++) cout << featureWeights[i] << ", ";
           cout << endl;
        };
        double** getStateFeatures(){ return stateFeatures; };
        void setFeatureWeight(unsigned int feat, double weight)
        {
            featureWeights[feat] = weight;
            //cout << "changed weights to" << endl;
            //for(int i=0; i<numFeatures; i++)
            //    cout << featureWeights[i] << " ";
            //cout << endl;
            computeCachedRewards();
        };
        //multiply features by weights for state s
        double getReward(unsigned int s)
        {
            //use precomputed rewards
            return getCachedReward(s);
            //
            //return dotProduct(stateFeatures[s], featureWeights, numFeatures);
        };
        double getCachedReward(unsigned int s)
        {
            //cout << "getting cached reward" << endl;
            return R[s];
        }
        void setFeatureWeights(double* fWeights)
        {
            for(int i=0; i<numFeatures-1; i++)
                featureWeights[i] = fWeights[i];
            featureWeights[numFeatures-1] = -0.1; //Last feature set to be -0.1, representing regular cell HAX TODO
            computeCachedRewards();
        };
        double getWeight(unsigned int state){ return featureWeights[state]; };
        void valueIteration(double eps);

};



bool MDP::isOptimalAction(unsigned int state, unsigned int action)
{
  calculateQValues();
  double max_q = numeric_limits<double>::lowest();
  for(unsigned int a = 0; a < numActions; a++)
  {
    if( Q[state][a] > max_q )
    {
      max_q  = Q[state][a];
    }
  }
  if( Q[state][action] == max_q) return true;
  return false;

}

void MDP::getOptimalActions(unsigned int state, vector<unsigned int> & actions)
{
    calculateQValues();
    //double max_q = 0;
    double max_q = numeric_limits<double>::lowest();
    for(unsigned int a = 0; a < numActions; a++)
    {
      if( Q[state][a] > max_q )
      {
        max_q  = Q[state][a];
      }
    }
    //cout << "max q value:" << max_q << endl;
    for(unsigned int a = 0; a < numActions; a++)
    {
      if( Q[state][a] == max_q ) actions.push_back(a);
    }
      
}


void MDP::getOptimalPolicy(vector<unsigned int> & opt)
{
  calculateQValues();
  for(unsigned int s = 0; s < numStates; s++)
  {
    //double max_q = 0;
    double max_q = numeric_limits<double>::lowest();
    unsigned int max_action = 0;
    for(unsigned int a = 0; a < numActions; a++)
    {
      if( Q[s][a] > max_q )
      {
        max_q  = Q[s][a];
        max_action = a;
      }
    }
    opt[s] = max_action;      
  }
}


void MDP::calculateQValues()
{
  if(R == nullptr) 
  {
    cout << "[ERROR] Reward has not been initialized!" << endl;
    return;
  }
  if(T == nullptr) 
  {
    cout << "[ERROR] Transition matrix has not been initialized!" << endl;
    return;
  }
  
  for(unsigned int s = 0; s < numStates; s++)
  {
    for(unsigned int a = 0; a < numActions; a++)
    {
      Q[s][a] = R[s];
      for(unsigned int s2 = 0; s2 < numStates; s2++)
      {
        Q[s][a] += discount * T[s][a][s2] * V[s2];
      }
    }
  }


}


void MDP::displayPolicy(vector<unsigned int> & policy, int width)
{
  for(unsigned int count = 0; count < numStates; count++)
  {
    cout << setiosflags(ios::fixed);
    if(count % width == 0) cout << endl;
    if(isTerminalState(count)) cout << "*" << "  ";
   // else if(policy[count]==STAY) cout << "-" << "  ";
    else if(policy[count]==UP) cout << "^" << "  ";
    else if(policy[count]==DOWN) cout << "v" << "  ";
    else if(policy[count]==LEFT) cout << "<" << "  ";
    else if(policy[count]==RIGHT) cout << ">" << "  ";
    else if(policy[count]==UP_LEFT) cout << "L" << "  ";
    else if(policy[count]==UP_RIGHT) cout << "R" << "  ";
    else if(policy[count]==DOWN_LEFT) cout << "l" << "  ";
    else if(policy[count]==DOWN_RIGHT) cout << "r" << "  ";
    else cout << "?" << "  ";

  }

}

void GridMDP::displayPolicy(vector<unsigned int> & policy)
{
  unsigned int count = 0;
  for(unsigned int r = 0; r < gridHeight; r++)
  {
    for(unsigned int c = 0; c < gridWidth; c++)
    {
     cout << setiosflags(ios::fixed);
    if(isTerminalState(count)) cout << "*" << "  ";
    //else if(policy[count]==STAY) cout << "-" << "  ";
    else if(policy[count]==UP) cout << "^" << "  ";
    else if(policy[count]==DOWN) cout << "v" << "  ";
    else if(policy[count]==LEFT) cout << "<" << "  ";
    else if(policy[count]==RIGHT) cout << ">" << "  ";
    else if(policy[count]==UP_LEFT) cout << "L" << "  ";
    else if(policy[count]==UP_RIGHT) cout << "R" << "  ";
    else if(policy[count]==DOWN_LEFT) cout << "l" << "  ";
    else if(policy[count]==DOWN_RIGHT) cout << "r" << "  ";
    else cout << "?" << "  ";
      count++;
    }
    cout << endl;
  }

}

void GridMDP::displayTransitions()
{
  cout << "-------- UP ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][UP][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- DOWN ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][DOWN][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- LEFT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][LEFT][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- RIGHT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][RIGHT][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- UP_LEFT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][UP_LEFT][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- UP_RIGHT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][UP_RIGHT][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- DOWN_LEFT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][DOWN_LEFT][s2] << " ";
        }
        cout << endl;
    }
    cout << "-------- DOWN_RIGHT ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][DOWN_RIGHT][s2] << " ";
        }
        cout << endl;
    }
    
    /*cout << "-------- STAY ----------" << endl;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
            cout << setiosflags(ios::fixed)
                 << setprecision(2)
                 << T[s1][STAY][s2] << " ";
        }
        cout << endl;
    }*/
}


void MDP::initRandDeterministicPolicy(vector<unsigned int> & policy)
{
  for(unsigned int s = 0; s < numStates; s++)
  {
    policy[s] = rand() % numActions;
  }
}


void MDP::deterministicPolicyIteration(vector<unsigned int> & policy)
{
  //generate random policy
  initRandDeterministicPolicy(policy);
  bool policyUnchanged = false;
  while(!policyUnchanged)
  {
    //update values based on current policy
    deterministicPolicyEvaluation(policy); //uses default value of k=20 for now
    //run policy improvement
    policyUnchanged = true;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
      //find expected utility of best action in s1 (undiscounted and reward in s1 doesn't matter ) (see R&N 657)
      //along the way also keep track of expected utility of taking policy action
      //also remember the best action
      double maxActionValue = numeric_limits<double>::lowest();
      double policyActionValue = 0;
      unsigned int bestAction = -1;
      for(unsigned int a = 0; a < numActions; a++)
      {
        //calculate expected utility of taking action a in state s1
        double expUtil = 0;
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
          expUtil += T[s1][a][s2] * V[s2];
        }
        if(expUtil > maxActionValue)
        {
          bestAction = a;
          maxActionValue = expUtil;
        }
        //remember how well current policy action does
        if(a == policy[s1])
          policyActionValue = expUtil;
      }
      //check if policy needs to be updated
      if(maxActionValue > policyActionValue)
      {
        policy[s1] = bestAction;
        policyUnchanged = false;
      }
    }
  }
}

//see how well a specific policy performs on mdp by updating state values k times
//TODO: currently assumes a deterministic policy! Should eventually make it stochastic
void MDP::deterministicPolicyEvaluation(vector<unsigned int> & policy, int k)
{
  for(int iter = 0; iter < k; iter++)
  {
    //update value of each state
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
      double tempV = 0;
      //add reward
      tempV += R[s1];
      //add discounted expected value after taking policy action
      unsigned int policyAction = policy[s1];
      double expUtil = 0;
      for(unsigned int s2 = 0; s2 < numStates; s2++)
      {
        expUtil += T[s1][policyAction][s2] * V[s2];
      }
      tempV += discount * expUtil;
      V[s1] = tempV;
    }
  }
}


//runs value iteration, Note: it sets V to zero at start so won't work with a warm start
void FeatureGridMDP::valueIteration(double eps)
{
  //initialize values to zero
  //cout << "here in value iteration!" << endl;
  double delta = 0;
  for(unsigned int s = 0; s < numStates; s++)
  {
    V[s] = R[s];
  }
  double* new_V = new double[numStates];
  //repeat until convergence within error eps
  do
  {
    delta = 0;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
      new_V[s1] = R[s1];
      //add discounted max over actions of value of next state
      double maxActionValue = -1000000;
      for(unsigned int a = 0; a < numActions; a++)
      {
        //cout << s1 << "," << a << "; ";
        //calculate expected utility of taking action a in state s1
        unsigned int s2=  getNextState(s1,a);
        double expUtil = T[s1][a][s2] * V[s2];
        if(expUtil > maxActionValue)
          maxActionValue = expUtil;
      }
      new_V[s1] += discount * maxActionValue;

      //update delta to track convergence
      double absDiff = abs(new_V[s1] - V[s1]);
      if(absDiff > delta) delta = absDiff;
    }
    
    for(unsigned int s = 0; s < numStates; s++) V[s] = new_V[s];
    
  }
  while( delta > eps * (1 - discount) / discount);
  delete new_V;
}


//runs value iteration, Note: it sets V to zero at start so won't work with a warm start
void MDP::valueIteration(double eps)
{
  //initialize values to zero
  double delta;
  for(unsigned int s = 0; s < numStates; s++)
  {
    V[s] = 0;
  }
  //repeat until convergence within error eps
  do
  {
    //cout << "--------" << endl;
    //displayAsGrid(V);
    
    //update value of each state
    cout.precision(5);
    cout << eps << "," << delta << endl;
    delta = 0;
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
      double tempV = 0;
      //add reward
      tempV += R[s1];
       //cout << "here" << endl;
      //add discounted max over actions of value of next state
      double maxActionValue = -10000;
      for(unsigned int a = 0; a < numActions; a++)
      {
        //cout << "here2" << endl;
        //calculate expected utility of taking action a in state s1
        double expUtil = 0;
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
          expUtil += T[s1][a][s2] * V[s2];
        }
        if(expUtil > maxActionValue)
          maxActionValue = expUtil;
      }
      tempV += discount * maxActionValue;

      //update delta to track convergence
      double absDiff = abs(tempV - V[s1]);
      if(absDiff > delta)
        delta = absDiff;
      V[s1] = tempV;
    }

  }
  while( delta > eps); // * (1 - discount) / discount);
}

void MDP::valueIteration(double eps, double* input_v) //warm start
{
  //initialize values to zero
  double delta;

  for(unsigned int s = 0; s < numStates; s++)
  {
    V[s] = input_v[s];
  }
  //repeat until convergence within error eps
  do
  {
    delta = 0;
    //update value of each state
    for(unsigned int s1 = 0; s1 < numStates; s1++)
    {
      double tempV = 0;
      //add reward
      tempV += R[s1];
      // cout << "here" << endl;
      //add discounted max over actions of value of next state
      double maxActionValue = -10000;
      for(unsigned int a = 0; a < numActions; a++)
      {
        //cout << "here2" << endl;
        //calculate expected utility of taking action a in state s1
        double expUtil = 0;
        for(unsigned int s2 = 0; s2 < numStates; s2++)
        {
          expUtil += T[s1][a][s2] * V[s2];
        }
        if(expUtil > maxActionValue)
          maxActionValue = expUtil;
      }
      tempV += discount * maxActionValue;

      //update delta to track convergence
      double absDiff = abs(tempV - V[s1]);
      if(absDiff > delta)
        delta = absDiff;
      V[s1] = tempV;
    }

  }
  while(delta > eps * (1 - discount) / discount);
}

void GridMDP::setDeterministicGridTransitions() //specific to grid MDP
{

   for(unsigned int s = 0; s < numStates; s++)
    {
        //UP
        if(s >= gridWidth)
            T[s][UP][s - gridWidth] = 1.0;
        else
            T[s][UP][s] = 1.0;

        //DOWN
        if(s < (gridHeight - 1) * gridWidth)
            T[s][DOWN][s + gridWidth] = 1.0;
        else
            T[s][DOWN][s] = 1.0;


        //LEFT
        if(s % gridWidth > 0)
            T[s][LEFT][s - 1] = 1.0;
        else
            T[s][LEFT][s] = 1.0;


        //RIGHT
        if(s % gridWidth < gridWidth - 1)
            T[s][RIGHT][s + 1] = 1.0;
        else
            T[s][RIGHT][s] = 1.0;

        // UP_LEFT
        if(s >= gridWidth  && s % gridWidth > 0 )
            T[s][UP_LEFT][s - gridWidth - 1] = 1.0;
        else
            T[s][UP_LEFT][s] = 1.0;

        // UP_RIGHT
        if(s >= gridWidth  && s % gridWidth < gridWidth - 1 )
            T[s][UP_RIGHT][s - gridWidth + 1] = 1.0;
        else
            T[s][UP_RIGHT][s] = 1.0;

        //DOWN_LEFT
        if(s < (gridHeight - 1) * gridWidth && s % gridWidth > 0)
            T[s][DOWN_LEFT][s + gridWidth - 1] = 1.0;
        else
            T[s][DOWN_LEFT][s] = 1.0;

        //DOWN_RIGHT
        if(s < (gridHeight - 1) * gridWidth && s % gridWidth < gridWidth - 1)
            T[s][DOWN_RIGHT][s + gridWidth + 1] = 1.0;
        else
            T[s][DOWN_RIGHT][s] = 1.0;
        
        //STAY
        //T[s][STAY][s] = 1.0;

    }


}

void MDP::displayRewards(unsigned int width){
  for(unsigned int s = 0; s < numStates; s++)
  {
    if(s % width == 0) cout << endl;
    cout << setiosflags(ios::fixed)
      << setprecision(2)
      << R[s] << ", ";
  }
  cout  << endl;
}

void GridMDP::displayRewards()
{
  if (R == nullptr){
    cout << "ERROR: no rewards!" << endl;
    return;
  }
  for(unsigned int r = 0; r < gridHeight; r++)
  {
    for(unsigned int c = 0; c < gridWidth; c++)
    {
      unsigned int state = r*gridWidth + c;
      cout << setiosflags(ios::fixed)
        << setprecision(2)
        << R[state] << ", ";
    }
    cout << endl ;
  }
}



bool operator== (MDP & lhs, MDP & rhs)
{
  double* R1 = lhs.getRewards();
  double* R2 = rhs.getRewards();
  for(unsigned int s = 0; s < lhs.getNumStates(); s++){
    if(R1[s] != R2[s]) return false;
  }
  return true;

}

#endif
