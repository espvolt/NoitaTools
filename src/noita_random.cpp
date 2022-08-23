// https://github.com/kaliuresis/noa/blob/main/src/noita_random.cpp
// https://github.com/TwoAbove/noita-tools/blob/31c59bc1399c61e7d933d14e3ee31165680eacb4/src/services/SeedInfo/noita_random/noita_random.cpp
#include <stdint.h>
#include <math.h>



typedef unsigned int uint;

typedef uint8_t byte;
typedef int8_t int8;
typedef int16_t int16;
typedef int32_t int32;
typedef int64_t int64;
typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;
typedef uint64_t uint64;
typedef uint8 bool8;

#define ever (;;)

#define len(array) sizeof(array)/sizeof((array)[0])


extern "C" double SetRandomSeed(uint64 world_seed, double x, double y);

extern "C" int Random(int a, int b, double* random_seed) {
    int iVar1;

    iVar1 = (int) *random_seed * 0x41a7 + ((int) *random_seed / 0x1f31d) * -0x7fffffff;
    if (iVar1 < 1) {
        iVar1 = iVar1 + 0x7fffffff;
    }

    *random_seed = (double)iVar1;

    return (int)(a - (int)((double)((b - a) + 1) * (double)iVar1 * -4.656612875e-10));
}

extern "C" double Randomf(double a, double b, double* random_seed) {
    int iVar1;

    iVar1 = (int) *random_seed * 0x41a7 + ((int) *random_seed / 0x1f31d) * -0x7fffffff;
    if (iVar1 < 1) {
        iVar1 = iVar1 + 0x7fffffff;
    }

    *random_seed = (double)iVar1;

    return (a - (int)((double)((b - a) + 1) * (double)iVar1 * -4.656612875e-10));
}

extern "C" double Randomfn(double* random_seed) {
    int iVar1;

    iVar1 = (int) *random_seed * 0x41a7 + ((int) *random_seed / 0x1f31d) * -0x7fffffff;
    if (iVar1 < 1) {
        iVar1 = iVar1 + 0x7fffffff;
    }

    *random_seed = (double)iVar1;

    return *random_seed * 4.656612875e-10;
}

extern "C" double ProceduralRandomfn(uint64 worldSeed, double x, double y) {
    double seed = SetRandomSeed(worldSeed, x, y);
    return Randomfn(&seed);
}

extern "C" double ProceduralRandomf(uint64 worldSeed, double x, double y, int a, int b) {
    double seed = SetRandomSeed(worldSeed, x, y);
    return Randomf(a, b, &seed);
}

extern "C" int ProceduralRandomi(uint64 worldSeed, double x, double y, int a, int b) {
    double seed = SetRandomSeed(worldSeed, x, y);
    return Random(a, b, &seed);
}

float GetDistribution(float mean, float sharpness, float baseline, double* seed) {
    int i = 0;
    do
    {
        float r1 = Randomfn(seed);
        float r2 = Randomfn(seed);
        float div = fabs(r1 - mean);
        if (r2 < ((1.0 - div) * baseline))
        {
            return r1;
        }
        if (div < 0.5)
        {
            // double v11 = sin(((0.5f - mean) + r1) * M_PI);
            float v11 = sin(((0.5f - mean) + r1) * 3.1415f);
            float v12 = pow(v11, sharpness);
            if (v12 > r2)
            {
                return r1;
            }
        }
        i++;
    } while (i < 100);
    return Randomfn(seed);
}


extern "C" float RandomDistributionf(float min, float max, float mean, float sharpness, double* seed)
{
    if (sharpness == 0.0)
    {
        float r = Randomfn(seed);
        return (r * (max - min)) + min;
    }
    float adjMean = (mean - min) / (max - min);
    return min + (max - min) * GetDistribution(adjMean, sharpness, 0.005f, seed); // Baseline is always this
}

extern "C" int RandomDistribution(int min, int max, int mean, float sharpness, double* seed)
{
    if (sharpness == 0)
    {
        return Random(min, max, seed);
    }

    float adjMean = (float)(mean - min) / (float)(max - min);
    float v7 = GetDistribution(adjMean, sharpness, 0.005f, seed); // Baseline is always this
    int d = (int)round((float)(max - min) * v7);
    return min + d;
}

