

#include<iostream>
#include<vector>
#include<algorithm>
#include<map>
using namespace std;

int countPairs(int k, vector<int> a) 
{

    unordered_map<int, int> m;
    vecter<int>::iterator it;
 int n = a.size();

    for (int it = a.begin(); it! = a.end(); it++)
        m[*it]+=1;
 
    int t = 0;
 
    for (int it = a.begin(); it! = a.end(); it++){
        t += m[ k- (*it) ];
        if (k - (*it) == (*it)) t--;
    }
 
    return t/2;


}

int main(){
a[7] = {6,5,1,2,3,4,5}
vector<int> v(a,a+6)
cout << countPairs(7,v)<<endl;

return 0;
}