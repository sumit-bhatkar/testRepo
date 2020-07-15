#include <iostream>
#include <ctime>

class Timer
{
public:
    Timer() { clock_gettime(CLOCK_REALTIME, &beg_); }

    double elapsed() {
        clock_gettime(CLOCK_REALTIME, &end_);
        return (end_.tv_sec - beg_.tv_sec)*1000 +
            (end_.tv_nsec - beg_.tv_nsec) / 1000000.;
    }

    void reset() { clock_gettime(CLOCK_REALTIME, &beg_); }

private:
    timespec beg_, end_;
};

// Timer tmr
// double t = tmr.elapsed();
// std::cout << "10M records : single thread prod / 10 partition :: " << t << " msec"<< std::endl;
