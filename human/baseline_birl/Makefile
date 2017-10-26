OBJS = build/birl_test.o build/feature_birl_test.o
TEST_OBJS =  build/birl_test.o build/feature_birl_test.o
CC = g++ -std=c++11 -O3
DEBUG = -g  
CFLAGS = -c $(DEBUG)
LFLAGS = $(DEBUG)


all: feature_birl_test birl_test

reward_learning: build/feature_birl_test.o 
	$(CC) $(LFLAGS) build/reward_learning.o -o reward_learning 

test_reward: $(OBJS)
	$(CC) $(LFLAGS) build/test_reward.o -o test_reward


build/birl_test.o: src/test_reward.cpp include/feature_birl.hpp include/mdp.hpp
	$(CC) $(CFLAGS) src/test_reward.cpp -o build/test_reward.o

build/feature_birl_test.o: src/reward_learning.cpp include/feature_birl.hpp include/mdp.hpp include/grid_domain.hpp
	$(CC) $(CFLAGS) src/reward_learning.cpp -o build/reward_learning.o

clean:
	\rm build/*.o src/*~ reward_learning test_reward

memchk:
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=40 --track-fds=yes --track-origins=yes ./birl_test

memchk2:
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=40 --track-fds=yes --track-origins=yes ./feature_birl_test 26 5 1


