
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"






void body (){
log("hello!", true);

};void for_loop (int i){
if (i > 0) {
i = i - 1;
body();
for_loop(i);

}
;

};



int main(){
    for_loop(10);


}