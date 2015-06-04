#include<vector>
using std::vector;
#include<numeric>
using std::accumulate;
#include<cmath>
using std::pow; using std::sqrt; using std::sin; using std::cos; using std::abs;

//This was just for testing arrays
double add_array(double* ary, int sz){
  double sum = 0;
  for(int i = 0; i < sz; ++i){
    sum += ary[i];
  }
  return sum;
}

float inline adding_squares(float tot, float val){
  //Inline function made for accumulate in sphere_function
  return tot + (val*val);
}

float cpp_sphere_function(double* vals, long sz){
  //Accumulates the squares of all vals
  return accumulate(vals, vals + sz, 0.0, adding_squares);
}

float cpp_rosenbrock_function(double* vals, long sz){
  //The rosenbrock function! It does things!
  double tot = 0.0;
  for(long i = 0; i < (sz - 1); ++i){
    tot += (100.0 * pow(vals[i+1] - (pow(vals[i], 2)), 2) + pow(vals[i] - 1, 2));
  }
  return tot;
}

float cpp_rana_function(double* vals, long sz, double* weights){
  //The rana function! It does more things! Wow!
  double tot = 0.0, x, y;
  for(long i = 0; i < sz; ++i){
    x = vals[i];
    if(i == (sz - 1)){
      y = vals[0];
    }
    else{
      y = vals[i + 1];
    }
    tot += weights[i] * (x * sin(sqrt(abs(y + 1 - x))) * cos(sqrt(abs(x + y + 1)))
			 + (y + 1) * cos(sqrt(abs(y + 1 - x))) * sin(sqrt(abs(x + y + 1))));
  }
  return tot;
}

float cpp_schafferF7(double* vals, long sz){
  //The schafferF7 function! It does other things!
  double tot = 0.0, norm = 1.0/sz, si;
  for(long i = 0; i < sz - 1; ++i){
    si = sqrt(pow(vals[i], 2) + pow(vals[i + 1], 2));
    tot += pow(norm * sqrt(si) * (sin(50 * pow(si, 0.20)) + 1), 2);
  }
  return tot;
}

float cpp_deceptive(double* vals, long sz){
  //The deceptive function. It does stuff.
  double decep = 0.20, best = 1.0, decep_best = 0.7, tot = 0.0;
  for(long i = 0; i < sz; ++i){
    if(vals[i] < decep){
      tot += vals[i] * (-1.0 / decep) + best;
    }
    else{
      tot += (vals[i] - decep) * (decep_best / (1.0 - decep));
    }
  }
  return tot / sz;
}
