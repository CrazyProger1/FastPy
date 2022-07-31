
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"






void draw_vert_border (bool endl = false){
log("|", endl);

};void draw_horz_border (){
log("+-+-+-+", true);

};void draw_row (str a, str b, str c){
draw_vert_border();
log(a);
draw_vert_border();
log(b);
draw_vert_border();
log(c);
draw_vert_border(true);

};void draw (str a, str b, str c, str d, str e, str f, str g, str h, str i){
draw_horz_border();
draw_row(a, b, c);
draw_horz_border();
draw_row(d, e, f);
draw_horz_border();
draw_row(g, h, i);
draw_horz_border();

};void draw_game_over (str winner){
log("Game over! ");
log("Won: ");
log(winner, true);

};void check_three (str a, str b, str c){
auto empty = " ";
if (a == b && b == c && c != empty) {
draw_game_over(a);

}
;

};void check_game_over (str a, str b, str c, str d, str e, str f, str g, str h, str i){
check_three(a, b, c);
check_three(a, d, g);
check_three(a, e, i);
check_three(b, e, h);
check_three(c, f, i);
check_three(c, e, g);
check_three(d, e, f);

};



int main(){
    auto a = " ";


auto b = " ";


auto c = " ";


auto d = " ";


auto e = " ";


auto f = " ";


auto g = " ";


auto h = " ";


auto i = " ";


auto move = "X";


auto x = "X";


auto o = "O";


while (true)
{
draw(a, b, c, d, e, f, g, h, i);

log(move);

int cell = input<int>(" enter cell number (1 - 9) >>");


if (cell == 1) {
a = move;

}

else if (cell == 2) {
b = move;

}

else if (cell == 3) {
c = move;

}

else if (cell == 4) {
d = move;

}

else if (cell == 5) {
e = move;

}

else if (cell == 6) {
f = move;

}

else if (cell == 7) {
g = move;

}

else if (cell == 8) {
h = move;

}

else if (cell == 9) {
i = move;

}

check_game_over(a, b, c, d, e, f, g, h, i);

if (move == x) {
move = o;

}

else {
auto move = x;

}


}
;


}