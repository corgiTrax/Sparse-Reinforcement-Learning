OBJS = build/birl_test.o build/feature_birl_test.o
TEST_OBJS =  build/birl_test.o build/feature_birl_test.o
CC = g++ -std=c++11 -O3
DEBUG = -g  
CFLAGS = -c $(DEBUG)
LFLAGS = $(DEBUG)


all: feature_birl_test birl_test

feature_birl_test: build/feature_birl_test.o 
	$(CC) $(LFLAGS) build/feature_birl_test.o -o feature_birl_test 

birl_test: $(OBJS)
	$(CC) $(LFLAGS) build/birl_test.o -o birl_test


build/birl_test.o: src/birl_test.cpp include/feature_birl.hpp include/mdp.hpp
	$(CC) $(CFLAGS) src/birl_test.cpp -o build/birl_test.o

build/feature_birl_test.o: src/feature_birl_test.cpp include/feature_birl.hpp include/mdp.hpp include/grid_domain.hpp
	$(CC) $(CFLAGS) src/feature_birl_test.cpp -o build/feature_birl_test.o

clean:
	\rm build/*.o src/*~ birl_test feature_birl_test

memchk:
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=40 --track-fds=yes --track-origins=yes ./birl_test

memchk2:
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=40 --track-fds=yes --track-origins=yes ./feature_birl_test 26 5 1