double Next(double random_seed) {
    int iVar1;

    iVar1 = (int) random_seed * 0x41a7 + ((int) random_seed / 0x1f31d) * -0x7fffffff;
    if (iVar1 < 1) {
        iVar1 = iVar1 + 0x7fffffff;
    }
    random_seed = (double)iVar1;
    return random_seed;
}

uint64 SetRandomSeedHelper(double r)
{
    uint64 e = *(uint64*)&r;
    if(((e >> 0x20 & 0x7fffffff) < 0x7FF00000)
       && (-9.223372036854776e+18 <= r) && (r < 9.223372036854776e+18))
    {
        //should be same as e &= ~(1<<63); which should also just clears the sign bit,
        //or maybe it does nothing,
        //but want to keep it as close to the assembly as possible for now
        e <<= 1;
        e >>= 1;
        double s = *(double*) &e;
        uint64 i = 0;
        if(s != 0.0)
        {
            uint64 f = (((uint64) e) & 0xfffffffffffff) | 0x0010000000000000;
            uint64 g = 0x433 - ((uint64) e >> 0x34);
            uint64 h = f >> g;

            int j = -(uint)(0x433 < ((e >> 0x20)&0xFFFFFFFF) >> 0x14);
            i = (uint64) j<<0x20 | j;
            i = ~i & h | f << (((uint64) s >> 0x34) - 0x433) & i;
            i = ~-(uint64)(r == s) & -i | i & -(uint64)(r == s);
            // error handling, whatever
            // f = f ^
            // if((int) g > 0 && f )
        }
        return i & 0xFFFFFFFF;
    }

    //error!
    uint64 error_ret_val = 0x8000000000000000;
    return *(double*) &error_ret_val;
}

uint SetRandomSeedHelper2(int param_1,int param_2,uint param_3)
{
    uint uVar1;
    uint uVar2;
    uint uVar3;

    uVar2 = (param_1 - param_2) - param_3 ^ param_3 >> 0xd;
    uVar1 = (param_2 - uVar2) - param_3 ^ uVar2 << 8;
    uVar3 = (param_3 - uVar2) - uVar1 ^ uVar1 >> 0xd;
    uVar2 = (uVar2 - uVar1) - uVar3 ^ uVar3 >> 0xc;
    uVar1 = (uVar1 - uVar2) - uVar3 ^ uVar2 << 0x10;
    uVar3 = (uVar3 - uVar2) - uVar1 ^ uVar1 >> 5;
    uVar2 = (uVar2 - uVar1) - uVar3 ^ uVar3 >> 3;
    uVar1 = (uVar1 - uVar2) - uVar3 ^ uVar2 << 10;
    return (uVar3 - uVar2) - uVar1 ^ uVar1 >> 0xf;
}

extern "C" double SetRandomSeed(uint64 world_seed, double x, double y) {
    double random_seed = 0;
    uint a = world_seed ^ 0x93262e6f;
    uint b = a & 0xfff;
    uint c = (a >> 0xc) & 0xfff;

    double x_ = x+b;

    double y_ = y+c;

    double r = x_*134217727.0;
    uint64 e = SetRandomSeedHelper(r);

    uint64 _x = (*(uint64*) &x_ & 0x7FFFFFFFFFFFFFFF);
    uint64 _y = (*(uint64*) &y_ & 0x7FFFFFFFFFFFFFFF);
    if(102400.0 <= *((double*) &_y) || *((double*) &_x) <= 1.0) {
        r = y_*134217727.0;
    }
    else {
        double y__ = y_*3483.328;
        double t = e;
        y__ += t;
        y_ *= y__;
        r = y_;
    }

    uint64 f = SetRandomSeedHelper(r);

    uint g = SetRandomSeedHelper2(e, f, world_seed);
    double s = g;
    s /= 4294967295.0;
    s *= 2147483639.0;
    s += 1.0;

    if(2147483647.0 <= s) {
        s = s*0.5;
    }
    random_seed = s;


    random_seed = Next(random_seed);

    uint h = world_seed&3;
    while(h) {
        random_seed = Next(random_seed);
        h--;
    }

    return random_seed;
}
