// https://stackoverflow.com/questions/3929774/how-much-overhead-is-there-when-creating-a-thread
//
// Run with
//  g++ thread_cost.cpp -std=c++11 -lpthread -O3 -o thread_cost
#include <thread>

int main(int argc, char** argv)
{
    for (volatile int i = 0; i < 100000; i++)
        std::thread([](){}).detach();
    return 0;
}
