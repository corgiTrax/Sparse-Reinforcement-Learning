#ifndef grid_domains_h
#define grid_domains_h

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <functional>

using namespace std;

void split(const string& s, char c,
           vector<string>& v) {
   string::size_type i = 0;
   string::size_type j = s.find(c);

   while (j != string::npos) {
      v.push_back(s.substr(i, j-i));
      i = ++j;
      j = s.find(c, j);

      if (j == string::npos)
         v.push_back(s.substr(i, s.length()));
   }
}

double** initFeaturesDiscreteDomain(const int numStates, const int numFeatures, string domain_file_name)
{
    double** stateFeatures;
    stateFeatures = new double*[numStates]; //numFeatures = 3; // target, obstacle, pathpoint
    
    //Initialize all features to 0
    for(int i=0; i<numStates; i++)
    {
        stateFeatures[i] = new double[numFeatures];
        double feature[numFeatures];
        for (int feat=0; feat < numFeatures; feat++) feature[feat] = 0;
        feature[3] = 1;
        copy(feature, feature+numFeatures, stateFeatures[i]);
    }
    
    ifstream feature_file (domain_file_name);

    if(feature_file.is_open())
    {
        cout << "loading features..." << endl;
        string line;
        while(getline(feature_file,line))
        {
         vector<string> results;
         split(line,',', results);
          unsigned int state = stoi(results[0]);
          unsigned int feature = stoi(results[1]);
          double value = stod(results[2]);
          if ( state < 0 || state > numStates - 1) continue;
          stateFeatures[state][feature] = value;
        }
        feature_file.close();
    }
    return stateFeatures;
}




#endif

